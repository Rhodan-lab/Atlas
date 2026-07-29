import {
  assertEvidence,
  focusEvidence,
  installNetworkPolicy,
  semantics,
  waitReady,
} from "../phase4_workspace_browser/common.mjs";

export async function selectorEvidence(browser, baseUrl, networkRecords) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    serviceWorkers: "block",
    reducedMotion: "no-preference",
  });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();

  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  const initial = await semantics(page);
  const choices = await page.locator("a[data-fixture]").evaluateAll(nodes => nodes.map(node => ({
    fixture: node.dataset.fixture,
    href: node.getAttribute("href"),
    text: node.textContent?.replace(/\s+/g, " ").trim() ?? "",
  })));
  assertEvidence(initial.language === "en", "E-READER-BROWSER-SELECTOR-LANG", "selector language must be English");
  assertEvidence(initial.headings[0]?.level === 1, "E-READER-BROWSER-SELECTOR-HEADING", "selector requires a level-one heading");
  assertEvidence(JSON.stringify(choices.map(item => item.fixture)) === JSON.stringify(["recommender", "catalase"]), "E-READER-BROWSER-SELECTOR-CHOICES", "selector must expose exactly the accepted package order");

  await page.keyboard.press("Tab");
  const skipFocus = await focusEvidence(page);
  assertEvidence(skipFocus.descriptor === "skip-link" && skipFocus.visible, "E-READER-BROWSER-SELECTOR-FOCUS", "selector skip link must receive visible first focus");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.activeElement?.id === "package-selection" && location.hash === "#package-selection");
  const selectionFocus = await focusEvidence(page);
  assertEvidence(selectionFocus.descriptor === "package-selection" && selectionFocus.visible, "E-READER-BROWSER-SELECTOR-FOCUS", "skip link must focus package selection visibly");

  await page.goto(`${baseUrl}/?fixture=catalase`, { waitUntil: "networkidle" });
  await page.waitForFunction(() => document.activeElement?.getAttribute("data-fixture") === "catalase");
  const catalaseFocus = await focusEvidence(page);
  const selectedStatus = await page.locator("#selector-status").innerText();
  assertEvidence(catalaseFocus.descriptor.includes("Catalase assay-methodology package") && catalaseFocus.visible, "E-READER-BROWSER-SELECTOR-KNOWN", "known Catalase selector must focus its accepted link visibly");
  assertEvidence(selectedStatus.includes("Accepted fixture selected: catalase"), "E-READER-BROWSER-SELECTOR-KNOWN", "known selector must expose explicit accepted status");
  await page.keyboard.press("Enter");
  await page.waitForURL(url => url.pathname.endsWith("/packages/catalase/index.html") && url.hash === "#overview");
  await waitReady(page);
  const catalaseActivation = {
    path: new URL(page.url()).pathname,
    hash: new URL(page.url()).hash,
    status: await page.locator("#runtime-status").innerText(),
    outcome: "pass",
  };

  await page.goto(`${baseUrl}/?fixture=unknown-fixture`, { waitUntil: "networkidle" });
  await page.waitForFunction(() => document.querySelector("#selector-error")?.hidden === false);
  const unknownFields = await page.locator("#selector-error dl > div").evaluateAll(nodes => Object.fromEntries(nodes.map(node => [
    node.querySelector("dt")?.textContent?.trim() ?? "",
    node.querySelector("dd")?.textContent?.trim() ?? "",
  ])));
  const unknownStatus = await page.locator("#selector-status").innerText();
  const choicesHidden = await page.locator(".package-list").evaluate(node => node.hidden);
  const unknownUrl = new URL(page.url());
  assertEvidence(unknownFields["Requested fixture"] === "unknown-fixture", "E-READER-BROWSER-SELECTOR-UNKNOWN", "unknown selector must expose requested fixture");
  assertEvidence(unknownFields.Fallback === "refused", "E-READER-BROWSER-SELECTOR-UNKNOWN", "unknown selector must refuse fallback");
  assertEvidence(unknownFields["Package mutation"] === "none", "E-READER-BROWSER-SELECTOR-UNKNOWN", "unknown selector must not mutate packages");
  assertEvidence(choicesHidden && unknownStatus.includes("no fallback package loaded"), "E-READER-BROWSER-SELECTOR-UNKNOWN", "unknown selector must expose failure without package fallback");
  assertEvidence(unknownUrl.pathname === "/" && unknownUrl.searchParams.get("fixture") === "unknown-fixture", "E-READER-BROWSER-SELECTOR-UNKNOWN", "unknown selector must not navigate automatically");

  await context.close();
  return {
    initial_semantics: initial,
    choices,
    skip_focus: skipFocus,
    selection_focus: selectionFocus,
    known_selector: {
      fixture: "catalase",
      focus_visible: catalaseFocus.visible,
      status: selectedStatus,
      activation: catalaseActivation,
      outcome: "pass",
    },
    unknown_selector: {
      requested_fixture: unknownFields["Requested fixture"],
      fallback: unknownFields.Fallback,
      package_mutation: unknownFields["Package mutation"],
      choices_hidden: choicesHidden,
      status: unknownStatus,
      navigation_preserved: true,
      outcome: "rejected-preserved",
    },
  };
}

export async function recommenderRegression(browser, baseUrl, recommenderShell, recommenderExport, networkRecords) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, serviceWorkers: "block" });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();
  await page.goto(`${baseUrl}/packages/recommender/index.html#overview`, { waitUntil: "networkidle" });
  await waitReady(page);
  const observed = await page.evaluate(() => ({
    hash: location.hash,
    route_count: document.querySelectorAll("a[data-route-id]").length,
    status: document.querySelector("#runtime-status")?.textContent ?? null,
    heading: document.querySelector("#active-view-title")?.textContent?.trim() ?? null,
  }));
  assertEvidence(observed.hash === "#overview" && observed.route_count === 13, "E-READER-BROWSER-REGRESSION", "accepted recommender route baseline must render unchanged");
  assertEvidence(observed.status === "Accepted workspace verified", "E-READER-BROWSER-REGRESSION", "recommender package must verify accepted workspace");
  assertEvidence(recommenderShell.workspace.id === recommenderExport.workspace.id, "E-READER-BROWSER-REGRESSION", "recommender package identities must remain aligned");
  await context.close();
  return {
    workspace: recommenderShell.workspace,
    accepted_export_digest: recommenderExport.report_digest,
    ...observed,
    outcome: "pass",
  };
}
