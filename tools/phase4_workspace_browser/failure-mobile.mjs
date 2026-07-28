import { assertEvidence, currentView, installNetworkPolicy, openRoute, waitReady } from "./common.mjs";

export async function mobileEvidence(browser, baseUrl, networkRecords) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, serviceWorkers: "block", reducedMotion: "reduce" });
  await installNetworkPolicy(context, baseUrl, networkRecords);
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  await waitReady(page);
  const result = await page.evaluate(() => ({
    width: innerWidth,
    height: innerHeight,
    scroll_width: document.documentElement.scrollWidth,
    reduced_motion: matchMedia("(prefers-reduced-motion: reduce)").matches,
    nav_buttons: document.querySelectorAll("a[data-route-id]").length,
  }));
  assertEvidence(result.width === 390 && result.height === 844, "E-WS-BROWSER-MOBILE", "mobile viewport must be pinned");
  assertEvidence(result.scroll_width <= result.width, "E-WS-BROWSER-MOBILE", "mobile view must not overflow horizontally");
  assertEvidence(result.reduced_motion, "E-WS-BROWSER-MOTION", "reduced motion preference must be honored");
  assertEvidence(result.nav_buttons === 13, "E-WS-BROWSER-MOBILE", "all routes must remain available on mobile");
  await openRoute(page, "summary");
  const textHeading = (await currentView(page)).heading;
  await context.close();
  return { ...result, text_heading: textHeading, outcome: "pass" };
}

export async function missingArtifactEvidence(browser, baseUrl, networkRecords) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, serviceWorkers: "block" });
  await installNetworkPolicy(context, baseUrl, networkRecords, new Set(["/data/workspace-export.json"]));
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => document.querySelector("#runtime-status")?.textContent === "Workspace package unavailable");
  const observed = await currentView(page);
  const errorText = await page.locator("#error-panel").innerText();
  assertEvidence(observed.heading === "The accepted workspace could not be verified", "E-WS-BROWSER-MISSING", "missing accepted export must show explicit failure");
  assertEvidence(errorText.includes("No fallback data was loaded") && errorText.includes("no workspace state was changed"), "E-WS-BROWSER-MISSING", "missing artifact failure must reject substitution and persistence");
  await context.close();
  return {
    blocked_path: "/data/workspace-export.json",
    heading: observed.heading,
    status: observed.status,
    error_visible: observed.error_hidden === false,
    fallback_used: false,
    persisted: false,
    outcome: "rejected-preserved",
  };
}
