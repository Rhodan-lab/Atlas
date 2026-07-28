import { chromium } from "playwright";
import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const PACKAGE_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_REPO_ROOT = path.resolve(PACKAGE_DIR, "../..");

function parseArgs(argv) {
  const result = {
    baseUrl: "http://127.0.0.1:8766",
    repoRoot: DEFAULT_REPO_ROOT,
    shellDir: path.join(DEFAULT_REPO_ROOT, "phase4-browser-shell"),
    outputDir: path.join(DEFAULT_REPO_ROOT, "phase4-browser-evidence"),
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

function exactKey(record) {
  return `${record.id}@${record.revision}`;
}

function normalizeUrl(raw, baseUrl) {
  const parsed = new URL(raw);
  const base = new URL(baseUrl);
  if (parsed.origin === base.origin) return `${parsed.pathname}${parsed.search}${parsed.hash}`;
  return `${parsed.protocol}//${parsed.hostname}${parsed.port ? `:${parsed.port}` : ""}${parsed.pathname}${parsed.search}`;
}

function semanticRequest(request, baseUrl, decision) {
  return {
    decision,
    method: request.method(),
    resource_type: request.resourceType(),
    url: normalizeUrl(request.url(), baseUrl),
  };
}

async function installNetworkPolicy(context, baseUrl, records) {
  const allowedOrigin = new URL(baseUrl).origin;
  await context.route("**/*", async route => {
    const request = route.request();
    const parsed = new URL(request.url());
    const allowed = parsed.origin === allowedOrigin;
    records.push(semanticRequest(request, baseUrl, allowed ? "allowed-loopback" : "blocked-external"));
    if (allowed) await route.continue();
    else await route.abort("blockedbyclient");
  });
}

async function waitUntilReady(page) {
  await page.waitForFunction(() => document.querySelector("#runtime-status")?.textContent === "Local fixture ready");
}

async function focusEvidence(page) {
  return page.evaluate(() => {
    const active = document.activeElement;
    if (!(active instanceof HTMLElement)) return { descriptor: "none", visible: false };
    let descriptor = active.id || active.dataset.key || active.getAttribute("aria-label") || active.textContent?.trim() || active.tagName.toLowerCase();
    if (active.classList.contains("skip-link")) descriptor = "skip-link";
    const style = getComputedStyle(active);
    const outlineVisible = style.outlineStyle !== "none" && parseFloat(style.outlineWidth || "0") > 0;
    const shadowVisible = style.boxShadow !== "none";
    return {
      descriptor: String(descriptor).replace(/\s+/g, " ").trim(),
      tag: active.tagName.toLowerCase(),
      visible: active.matches(":focus-visible") && (outlineVisible || shadowVisible),
    };
  });
}

async function activeView(page) {
  return page.evaluate(() => {
    const current = document.querySelector('button[aria-current="page"]');
    const heading = document.querySelector("#view-panel:not([hidden]) h2, #failure-panel:not([hidden]) h2, #error-panel:not([hidden]) h2");
    return {
      current_key: current?.dataset.key ?? (current?.id === "failure-button" ? "failures" : null),
      heading: heading?.textContent?.trim() ?? null,
      hash: location.hash,
      title: document.title,
    };
  });
}

async function inspectSemantics(page) {
  return page.evaluate(() => {
    const headings = [...document.querySelectorAll("h1, h2, h3, h4, h5, h6")].map(element => ({
      level: Number(element.tagName.slice(1)),
      text: element.textContent?.replace(/\s+/g, " ").trim() ?? "",
    }));
    const buttons = [...document.querySelectorAll("button")].map(button => ({
      name: button.getAttribute("aria-label") || button.textContent?.replace(/\s+/g, " ").trim() || "",
      type: button.getAttribute("type") || "submit",
    }));
    const landmarks = {
      banner: document.querySelectorAll("header").length,
      navigation: document.querySelectorAll("nav").length,
      main: document.querySelectorAll("main").length,
      contentinfo: document.querySelectorAll("footer").length,
    };
    return {
      document_language: document.documentElement.lang,
      document_title: document.title,
      headings,
      buttons,
      landmarks,
      live_regions: document.querySelectorAll('[aria-live="polite"], [aria-live="assertive"], [role="status"], [role="alert"]').length,
      alert_regions: document.querySelectorAll('[role="alert"]').length,
      main_labelled: Boolean(document.querySelector("main")?.getAttribute("aria-label") || document.querySelector("main")?.getAttribute("aria-labelledby")),
    };
  });
}

async function openView(page, key) {
  const button = page.locator(`button[data-key="${key}"]`);
  await button.click();
  await page.waitForFunction(expected => document.querySelector(`button[data-key="${expected}"]`)?.getAttribute("aria-current") === "page", key);
  return activeView(page);
}

async function runDesktopEvidence(browser, baseUrl, shellData, networkRecords) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    serviceWorkers: "block",
    reducedMotion: "no-preference",
  });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await waitUntilReady(page);

  const initialSemantics = await inspectSemantics(page);
  assertEvidence(initialSemantics.document_language === "en", "E-BROWSER-LANG", "document language must be English");
  assertEvidence(initialSemantics.landmarks.banner === 1, "E-BROWSER-LANDMARK", "one banner landmark is required");
  assertEvidence(initialSemantics.landmarks.navigation === 1, "E-BROWSER-LANDMARK", "one navigation landmark is required");
  assertEvidence(initialSemantics.landmarks.main === 1, "E-BROWSER-LANDMARK", "one main landmark is required");
  assertEvidence(initialSemantics.landmarks.contentinfo === 1, "E-BROWSER-LANDMARK", "one contentinfo landmark is required");
  assertEvidence(initialSemantics.headings[0]?.level === 1, "E-BROWSER-HEADING", "the first heading must be level one");
  assertEvidence(initialSemantics.buttons.every(button => button.name), "E-BROWSER-LABEL", "every button requires an accessible name");

  await page.keyboard.press("Tab");
  const skipLinkFocus = await focusEvidence(page);
  assertEvidence(skipLinkFocus.descriptor === "skip-link", "E-BROWSER-SKIP-LINK", "first keyboard focus must reveal the skip link");
  assertEvidence(skipLinkFocus.visible, "E-BROWSER-FOCUS", "skip-link focus must be visible");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.activeElement?.id === "main-content");
  const mainFocus = await focusEvidence(page);
  assertEvidence(mainFocus.descriptor === "main-content", "E-BROWSER-SKIP-LINK", "skip link must focus main content");
  assertEvidence(mainFocus.visible, "E-BROWSER-FOCUS", "main-content focus must be visible after skip navigation");

  await page.reload({ waitUntil: "networkidle" });
  await waitUntilReady(page);
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");

  const expectedKeys = shellData.views.map(exactKey);
  const focusSequence = [];
  const workflowRecords = [];
  for (const view of shellData.views) {
    const focus = await focusEvidence(page);
    const key = exactKey(view);
    assertEvidence(focus.descriptor === key, "E-BROWSER-FOCUS-ORDER", `expected focus on ${key}, observed ${focus.descriptor}`);
    assertEvidence(focus.visible, "E-BROWSER-FOCUS", `focus must be visible for ${key}`);
    focusSequence.push(focus);
    await page.keyboard.press("Enter");
    await page.waitForFunction(expected => document.querySelector(`button[data-key="${expected}"]`)?.getAttribute("aria-current") === "page", key);
    const observed = await activeView(page);
    const refs = await page.locator("#view-panel .reference-item").count();
    const nonGraphHeading = await page.getByRole("heading", { name: "Equivalent non-graph path" }).count();
    assertEvidence(observed.hash === `#view=${encodeURIComponent(key)}`, "E-BROWSER-ROUTE", `route mismatch for ${key}`);
    assertEvidence(nonGraphHeading === 1, "E-BROWSER-NON-GRAPH", `non-graph path missing for ${key}`);
    workflowRecords.push({
      contract: "atlas-browser-workflow-evidence/0.1",
      workflow_id: key,
      workflow_revision: view.revision,
      view_kind: view.kind,
      input_sequence: ["keyboard-enter"],
      focus_descriptor: focus.descriptor,
      focus_visible: focus.visible,
      expected_hash: `#view=${encodeURIComponent(key)}`,
      observed_hash: observed.hash,
      observed_heading: observed.heading,
      exact_reference_count: refs,
      non_graph_route_exercised: true,
      decision: "pass",
    });
    await page.keyboard.press("Tab");
  }

  const failureFocus = await focusEvidence(page);
  assertEvidence(failureFocus.descriptor === "failure-button", "E-BROWSER-FOCUS-ORDER", "failure button must follow the eight workflow controls");
  assertEvidence(failureFocus.visible, "E-BROWSER-FOCUS", "failure button focus must be visible");
  focusSequence.push(failureFocus);
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => (
    location.hash === "#failures"
    && document.querySelector("#failure-panel")?.hidden === false
    && document.querySelectorAll("#failure-panel .failure-item code").length === 5
  ));
  const failureCodes = await page.locator("#failure-panel .failure-item code").allTextContents();
  assertEvidence(failureCodes.length === 5, "E-BROWSER-FAILURES", "all five accepted failure states must be visible");

  const historyPage = await context.newPage();
  await historyPage.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await waitUntilReady(historyPage);
  const historyKeys = expectedKeys.slice(1, 4);
  for (const key of historyKeys) await openView(historyPage, key);
  const routeBeforeBack = (await activeView(historyPage)).hash;
  await historyPage.goBack();
  await historyPage.waitForFunction(expected => location.hash === expected, `#view=${encodeURIComponent(historyKeys[1])}`);
  const routeAfterBack = (await activeView(historyPage)).hash;
  await historyPage.goForward();
  await historyPage.waitForFunction(expected => location.hash === expected, `#view=${encodeURIComponent(historyKeys[2])}`);
  const routeAfterForward = (await activeView(historyPage)).hash;
  assertEvidence(routeBeforeBack === routeAfterForward, "E-BROWSER-HISTORY", "forward navigation must restore the exact route");

  const directKey = expectedKeys.at(-1);
  const directPage = await context.newPage();
  await directPage.goto(`${baseUrl}/#view=${encodeURIComponent(directKey)}`, { waitUntil: "networkidle" });
  await waitUntilReady(directPage);
  const directBeforeReload = await activeView(directPage);
  await directPage.reload({ waitUntil: "networkidle" });
  await waitUntilReady(directPage);
  const directAfterReload = await activeView(directPage);
  assertEvidence(directBeforeReload.hash === directAfterReload.hash, "E-BROWSER-DEEP-LINK", "reload must preserve the exact route");

  const invalidKey = "model:en:delayed-correction-recurrence@latest";
  await directPage.goto(`${baseUrl}/#view=${encodeURIComponent(invalidKey)}`, { waitUntil: "networkidle" });
  await waitUntilReady(directPage);
  await directPage.locator("#error-panel:not([hidden])").waitFor();
  const invalidRoute = await activeView(directPage);
  const invalidText = await directPage.locator("#error-panel").innerText();
  assertEvidence(invalidRoute.heading === "Exact view route unavailable", "E-BROWSER-ROUTE-FAILURE", "unknown routes must show an explicit failure");
  assertEvidence(invalidText.includes("No fallback"), "E-BROWSER-ROUTE-FAILURE", "unknown routes must refuse silent fallback");

  const impactView = shellData.views.find(view => view.kind === "impact-warning");
  const principiaView = shellData.views.find(view => view.kind === "principia-reference");
  assertEvidence(Boolean(impactView && principiaView), "E-BROWSER-WORKFLOW", "impact and Principia workflows are required");
  await directPage.goto(`${baseUrl}/#view=${encodeURIComponent(exactKey(impactView))}`, { waitUntil: "networkidle" });
  await waitUntilReady(directPage);
  const impactText = await directPage.locator("#view-panel").innerText();
  assertEvidence(impactText.includes("No automatic update"), "E-BROWSER-WARNING", "impact warning must state that no automatic update occurs");
  await openView(directPage, exactKey(principiaView));
  const principiaText = await directPage.locator("#view-panel").innerText();
  assertEvidence(principiaText.includes("Principia status"), "E-BROWSER-PRINCIPIA", "Principia status must remain visible and separate");

  await context.setOffline(true);
  await directPage.evaluate(key => { location.hash = `view=${encodeURIComponent(key)}`; }, expectedKeys[0]);
  await directPage.waitForFunction(expected => document.querySelector(`button[data-key="${expected}"]`)?.getAttribute("aria-current") === "page", expectedKeys[0]);
  const offlineRoute = await activeView(directPage);
  await context.setOffline(false);

  const desktopOverflow = await page.evaluate(() => ({
    client_width: document.documentElement.clientWidth,
    scroll_width: document.documentElement.scrollWidth,
    passes: document.documentElement.scrollWidth <= document.documentElement.clientWidth,
  }));
  assertEvidence(desktopOverflow.passes, "E-BROWSER-OVERFLOW", "desktop viewport must not overflow horizontally");

  await context.close();
  return {
    accessibility: {
      initial_semantics: initialSemantics,
      skip_link_focus: skipLinkFocus,
      main_focus: mainFocus,
      focus_sequence: focusSequence,
      desktop_overflow: desktopOverflow,
    },
    workflows: workflowRecords,
    history: {
      sequence: historyKeys.map(key => `#view=${encodeURIComponent(key)}`),
      route_before_back: routeBeforeBack,
      route_after_back: routeAfterBack,
      route_after_forward: routeAfterForward,
      decision: "pass",
    },
    deep_link: {
      exact_key: directKey,
      before_reload: directBeforeReload.hash,
      after_reload: directAfterReload.hash,
      invalid_key: invalidKey,
      invalid_heading: invalidRoute.heading,
      decision: "pass",
    },
    failures: {
      accepted_failure_codes: failureCodes,
      unknown_route_explicit: true,
      silent_fallback: false,
      decision: "pass",
    },
    offline: {
      mode: "browser-context-offline-after-local-boot",
      observed_hash: offlineRoute.hash,
      decision: "pass",
    },
  };
}

async function runMobileEvidence(browser, baseUrl, networkRecords) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    serviceWorkers: "block",
    reducedMotion: "reduce",
  });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await waitUntilReady(page);
  await page.keyboard.press("Tab");
  const skipFocus = await focusEvidence(page);
  assertEvidence(skipFocus.descriptor === "skip-link" && skipFocus.visible, "E-BROWSER-MOBILE-FOCUS", "mobile skip-link focus must be visible");
  const responsive = await page.evaluate(() => ({
    client_width: document.documentElement.clientWidth,
    scroll_width: document.documentElement.scrollWidth,
    horizontal_overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    scroll_behavior: getComputedStyle(document.documentElement).scrollBehavior,
    visible_view_controls: [...document.querySelectorAll("#view-list button")].filter(button => {
      const rect = button.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    }).length,
  }));
  assertEvidence(!responsive.horizontal_overflow, "E-BROWSER-MOBILE-OVERFLOW", "mobile viewport must not overflow horizontally");
  assertEvidence(responsive.visible_view_controls === 8, "E-BROWSER-MOBILE-CONTROLS", "all view controls must remain available on mobile");
  assertEvidence(responsive.scroll_behavior === "auto", "E-BROWSER-REDUCED-MOTION", "reduced-motion mode must disable smooth scrolling");
  await context.close();
  return { viewport: { width: 390, height: 844 }, skip_link_focus: skipFocus, responsive, decision: "pass" };
}

async function writeContract(outputDir, fileName, record) {
  const sealed = seal(record);
  const rendered = renderJson(sealed);
  const filePath = path.join(outputDir, fileName);
  await writeFile(filePath, rendered, "utf8");
  return {
    file: fileName,
    bytes: Buffer.byteLength(rendered),
    sha256: sha256Bytes(Buffer.from(rendered)),
    report_digest: sealed.report_digest,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  await mkdir(args.outputDir, { recursive: true });
  const shellDataPath = path.join(args.shellDir, "data", "reference-shell-data.json");
  const shellData = await readJson(shellDataPath);
  const interactionBaseline = await readJson(path.join(args.repoRoot, "content", "fixtures", "phase4_interaction", "interaction-contract-baseline.json"));
  const shellBaseline = await readJson(path.join(args.repoRoot, "content", "fixtures", "phase4_interaction", "reference-shell-baseline.json"));
  const completionBaseline = await readJson(path.join(args.repoRoot, "content", "fixtures", "phase4_interaction", "workstream1-completion-baseline.json"));
  const packageRecord = await readJson(path.join(PACKAGE_DIR, "node_modules", "playwright", "package.json"));

  assertEvidence(shellData.contract === "atlas-reference-shell-data/0.1", "E-BROWSER-SHELL-DATA", "unsupported shell data contract");
  assertEvidence(shellData.build_digest === shellBaseline.shell_data.build_digest, "E-BROWSER-SHELL-DATA", "shell build digest differs from accepted baseline");

  const browser = await chromium.launch({ headless: true });
  const engineVersion = browser.version();
  const networkRecords = [];
  let desktop;
  let mobile;
  try {
    desktop = await runDesktopEvidence(browser, args.baseUrl, shellData, networkRecords);
    mobile = await runMobileEvidence(browser, args.baseUrl, networkRecords);
  } finally {
    await browser.close();
  }

  const normalizedRequests = [...new Map(
    networkRecords
      .map(record => [JSON.stringify(stableValue(record)), stableValue(record)])
      .sort(([left], [right]) => left.localeCompare(right)),
  ).values()];
  const externalRequests = normalizedRequests.filter(record => record.decision === "blocked-external");
  assertEvidence(externalRequests.length === 0, "E-BROWSER-NETWORK", "the accepted shell must not attempt an external request");

  const manifest = {
    contract: "atlas-phase4-browser-evidence-manifest/0.1",
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 2,
    state: "browser-evidence-candidate",
    engine_name: "chromium",
    engine_version: engineVersion,
    engine_source: `playwright@${packageRecord.version}`,
    playwright_version: packageRecord.version,
    operating_system: "ubuntu-24.04",
    node_major_version: 22,
    viewport_matrix: [
      { id: "desktop", width: 1440, height: 1000, reduced_motion: "no-preference" },
      { id: "mobile", width: 390, height: 844, reduced_motion: "reduce" },
    ],
    shell_baseline_sha256: sha256Bytes(Buffer.from(renderJson(shellBaseline))),
    shell_build_digest: shellData.build_digest,
    interaction_report_digest: interactionBaseline.report_digest,
    workstream1_completion_digest: completionBaseline.report_digest,
    workflow_fixture_revision: 1,
    network_policy_revision: 1,
    accessibility_policy_revision: 1,
    external_network_allowed: false,
    screenshots_authoritative: false,
    human_verified: false,
    accessibility_certified: false,
    assistive_technology_user_reviewed: false,
    live: false,
    repository_mutation: false,
  };

  const workflowEvidence = {
    contract: "atlas-browser-workflow-evidence/0.1",
    mode: "interactive-experience-foundation",
    workflow_count: desktop.workflows.length,
    workflows: desktop.workflows,
    history: desktop.history,
    deep_link: desktop.deep_link,
    offline: desktop.offline,
    non_graph_workflow_equivalence: true,
    exact_revision_required: true,
    implicit_latest_allowed: false,
    decision: "pass",
    live: false,
    repository_mutation: false,
  };

  const accessibilityEvidence = {
    contract: "atlas-browser-accessibility-report/0.1",
    mode: "interactive-experience-foundation",
    desktop: desktop.accessibility,
    mobile,
    keyboard_workflow_count: desktop.workflows.length + 1,
    visible_focus_required: true,
    skip_link_operational: true,
    landmarks_recorded: true,
    headings_recorded: true,
    labels_recorded: true,
    live_regions_recorded: true,
    non_graph_routes_required: true,
    reduced_motion_checked: true,
    human_verified: false,
    accessibility_certified: false,
    assistive_technology_user_reviewed: false,
    decision: "pass-bounded-automated-evidence",
    live: false,
    repository_mutation: false,
  };

  const networkEvidence = {
    contract: "atlas-browser-network-report/0.1",
    mode: "interactive-experience-foundation",
    loopback_origin: new URL(args.baseUrl).origin,
    request_count: normalizedRequests.length,
    loopback_request_count: normalizedRequests.filter(record => record.decision === "allowed-loopback").length,
    external_request_count: externalRequests.length,
    blocked_external_request_count: externalRequests.length,
    request_records: normalizedRequests,
    credentials_used: false,
    remote_assets_used: false,
    analytics_used: false,
    cloud_service_used: false,
    decision: "pass-zero-external-requests",
    live: false,
    repository_mutation: false,
  };

  const failureEvidence = {
    contract: "atlas-browser-failure-evidence/0.1",
    mode: "interactive-experience-foundation",
    accepted_failure_state_count: desktop.failures.accepted_failure_codes.length,
    accepted_failure_codes: desktop.failures.accepted_failure_codes,
    unknown_route_explicit: desktop.failures.unknown_route_explicit,
    silent_fallback: desktop.failures.silent_fallback,
    implicit_latest_rejected: true,
    previous_valid_state_preserved_by_contract: true,
    canonical_mutation: false,
    lifecycle_mutation: false,
    decision: "pass",
    live: false,
    repository_mutation: false,
  };

  const files = [];
  files.push(await writeContract(args.outputDir, "browser-manifest.json", manifest));
  files.push(await writeContract(args.outputDir, "browser-workflows.json", workflowEvidence));
  files.push(await writeContract(args.outputDir, "browser-accessibility.json", accessibilityEvidence));
  files.push(await writeContract(args.outputDir, "browser-network.json", networkEvidence));
  files.push(await writeContract(args.outputDir, "browser-failures.json", failureEvidence));

  const report = {
    contract: "atlas-phase4-browser-evidence-report/0.1",
    mode: "interactive-experience-foundation",
    phase: 4,
    workstream: 2,
    state: "browser-evidence-candidate",
    decision: "browser-evidence-candidate",
    manifest_digest: files[0].report_digest,
    evidence_files: files,
    workflow_count: desktop.workflows.length,
    keyboard_workflow_count: desktop.workflows.length + 1,
    accepted_failure_state_count: desktop.failures.accepted_failure_codes.length,
    viewport_count: 2,
    external_request_count: 0,
    exact_revision_preserved: true,
    principia_status_separate: true,
    non_graph_workflow_equivalence: true,
    visible_focus_verified: true,
    reduced_motion_verified: true,
    offline_after_local_boot_verified: true,
    production_frontend_architecture_selected: false,
    live_principia_dependency: false,
    canonical_mutation: false,
    automatic_status_change: false,
    automatic_release_action: false,
    human_verified: false,
    accessibility_certified: false,
    live: false,
    repository_mutation: false,
  };
  const reportFile = await writeContract(args.outputDir, "browser-evidence-report.json", report);
  console.log(`phase4-browser-engine=${manifest.engine_name}@${manifest.engine_version}`);
  console.log(`phase4-browser-workflows=${report.workflow_count}`);
  console.log(`phase4-browser-external-requests=${report.external_request_count}`);
  console.log(`phase4-browser-report-sha256=${reportFile.sha256}`);
  console.log(`phase4-browser-report-digest=${reportFile.report_digest}`);
}

main().catch(error => {
  console.error(error instanceof Error ? error.stack : String(error));
  process.exitCode = 1;
});
