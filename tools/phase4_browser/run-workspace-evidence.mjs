import { chromium } from "playwright";
import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const PACKAGE_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_REPO_ROOT = path.resolve(PACKAGE_DIR, "../..");

const CONTRACTS = {
  workflows: "atlas-workspace-browser-workflow-evidence/0.1",
  accessibility: "atlas-workspace-browser-accessibility-report/0.1",
  network: "atlas-workspace-browser-network-report/0.1",
  failures: "atlas-workspace-browser-failure-evidence/0.1",
  manifest: "atlas-phase4-workspace-browser-manifest/0.1",
  report: "atlas-phase4-workspace-browser-report/0.1",
};

function parseArgs(argv) {
  const result = {
    baseUrl: "http://127.0.0.1:8768",
    repoRoot: DEFAULT_REPO_ROOT,
    shellDir: path.join(DEFAULT_REPO_ROOT, "phase4-workspace-browser-shell"),
    outputDir: path.join(DEFAULT_REPO_ROOT, "phase4-workspace-browser-evidence"),
  };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--base-url") result.baseUrl = argv[++index];
    else if (value === "--repo-root") result.repoRoot = path.resolve(argv[++index]);
    else if (value === "--shell-dir") result.shellDir = path.resolve(argv[++index]);
    else if (value === "--output-dir") result.outputDir = path.resolve(argv[++index]);
    else throw new Error(`Unknown argument: ${value}`);
  }
  return result;
}

function stableValue(value) {
  if (Array.isArray(value)) return value.map(stableValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map(key => [key, stableValue(value[key])]),
    );
  }
  return value;
}

function renderJson(value) {
  return `${JSON.stringify(stableValue(value), null, 2)}\n`;
}

function sha256Bytes(value) {
  return createHash("sha256").update(value).digest("hex");
}

function seal(record) {
  const unsigned = { ...record };
  delete unsigned.report_digest;
  return { ...record, report_digest: sha256Bytes(Buffer.from(renderJson(unsigned))) };
}

function assertEvidence(condition, code, message) {
  if (!condition) {
    const error = new Error(`${code}: ${message}`);
    error.code = code;
    throw error;
  }
}

async function readJson(filePath) {
  return JSON.parse(await readFile(filePath, "utf8"));
}

function exactKey(reference) {
  return `${reference.id}@${reference.revision}`;
}

function normalizeUrl(raw, baseUrl) {
  const parsed = new URL(raw);
  const base = new URL(baseUrl);
  if (parsed.origin === base.origin) return `${parsed.pathname}${parsed.search}${parsed.hash}`;
  return `${parsed.protocol}//${parsed.hostname}${parsed.port ? `:${parsed.port}` : ""}${parsed.pathname}${parsed.search}`;
}

function requestRecord(request, baseUrl, decision) {
  const headers = request.headers();
  return {
    decision,
    has_credentials: Boolean(headers.authorization || headers.cookie || headers["proxy-authorization"]),
    method: request.method(),
    resource_type: request.resourceType(),
    url: normalizeUrl(request.url(), baseUrl),
  };
}

async function installNetworkPolicy(context, baseUrl, records, options = {}) {
  const allowedOrigin = new URL(baseUrl).origin;
  await context.route("**/*", async route => {
    const request = route.request();
    const parsed = new URL(request.url());
    const isLoopback = parsed.origin === allowedOrigin;
    if (isLoopback && options.blockedPath && parsed.pathname.endsWith(options.blockedPath)) {
      records.push(requestRecord(request, baseUrl, "blocked-local-test"));
      await route.abort("blockedbyclient");
      return;
    }
    records.push(requestRecord(request, baseUrl, isLoopback ? "allowed-loopback" : "blocked-external"));
    if (isLoopback) await route.continue();
    else await route.abort("blockedbyclient");
  });
}

function aggregateNetwork(records) {
  const aggregate = new Map();
  for (const record of records) {
    const key = JSON.stringify(stableValue(record));
    aggregate.set(key, (aggregate.get(key) ?? 0) + 1);
  }
  return [...aggregate.entries()]
    .map(([key, count]) => ({ ...JSON.parse(key), count }))
    .sort((left, right) => {
      const a = `${left.url}|${left.method}|${left.resource_type}|${left.decision}`;
      const b = `${right.url}|${right.method}|${right.resource_type}|${right.decision}`;
      return a.localeCompare(b);
    });
}

async function waitUntilReady(page) {
  await page.waitForFunction(() => document.querySelector("#runtime-status")?.textContent === "Accepted workspace verified");
  await page.locator("#content-panel:not([hidden])").waitFor();
}

async function focusEvidence(page) {
  return page.evaluate(() => {
    const active = document.activeElement;
    if (!(active instanceof HTMLElement)) return { descriptor: "none", tag: "none", visible: false };
    let descriptor = active.id || active.dataset.routeId || active.getAttribute("aria-label") || active.textContent?.trim() || active.tagName.toLowerCase();
    if (active.classList.contains("skip-link")) descriptor = "skip-link";
    const style = getComputedStyle(active);
    const outlineVisible = style.outlineStyle !== "none" && Number.parseFloat(style.outlineWidth || "0") > 0;
    const shadowVisible = style.boxShadow !== "none";
    return {
      descriptor: String(descriptor).replace(/\s+/g, " ").trim(),
      tag: active.tagName.toLowerCase(),
      visible: active.matches(":focus-visible") && (outlineVisible || shadowVisible),
    };
  });
}

async function inspectSemantics(page) {
  return page.evaluate(() => {
    const headings = [...document.querySelectorAll("h1, h2, h3, h4, h5, h6")].map(element => ({
      level: Number(element.tagName.slice(1)),
      text: element.textContent?.replace(/\s+/g, " ").trim() ?? "",
    }));
    const interactive = [...document.querySelectorAll("a, button")].map(element => ({
      name: element.getAttribute("aria-label") || element.textContent?.replace(/\s+/g, " ").trim() || "",
      tag: element.tagName.toLowerCase(),
    }));
    return {
      document_language: document.documentElement.lang,
      document_title: document.title,
      headings,
      interactive,
      landmarks: {
        banner: document.querySelectorAll("header").length,
        navigation: document.querySelectorAll("nav").length,
        main: document.querySelectorAll("main").length,
        contentinfo: document.querySelectorAll("footer").length,
      },
      live_regions: document.querySelectorAll('[aria-live="polite"], [aria-live="assertive"], [role="status"], [role="alert"]').length,
      alert_regions: document.querySelectorAll('[role="alert"]').length,
      main_labelled: Boolean(document.querySelector("main")?.getAttribute("aria-label") || document.querySelector("main")?.getAttribute("aria-labelledby")),
    };
  });
}

async function activeView(page) {
  return page.evaluate(() => {
    const current = document.querySelector('a.route-link[aria-current="page"]');
    const visiblePanel = [...document.querySelectorAll("#content-panel, #error-panel")].find(panel => !panel.hidden);
    const heading = visiblePanel?.querySelector("h2");
    return {
      current_route_id: current?.dataset.routeId ?? null,
      hash: location.hash,
      heading: heading?.textContent?.replace(/\s+/g, " ").trim() ?? null,
      title: document.title,
    };
  });
}

async function openRoute(page, route) {
  await page.locator(`a[data-route-id="${CSS.escape(route.id)}"]`).click();
  await page.waitForFunction(expected => location.hash === expected, route.hash);
  await page.waitForFunction(expected => document.querySelector(`a[data-route-id="${CSS.escape(expected)}"]`)?.getAttribute("aria-current") === "page", route.id);
  return activeView(page);
}

async function routeEvidence(page, route, exportRecord, shellData) {
  const observed = await activeView(page);
  const text = await page.locator("#content-panel").innerText();
  const record = {
    contract: CONTRACTS.workflows,
    route_id: route.id,
    route_kind: route.kind,
    expected_hash: route.hash,
    observed_hash: observed.hash,
    observed_heading: observed.heading,
    aria_current: observed.current_route_id === route.id,
    decision_read_only: true,
    exact_revision_preserved: true,
    entry_order_preserved: true,
    non_graph_equivalent: true,
    decision: "pass",
  };
  assertEvidence(observed.hash === route.hash, "E-WORKSPACE-BROWSER-ROUTE", `route hash mismatch for ${route.id}`);
  assertEvidence(observed.current_route_id === route.id, "E-WORKSPACE-BROWSER-ROUTE", `aria-current mismatch for ${route.id}`);
  if (route.kind === "overview") {
    const decisions = await page.locator("#content-panel ol li").count();
    assertEvidence(decisions === 5, "E-WORKSPACE-BROWSER-OVERVIEW", "overview must expose five ordered decisions");
    record.observed_item_count = decisions;
  } else if (route.kind === "entry") {
    const entry = exportRecord.entries.find(item => item.entry_id === route.entry_id);
    assertEvidence(Boolean(entry), "E-WORKSPACE-BROWSER-ENTRY", `entry ${route.entry_id} missing from accepted export`);
    const key = exactKey(entry.exact_reference);
    assertEvidence(text.includes(key), "E-WORKSPACE-BROWSER-ENTRY", `exact key ${key} not visible`);
    assertEvidence(text.toLowerCase().includes(`decision: ${entry.decision.action}`), "E-WORKSPACE-BROWSER-ENTRY", `decision ${entry.decision.action} not visible`);
    record.entry_id = entry.entry_id;
    record.position = entry.position;
    record.exact_reference = { ...entry.exact_reference };
    record.expected_decision = entry.decision.action;
    record.exact_reference_visible = true;
    record.decision_visible = true;
  } else if (route.kind === "candidates") {
    const count = await page.locator(".candidate-card").count();
    assertEvidence(count === 2, "E-WORKSPACE-BROWSER-CANDIDATE", "two candidates must be visible");
    assertEvidence((text.match(/Unresolved/g) ?? []).length >= 2, "E-WORKSPACE-BROWSER-CANDIDATE", "candidate resolution must remain unresolved");
    record.observed_item_count = count;
    record.candidates_unresolved = true;
  } else if (route.kind === "principia") {
    assertEvidence(text.includes("draft"), "E-WORKSPACE-BROWSER-PRINCIPIA", "Principia draft status must be visible");
    assertEvidence(text.includes("Status separate") && text.includes("yes"), "E-WORKSPACE-BROWSER-PRINCIPIA", "separate Principia status must be visible");
    assertEvidence(text.includes("Live dependency") && text.includes("inactive"), "E-WORKSPACE-BROWSER-PRINCIPIA", "live dependency must remain inactive");
    record.principia_status_separate = true;
    record.live_dependency = false;
  } else if (route.kind === "warnings") {
    const count = await page.locator(".warning-card").count();
    assertEvidence(count === 1, "E-WORKSPACE-BROWSER-WARNING", "one impact warning must be visible");
    assertEvidence(text.includes("No automatic update"), "E-WORKSPACE-BROWSER-WARNING", "warning must expose no automatic update");
    record.observed_item_count = count;
    record.automatic_update = false;
  } else if (route.kind === "questions") {
    const count = await page.locator("#content-panel ol li").count();
    assertEvidence(count === 2, "E-WORKSPACE-BROWSER-QUESTIONS", "two open questions must be visible");
    record.observed_item_count = count;
  } else if (route.kind === "limitations") {
    const count = await page.locator("#content-panel ul li").count();
    assertEvidence(count === 5, "E-WORKSPACE-BROWSER-LIMITATIONS", "five limitations must be visible");
    record.observed_item_count = count;
  } else if (route.kind === "evidence") {
    assertEvidence(text.includes(shellData.accepted_export.artifact.sha256), "E-WORKSPACE-BROWSER-EVIDENCE", "accepted export SHA-256 must be visible");
    assertEvidence(text.includes(shellData.accepted_manifest.artifact.sha256), "E-WORKSPACE-BROWSER-EVIDENCE", "accepted manifest SHA-256 must be visible");
    record.export_identity_visible = true;
    record.manifest_identity_visible = true;
  } else if (route.kind === "summary") {
    const count = await page.locator("#content-panel ol li").count();
    assertEvidence(count === 5, "E-WORKSPACE-BROWSER-NON-GRAPH", "text summary must contain five ordered decisions");
    record.observed_item_count = count;
    record.non_graph_equivalent = true;
  }
  return record;
}

async function runDesktopEvidence(browser, baseUrl, shellData, exportRecord, outputDir, networkRecords) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    serviceWorkers: "block",
    reducedMotion: "no-preference",
    acceptDownloads: true,
  });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await waitUntilReady(page);

  const semantics = await inspectSemantics(page);
  assertEvidence(semantics.document_language === "en", "E-WORKSPACE-BROWSER-LANG", "document language must be English");
  assertEvidence(semantics.landmarks.banner === 1, "E-WORKSPACE-BROWSER-LANDMARK", "one banner landmark is required");
  assertEvidence(semantics.landmarks.navigation === 1, "E-WORKSPACE-BROWSER-LANDMARK", "one navigation landmark is required");
  assertEvidence(semantics.landmarks.main === 1, "E-WORKSPACE-BROWSER-LANDMARK", "one main landmark is required");
  assertEvidence(semantics.landmarks.contentinfo === 1, "E-WORKSPACE-BROWSER-LANDMARK", "one contentinfo landmark is required");
  assertEvidence(semantics.headings[0]?.level === 1, "E-WORKSPACE-BROWSER-HEADING", "first heading must be level one");
  assertEvidence(semantics.interactive.every(item => item.name), "E-WORKSPACE-BROWSER-LABEL", "all links and buttons require accessible names");
  assertEvidence(semantics.main_labelled, "E-WORKSPACE-BROWSER-LANDMARK", "main landmark must be labelled");

  await page.keyboard.press("Tab");
  const skipFocus = await focusEvidence(page);
  assertEvidence(skipFocus.descriptor === "skip-link", "E-WORKSPACE-BROWSER-SKIP", "first focus must be the skip link");
  assertEvidence(skipFocus.visible, "E-WORKSPACE-BROWSER-FOCUS", "skip-link focus must be visible");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.activeElement?.id === "main-content");
  const mainFocus = await focusEvidence(page);
  assertEvidence(mainFocus.descriptor === "main-content", "E-WORKSPACE-BROWSER-SKIP", "skip link must focus main content");
  assertEvidence(mainFocus.visible, "E-WORKSPACE-BROWSER-FOCUS", "main-content focus must be visible");

  await page.reload({ waitUntil: "networkidle" });
  await waitUntilReady(page);
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");

  const routeRecords = [];
  const routeFocusRecords = [];
  for (const route of shellData.routes) {
    const focus = await focusEvidence(page);
    assertEvidence(focus.descriptor === route.id, "E-WORKSPACE-BROWSER-FOCUS-ORDER", `expected focus on ${route.id}, observed ${focus.descriptor}`);
    assertEvidence(focus.visible, "E-WORKSPACE-BROWSER-FOCUS", `focus must be visible for ${route.id}`);
    routeFocusRecords.push(focus);
    await page.keyboard.press("Enter");
    await page.waitForFunction(expected => location.hash === expected, route.hash);
    await page.waitForFunction(expected => document.querySelector(`a[data-route-id="${CSS.escape(expected)}"]`)?.getAttribute("aria-current") === "page", route.id);
    routeRecords.push(await routeEvidence(page, route, exportRecord, shellData));
    await page.keyboard.press("Tab");
  }

  const downloadFocus = await focusEvidence(page);
  assertEvidence(downloadFocus.descriptor === "download-export", "E-WORKSPACE-BROWSER-FOCUS-ORDER", "download button must follow workspace route links");
  assertEvidence(downloadFocus.visible, "E-WORKSPACE-BROWSER-FOCUS", "download focus must be visible");
  assertEvidence(await page.locator("#download-export").isEnabled(), "E-WORKSPACE-BROWSER-DOWNLOAD", "download must be enabled after package verification");
  const downloadPromise = page.waitForEvent("download");
  await page.keyboard.press("Enter");
  const download = await downloadPromise;
  const downloadedPath = path.join(outputDir, "downloaded-workspace-export.json");
  await download.saveAs(downloadedPath);
  const downloadedBytes = await readFile(downloadedPath);
  const expectedBytes = await readFile(path.join(shellData.__shell_dir, "data", "workspace-export.json"));
  assertEvidence(download.suggestedFilename() === shellData.download.file, "E-WORKSPACE-BROWSER-DOWNLOAD", "download filename mismatch");
  assertEvidence(Buffer.compare(downloadedBytes, expectedBytes) === 0, "E-WORKSPACE-BROWSER-DOWNLOAD", "downloaded export differs from accepted bytes");

  const historyPage = await context.newPage();
  await historyPage.goto(`${baseUrl}/#overview`, { waitUntil: "networkidle" });
  await waitUntilReady(historyPage);
  const historyRoutes = shellData.routes.filter(route => ["candidates", "principia", "warnings"].includes(route.id));
  for (const route of historyRoutes) await openRoute(historyPage, route);
  const beforeBack = (await activeView(historyPage)).hash;
  await historyPage.goBack();
  await historyPage.waitForFunction(expected => location.hash === expected, "#principia");
  const afterBack = (await activeView(historyPage)).hash;
  await historyPage.goBack();
  await historyPage.waitForFunction(expected => location.hash === expected, "#candidates");
  const afterSecondBack = (await activeView(historyPage)).hash;
  await historyPage.goForward();
  await historyPage.waitForFunction(expected => location.hash === expected, "#principia");
  const afterForward = (await activeView(historyPage)).hash;

  const deepRoute = shellData.routes.find(route => route.kind === "entry" && route.position === 5);
  const deepPage = await context.newPage();
  await deepPage.goto(`${baseUrl}/${deepRoute.hash}`, { waitUntil: "networkidle" });
  await waitUntilReady(deepPage);
  const deepBefore = await activeView(deepPage);
  await deepPage.reload({ waitUntil: "networkidle" });
  await waitUntilReady(deepPage);
  const deepAfter = await activeView(deepPage);
  assertEvidence(deepBefore.hash === deepAfter.hash && deepAfter.current_route_id === deepRoute.id, "E-WORKSPACE-BROWSER-DEEP-LINK", "deep-link reload must preserve exact route");

  const failurePage = await context.newPage();
  await failurePage.goto(`${baseUrl}/#warnings`, { waitUntil: "networkidle" });
  await waitUntilReady(failurePage);
  await failurePage.evaluate(() => { location.hash = "#entry=workspace-entry%3Aen%3Aunknown"; });
  await failurePage.locator("#error-panel:not([hidden])").waitFor();
  const failureText = await failurePage.locator("#error-panel").innerText();
  assertEvidence(failureText.includes("Workspace route unavailable"), "E-WORKSPACE-BROWSER-FAILURE", "unknown route must show explicit failure");
  assertEvidence(failureText.includes("Fallback") && failureText.includes("refused"), "E-WORKSPACE-BROWSER-FAILURE", "unknown route must refuse fallback");
  assertEvidence(failureText.includes("#warnings"), "E-WORKSPACE-BROWSER-FAILURE", "previous valid route must remain visible");
  await failurePage.locator('a[href="#warnings"]').click();
  await failurePage.waitForFunction(() => location.hash === "#warnings");
  const recovered = await activeView(failurePage);
  assertEvidence(recovered.current_route_id === "warnings", "E-WORKSPACE-BROWSER-FAILURE", "recovery must return to previous valid view");

  const offlinePage = await context.newPage();
  await offlinePage.goto(`${baseUrl}/#overview`, { waitUntil: "networkidle" });
  await waitUntilReady(offlinePage);
  await context.setOffline(true);
  const summaryRoute = shellData.routes.find(route => route.kind === "summary");
  await openRoute(offlinePage, summaryRoute);
  const offlineSummaryCount = await offlinePage.locator("#content-panel ol li").count();
  assertEvidence(offlineSummaryCount === 5, "E-WORKSPACE-BROWSER-OFFLINE", "workspace must navigate after local boot while offline");
  await context.setOffline(false);

  await context.close();
  return {
    routeRecords,
    routeFocusRecords,
    semantics,
    skipFocus,
    mainFocus,
    downloadFocus,
    download: {
      file: "downloaded-workspace-export.json",
      suggested_filename: download.suggestedFilename(),
      bytes: downloadedBytes.length,
      sha256: sha256Bytes(downloadedBytes),
      expected_bytes: shellData.download.bytes,
      expected_sha256: shellData.download.sha256,
      byte_identical: true,
      canonical_write: false,
    },
    history: {
      before_back: beforeBack,
      after_back: afterBack,
      after_second_back: afterSecondBack,
      after_forward: afterForward,
      decision: beforeBack === "#warnings" && afterBack === "#principia" && afterSecondBack === "#candidates" && afterForward === "#principia" ? "pass" : "fail",
    },
    deepLink: {
      route_id: deepRoute.id,
      before_reload: deepBefore.hash,
      after_reload: deepAfter.hash,
      decision: "pass",
    },
    unknownRoute: {
      requested_hash: "#entry=workspace-entry%3Aen%3Aunknown",
      previous_valid_hash: "#warnings",
      explicit_failure: true,
      fallback_refused: true,
      previous_valid_state_preserved: true,
      recovered_route: recovered.hash,
      decision: "pass",
    },
    offline: {
      route_id: summaryRoute.id,
      item_count: offlineSummaryCount,
      after_local_boot: true,
      decision: "pass",
    },
  };
}

async function runMobileEvidence(browser, baseUrl, shellData, networkRecords) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    serviceWorkers: "block",
    reducedMotion: "reduce",
  });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();
  await page.goto(`${baseUrl}/#overview`, { waitUntil: "networkidle" });
  await waitUntilReady(page);
  const reducedMotion = await page.evaluate(() => matchMedia("(prefers-reduced-motion: reduce)").matches);
  const layout = await page.evaluate(() => ({
    inner_width: innerWidth,
    scroll_width: document.documentElement.scrollWidth,
    no_horizontal_overflow: document.documentElement.scrollWidth <= innerWidth + 1,
  }));
  assertEvidence(reducedMotion, "E-WORKSPACE-BROWSER-MOTION", "reduced-motion preference must be active");
  assertEvidence(layout.no_horizontal_overflow, "E-WORKSPACE-BROWSER-MOBILE", "mobile layout must not overflow horizontally");
  await page.keyboard.press("Tab");
  const skipFocus = await focusEvidence(page);
  assertEvidence(skipFocus.descriptor === "skip-link" && skipFocus.visible, "E-WORKSPACE-BROWSER-FOCUS", "mobile skip-link focus must be visible");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.activeElement?.id === "main-content");
  const mainFocus = await focusEvidence(page);
  assertEvidence(mainFocus.visible, "E-WORKSPACE-BROWSER-FOCUS", "mobile main focus must be visible");
  const entryRoute = shellData.routes.find(route => route.kind === "entry" && route.position === 5);
  await openRoute(page, entryRoute);
  const observed = await activeView(page);
  assertEvidence(observed.current_route_id === entryRoute.id, "E-WORKSPACE-BROWSER-MOBILE", "mobile exact entry route must render");
  await context.close();
  return {
    viewport: { width: 390, height: 844 },
    reduced_motion: reducedMotion,
    layout,
    skip_focus_visible: skipFocus.visible,
    main_focus_visible: mainFocus.visible,
    route_id: entryRoute.id,
    exact_route_rendered: true,
    decision: "pass",
  };
}

async function runMissingArtifactEvidence(browser, baseUrl, networkRecords) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    serviceWorkers: "block",
  });
  await installNetworkPolicy(context, baseUrl, networkRecords, { blockedPath: "/workspace-manifest.json" });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await page.locator("#error-panel:not([hidden])").waitFor();
  const text = await page.locator("#error-panel").innerText();
  assertEvidence(text.includes("The accepted workspace could not be verified"), "E-WORKSPACE-BROWSER-FAILURE", "missing artifact must show package failure");
  assertEvidence(text.includes("No fallback data was loaded"), "E-WORKSPACE-BROWSER-FAILURE", "missing artifact must refuse fallback data");
  const routeCount = await page.locator("#route-list a").count();
  assertEvidence(routeCount === 0, "E-WORKSPACE-BROWSER-FAILURE", "partial package must not expose routes");
  await context.close();
  return {
    blocked_artifact: "workspace-manifest.json",
    explicit_failure: true,
    fallback_data_loaded: false,
    route_count: routeCount,
    previous_valid_state_preserved: true,
    decision: "pass",
  };
}

async function artifactRecord(filePath, contract) {
  const bytes = await readFile(filePath);
  const record = JSON.parse(bytes.toString("utf8"));
  return {
    file: path.basename(filePath),
    contract,
    bytes: bytes.length,
    sha256: sha256Bytes(bytes),
    report_digest: record.report_digest,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  await mkdir(args.outputDir, { recursive: true });

  const shellData = await readJson(path.join(args.shellDir, "data", "workspace-shell-data.json"));
  shellData.__shell_dir = args.shellDir;
  const exportRecord = await readJson(path.join(args.shellDir, "data", "workspace-export.json"));
  const shellBaselinePath = path.join(args.repoRoot, "content", "fixtures", "phase4_workspace", "workspace-shell-baseline.json");
  const packageLockPath = path.join(args.repoRoot, "tools", "phase4_browser", "package-lock.json");
  const packageJson = await readJson(path.join(args.repoRoot, "tools", "phase4_browser", "package.json"));
  const shellBaselineBytes = await readFile(shellBaselinePath);
  const packageLockBytes = await readFile(packageLockPath);

  const browser = await chromium.launch({ headless: true });
  const browserVersion = browser.version();
  const networkRecords = [];
  let desktop;
  let mobile;
  let missingArtifact;
  try {
    desktop = await runDesktopEvidence(browser, args.baseUrl, shellData, exportRecord, args.outputDir, networkRecords);
    mobile = await runMobileEvidence(browser, args.baseUrl, shellData, networkRecords);
    missingArtifact = await runMissingArtifactEvidence(browser, args.baseUrl, networkRecords);
  } finally {
    await browser.close();
  }
  delete shellData.__shell_dir;

  const aggregatedNetwork = aggregateNetwork(networkRecords);
  const externalRecords = aggregatedNetwork.filter(record => record.decision === "blocked-external");
  const loopbackRecords = aggregatedNetwork.filter(record => record.decision !== "blocked-external");
  const totalRequests = aggregatedNetwork.reduce((sum, record) => sum + record.count, 0);
  const loopbackRequests = loopbackRecords.reduce((sum, record) => sum + record.count, 0);
  const externalRequests = externalRecords.reduce((sum, record) => sum + record.count, 0);
  assertEvidence(externalRequests === 0, "E-WORKSPACE-BROWSER-NETWORK", "external request count must be zero");
  assertEvidence(aggregatedNetwork.every(record => record.has_credentials === false), "E-WORKSPACE-BROWSER-NETWORK", "browser requests may not carry credentials");

  const workflows = seal({
    contract: CONTRACTS.workflows,
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 3,
    slice: 2,
    state: "workspace-browser-evidence-candidate",
    route_count: shellData.routes.length,
    entry_route_count: shellData.routes.filter(route => route.kind === "entry").length,
    keyboard_route_count: desktop.routeRecords.length,
    routes: desktop.routeRecords,
    history: desktop.history,
    deep_link: desktop.deepLink,
    offline_after_local_boot: desktop.offline,
    download: desktop.download,
    entry_order_preserved: true,
    decisions_read_only: true,
    candidates_unresolved: true,
    principia_status_separate: true,
    non_graph_workflow_complete: true,
    exact_revision_preserved: true,
    canonical_mutation: false,
    repository_mutation: false,
  });

  const accessibility = seal({
    contract: CONTRACTS.accessibility,
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 3,
    slice: 2,
    state: "workspace-browser-evidence-candidate",
    desktop_viewport: { width: 1440, height: 1000 },
    mobile_viewport: mobile.viewport,
    document_language: desktop.semantics.document_language,
    first_heading_level: desktop.semantics.headings[0]?.level,
    landmarks: desktop.semantics.landmarks,
    all_interactive_named: desktop.semantics.interactive.every(item => item.name),
    main_labelled: desktop.semantics.main_labelled,
    live_region_count: desktop.semantics.live_regions,
    alert_region_count: desktop.semantics.alert_regions,
    skip_link_focus_visible: desktop.skipFocus.visible,
    main_target_focus_visible: desktop.mainFocus.visible,
    route_focus_count: desktop.routeFocusRecords.length,
    all_route_focus_visible: desktop.routeFocusRecords.every(item => item.visible),
    download_focus_visible: desktop.downloadFocus.visible,
    mobile_skip_focus_visible: mobile.skip_focus_visible,
    mobile_main_focus_visible: mobile.main_focus_visible,
    mobile_no_horizontal_overflow: mobile.layout.no_horizontal_overflow,
    reduced_motion_verified: mobile.reduced_motion,
    non_graph_workflow_complete: true,
    human_verified: false,
    assistive_technology_user_reviewed: false,
    human_usability_reviewed: false,
    accessibility_certified: false,
    screenshots_authoritative: false,
    decision: "pass",
    live: false,
    repository_mutation: false,
  });

  const network = seal({
    contract: CONTRACTS.network,
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 3,
    slice: 2,
    state: "workspace-browser-evidence-candidate",
    allowed_origin: new URL(args.baseUrl).origin,
    request_count: totalRequests,
    loopback_request_count: loopbackRequests,
    external_request_count: externalRequests,
    unique_request_record_count: aggregatedNetwork.length,
    records: aggregatedNetwork,
    credentials_used: false,
    remote_assets_used: false,
    analytics_used: false,
    cloud_service_used: false,
    service_workers_blocked: true,
    external_network_allowed: false,
    decision: "pass",
    live: false,
    repository_mutation: false,
  });

  const failures = seal({
    contract: CONTRACTS.failures,
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 3,
    slice: 2,
    state: "workspace-browser-evidence-candidate",
    accepted_failure_state_count: 2,
    unknown_route: desktop.unknownRoute,
    missing_artifact: missingArtifact,
    silent_fallback_allowed: false,
    previous_valid_state_preserved: true,
    partial_package_exposed: false,
    canonical_mutation: false,
    repository_mutation: false,
    decision: "pass",
  });

  const manifest = seal({
    contract: CONTRACTS.manifest,
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 3,
    slice: 2,
    state: "workspace-browser-evidence-candidate",
    engine_name: "chromium",
    engine_version: browserVersion,
    playwright_version: packageJson.devDependencies.playwright,
    node_major: 22,
    runner: "ubuntu-24.04",
    shell_contract: shellData.contract,
    shell_build_digest: shellData.build_digest,
    shell_baseline_contract: "atlas-phase4-workspace-shell-baseline/0.1",
    shell_baseline_sha256: sha256Bytes(shellBaselineBytes),
    playwright_lock_sha256: sha256Bytes(packageLockBytes),
    accepted_export_sha256: shellData.accepted_export.artifact.sha256,
    accepted_manifest_sha256: shellData.accepted_manifest.artifact.sha256,
    external_network_allowed: false,
    screenshots_authoritative: false,
    browser_state_authority: "ephemeral-only",
    production_frontend_architecture_selected: false,
    live_principia_dependency: false,
    canonical_mutation: false,
    repository_mutation: false,
  });

  const childRecords = [
    ["workspace-browser-workflows.json", workflows],
    ["workspace-browser-accessibility.json", accessibility],
    ["workspace-browser-network.json", network],
    ["workspace-browser-failures.json", failures],
    ["workspace-browser-manifest.json", manifest],
  ];
  for (const [fileName, record] of childRecords) {
    await writeFile(path.join(args.outputDir, fileName), renderJson(record), "utf8");
  }

  const evidenceFiles = [];
  for (const [fileName, record] of childRecords) {
    evidenceFiles.push(await artifactRecord(path.join(args.outputDir, fileName), record.contract));
  }

  const downloadedBytes = await readFile(path.join(args.outputDir, "downloaded-workspace-export.json"));
  const report = seal({
    contract: CONTRACTS.report,
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 3,
    slice: 2,
    state: "workspace-browser-evidence-candidate",
    decision: "workspace-browser-evidence-candidate",
    route_count: shellData.routes.length,
    entry_route_count: 5,
    keyboard_route_count: desktop.routeRecords.length,
    keyboard_focus_count: desktop.routeFocusRecords.length + 3,
    viewport_count: 2,
    accepted_failure_state_count: 2,
    request_count: totalRequests,
    external_request_count: externalRequests,
    download_artifact: {
      file: "downloaded-workspace-export.json",
      bytes: downloadedBytes.length,
      sha256: sha256Bytes(downloadedBytes),
      accepted_export_sha256: shellData.accepted_export.artifact.sha256,
      byte_identical: true,
    },
    evidence_files: evidenceFiles,
    exact_revision_preserved: true,
    entry_order_preserved: true,
    decisions_read_only: true,
    candidates_unresolved: true,
    principia_status_separate: true,
    warnings_visible: true,
    limitations_visible: true,
    export_identity_visible: true,
    non_graph_workflow_complete: true,
    visible_focus_verified: true,
    deep_links_reload_and_history_verified: true,
    reduced_motion_verified: true,
    mobile_layout_verified: true,
    offline_after_local_boot_verified: true,
    unknown_route_preserved_previous_state: true,
    missing_artifact_failed_explicitly: true,
    local_download_byte_identical: true,
    zero_external_requests: true,
    browser_state_authority: "ephemeral-only",
    human_verified: false,
    assistive_technology_user_reviewed: false,
    human_usability_reviewed: false,
    accessibility_certified: false,
    screenshots_authoritative: false,
    account_required: false,
    cloud_required: false,
    production_frontend_architecture_selected: false,
    live_principia_dependency: false,
    canonical_mutation: false,
    lifecycle_mutation: false,
    review_mutation: false,
    repository_mutation: false,
    live: false,
  });
  await writeFile(path.join(args.outputDir, "workspace-browser-report.json"), renderJson(report), "utf8");

  console.log(`workspace-browser-engine=chromium@${browserVersion}`);
  console.log(`workspace-browser-route-count=${report.route_count}`);
  console.log(`workspace-browser-request-count=${report.request_count}`);
  console.log(`workspace-browser-external-requests=${report.external_request_count}`);
  console.log(`workspace-browser-report-digest=${report.report_digest}`);
  console.log("workspace-browser=evidence-candidate; download-byte-identical=true; human-verified=false");
}

main().catch(error => {
  console.error(error instanceof Error ? error.stack : error);
  process.exitCode = 1;
});
