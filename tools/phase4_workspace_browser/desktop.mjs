import { assertEvidence, currentView, focusEvidence, installNetworkPolicy, openRoute, readDownload, routeHash, semantics, sha256, waitReady } from "./common.mjs";

export async function desktopEvidence(browser, baseUrl, shellData, workspaceExport, expectedExportBytes, networkRecords) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    serviceWorkers: "block",
    reducedMotion: "no-preference",
    acceptDownloads: true,
  });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await waitReady(page);

  const initialSemantics = await semantics(page);
  assertEvidence(initialSemantics.language === "en", "E-WS-BROWSER-LANG", "document language must be English");
  assertEvidence(Object.values(initialSemantics.landmarks).every(value => value === 1), "E-WS-BROWSER-LANDMARK", "one of each primary landmark is required");
  assertEvidence(initialSemantics.headings[0]?.level === 1, "E-WS-BROWSER-HEADING", "first heading must be level one");
  assertEvidence(initialSemantics.named_buttons, "E-WS-BROWSER-LABEL", "every button needs an accessible name");
  assertEvidence(initialSemantics.live_regions >= 2 && initialSemantics.alert_regions === 1, "E-WS-BROWSER-LIVE", "status and alert regions are required");

  await page.keyboard.press("Tab");
  const skipFocus = await focusEvidence(page);
  assertEvidence(skipFocus.descriptor === "skip-link" && skipFocus.visible, "E-WS-BROWSER-SKIP", "first focus must be the visible skip link");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.activeElement?.id === "main-content");
  const mainFocus = await focusEvidence(page);
  assertEvidence(mainFocus.descriptor === "main-content" && mainFocus.visible, "E-WS-BROWSER-SKIP", "skip link must visibly focus main content");

  await page.reload({ waitUntil: "networkidle" });
  await waitReady(page);
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");

  const routeOrder = shellData.routes.map(item => item.id);
  const domRouteOrder = await page.locator("a[data-route-id]").evaluateAll(nodes => nodes.map(node => node.dataset.routeId));
  assertEvidence(JSON.stringify(routeOrder) === JSON.stringify(domRouteOrder), "E-WS-BROWSER-ORDER", "navigation must preserve accepted route order");

  const routeRecords = [];
  for (const route of shellData.routes) {
    const focus = await focusEvidence(page);
    assertEvidence(focus.descriptor === route.id, "E-WS-BROWSER-FOCUS-ORDER", `expected ${route.id}, observed ${focus.descriptor}`);
    assertEvidence(focus.visible, "E-WS-BROWSER-FOCUS", `focus must be visible for ${route.id}`);
    await page.keyboard.press("Enter");
    await page.waitForFunction(expected => location.hash === expected, route.hash);
    await page.waitForFunction(expected => document.querySelector(`a[data-route-id="${expected}"]`)?.getAttribute("aria-current") === "page", route.id);
    const observed = await currentView(page);
    assertEvidence(observed.current_route === route.id, "E-WS-BROWSER-ROUTE", `route ${route.id} must be current`);
    assertEvidence(observed.error_hidden === true, "E-WS-BROWSER-ROUTE", `route ${route.id} must not expose an error`);
    let exactReference = null;
    let decision = null;
    if (route.kind === "entry") {
      const source = workspaceExport.entries.find(item => item.entry_id === route.entry_id);
      exactReference = `${source.exact_reference.id}@${source.exact_reference.revision}`;
      decision = source.decision.action;
      const text = await page.locator("#content-panel").innerText();
      assertEvidence(text.includes(exactReference), "E-WS-BROWSER-REVISION", `entry ${route.id} must expose its exact revision`);
      assertEvidence(text.toLowerCase().includes(decision), "E-WS-BROWSER-DECISION", `entry ${route.id} must expose its read-only decision`);
    }
    routeRecords.push({
      route_id: route.id,
      kind: route.kind,
      observed_hash: observed.hash,
      heading: observed.heading,
      focus_visible: focus.visible,
      exact_reference: exactReference,
      decision,
      decision_read_only: true,
      non_graph_available: true,
      outcome: "pass",
    });
    await page.keyboard.press("Tab");
  }

  const candidates = await openRoute(page, "candidates");
  const candidateText = (await page.locator("#content-panel").innerText()).toLowerCase();
  assertEvidence(candidateText.includes("unresolved") && candidateText.includes("automatic resolution") && candidateText.includes("blocked"), "E-WS-BROWSER-CANDIDATE", "candidate route must preserve unresolved non-automatic status");
  const principia = await openRoute(page, "principia");
  const principiaText = (await page.locator("#content-panel").innerText()).toLowerCase();
  assertEvidence(principiaText.includes("draft") && principiaText.includes("status separate") && principiaText.includes("yes"), "E-WS-BROWSER-PRINCIPIA", "Principia status must remain separate");
  const warning = await openRoute(page, "warnings");
  const warningText = (await page.locator("#content-panel").innerText()).toLowerCase();
  assertEvidence(warningText.includes("automatic update") && warningText.includes("blocked"), "E-WS-BROWSER-WARNING", "warning route must refuse automatic updates");
  await openRoute(page, "summary");
  const textSummary = await page.locator("#content-panel").innerText();
  for (const entry of workspaceExport.entries) assertEvidence(textSummary.includes(entry.visible_metadata.title), "E-WS-BROWSER-NON-GRAPH", `text route must cover ${entry.entry_id}`);
  for (const candidate of workspaceExport.candidate_references) assertEvidence(textSummary.includes(candidate.id), "E-WS-BROWSER-NON-GRAPH", `text route must cover ${candidate.id}`);

  const historyPage = await context.newPage();
  await historyPage.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await waitReady(historyPage);
  const historyRoutes = routeOrder.slice(1, 4);
  for (const routeId of historyRoutes) await openRoute(historyPage, routeId);
  const beforeBack = (await currentView(historyPage)).hash;
  await historyPage.goBack();
  await historyPage.waitForFunction(expected => location.hash === expected, routeHash(historyRoutes[1]));
  const afterBack = (await currentView(historyPage)).hash;
  await historyPage.goForward();
  await historyPage.waitForFunction(expected => location.hash === expected, routeHash(historyRoutes[2]));
  const afterForward = (await currentView(historyPage)).hash;
  assertEvidence(beforeBack === afterForward && afterBack === routeHash(historyRoutes[1]), "E-WS-BROWSER-HISTORY", "back and forward must restore exact routes");

  const directRoute = routeOrder[3];
  const directPage = await context.newPage();
  await directPage.goto(`${baseUrl}/${routeHash(directRoute)}`, { waitUntil: "networkidle" });
  await waitReady(directPage);
  const directBefore = await currentView(directPage);
  await directPage.reload({ waitUntil: "networkidle" });
  await waitReady(directPage);
  const directAfter = await currentView(directPage);
  assertEvidence(directBefore.hash === directAfter.hash && directAfter.current_route === directRoute, "E-WS-BROWSER-DEEP-LINK", "reload must preserve exact route");

  await openRoute(page, "overview");
  await page.evaluate(() => { location.hash = "#unknown-workspace-route"; });
  await page.waitForFunction(() => document.querySelector("#error-panel")?.hidden === false);
  const invalidView = await currentView(page);
  const invalidText = await page.locator("#error-panel").innerText();
  const recoveryHref = await page.locator("#error-panel a.route-link").getAttribute("href");
  assertEvidence(invalidView.heading === "Workspace route unavailable", "E-WS-BROWSER-FAILURE-PRESERVE", "unknown route must show an explicit failure view");
  assertEvidence(invalidText.includes("Fallback") && invalidText.includes("refused") && invalidText.includes("Previous valid route"), "E-WS-BROWSER-FAILURE-PRESERVE", "unknown route must refuse fallback and record the prior route");
  assertEvidence(recoveryHref === "#overview", "E-WS-BROWSER-FAILURE-PRESERVE", "unknown route must provide deterministic recovery to the previous valid route");

  await openRoute(page, "evidence");
  const downloadPromise = page.waitForEvent("download");
  await page.locator("#download-export").click();
  const download = await downloadPromise;
  const downloaded = await readDownload(download);
  assertEvidence(download.suggestedFilename() === "workspace-export.json", "E-WS-BROWSER-DOWNLOAD", "download filename must be deterministic");
  assertEvidence(Buffer.compare(downloaded, expectedExportBytes) === 0, "E-WS-BROWSER-DOWNLOAD", "download must be byte-identical to accepted export");

  await context.close();
  return {
    initialSemantics,
    skipFocus,
    mainFocus,
    routeOrder,
    routeRecords,
    candidates_heading: candidates.heading,
    principia_heading: principia.heading,
    warning_heading: warning.heading,
    history: { routes: historyRoutes, before_back: beforeBack, after_back: afterBack, after_forward: afterForward, outcome: "pass" },
    deep_link: { route_id: directRoute, before_reload: directBefore.hash, after_reload: directAfter.hash, outcome: "pass" },
    unknown_route: { attempted: "#unknown-workspace-route", failure_heading: invalidView.heading, previous_valid_route: "#overview", recovery_href: recoveryHref, fallback_refused: true, status: invalidView.status, outcome: "rejected-preserved" },
    download: {
      filename: download.suggestedFilename(),
      bytes: downloaded.length,
      sha256: sha256(downloaded),
      accepted_bytes: expectedExportBytes.length,
      accepted_sha256: sha256(expectedExportBytes),
      byte_identical: Buffer.compare(downloaded, expectedExportBytes) === 0,
      network_required: false,
      repository_mutation: false,
      outcome: "pass",
    },
  };
}
