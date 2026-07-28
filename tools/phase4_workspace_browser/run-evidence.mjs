import { chromium } from "playwright";
import { readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { assertEvidence, parseArgs, readJson, setRoutes, sha256 } from "./common.mjs";
import { desktopEvidence } from "./desktop.mjs";
import { mobileEvidence, missingArtifactEvidence } from "./failure-mobile.mjs";
import { writeEvidence } from "./emit.mjs";

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const shellData = await readJson(path.join(args.shellDir, "data", "workspace-shell-data.json"));
  setRoutes(shellData.routes);
  const workspaceExport = await readJson(path.join(args.shellDir, "data", "workspace-export.json"));
  const workspaceManifest = await readJson(path.join(args.shellDir, "data", "workspace-manifest.json"));
  const expectedExportBytes = await readFile(path.join(args.shellDir, "data", "workspace-export.json"));
  assertEvidence(shellData.accepted_export.artifact.sha256 === sha256(expectedExportBytes), "E-WS-BROWSER-INPUT", "shell accepted export identity must match package bytes");
  assertEvidence(workspaceExport.report_digest === shellData.accepted_export.report_digest, "E-WS-BROWSER-INPUT", "accepted export digest must match shell data");
  assertEvidence(workspaceManifest.report_digest === shellData.accepted_manifest.report_digest, "E-WS-BROWSER-INPUT", "accepted manifest digest must match shell data");

  const browser = await chromium.launch({ headless: true });
  const networkRecords = [];
  try {
    const desktop = await desktopEvidence(browser, args.baseUrl, shellData, workspaceExport, expectedExportBytes, networkRecords);
    const mobile = await mobileEvidence(browser, args.baseUrl, networkRecords);
    const missingArtifact = await missingArtifactEvidence(browser, args.baseUrl, networkRecords);
    const evidence = await writeEvidence(args.outputDir, browser, args, shellData, workspaceExport, workspaceManifest, expectedExportBytes, desktop, mobile, missingArtifact, networkRecords);
    console.log(`workspace-browser-engine=chromium@${browser.version()}`);
    console.log(`workspace-browser-report-digest=${evidence.report.report_digest}`);
    console.log(`workspace-browser-routes=${evidence.report.route_count}`);
    console.log(`workspace-browser-external-requests=${evidence.report.external_request_count}`);
    console.log("workspace-browser=workspace-browser-candidate; authority=ephemeral-only; mutation=false");
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
