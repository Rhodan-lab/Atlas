import { chromium } from "playwright";
import { readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import {
  assertEvidence,
  readJson,
  setRoutes,
  sha256,
} from "../phase4_workspace_browser/common.mjs";
import { desktopEvidence } from "../phase4_workspace_browser/desktop.mjs";
import { selectorEvidence, recommenderRegression } from "./selector.mjs";
import { catalaseMobileEvidence, catalaseMissingArtifactEvidence } from "./failures.mjs";
import { writeEvidence } from "./emit.mjs";

function parseArgs(argv) {
  const result = {
    baseUrl: "http://127.0.0.1:8772",
    repoRoot: path.resolve("../.."),
    packageDir: path.resolve("../../phase4-reader-reuse-package"),
    outputDir: path.resolve("../../phase4-reader-reuse-browser-evidence"),
  };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--base-url") result.baseUrl = argv[++index];
    else if (value === "--repo-root") result.repoRoot = path.resolve(argv[++index]);
    else if (value === "--package-dir") result.packageDir = path.resolve(argv[++index]);
    else if (value === "--output-dir") result.outputDir = path.resolve(argv[++index]);
    else throw new Error(`Unknown argument: ${value}`);
  }
  return result;
}

async function verifyInputFile(packageDir, relative, expected) {
  const payload = await readFile(path.join(packageDir, relative));
  assertEvidence(payload.length === expected.bytes, "E-READER-BROWSER-INPUT", `${relative} byte length differs from pinned package`);
  assertEvidence(sha256(payload) === expected.sha256, "E-READER-BROWSER-INPUT", `${relative} SHA-256 differs from pinned package`);
  return payload;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const packageBaseline = await readJson(path.join(args.repoRoot, "content/fixtures/phase4_workspace_reader_reuse/reader-reuse-baseline.json"));
  const packageIndexBytes = await verifyInputFile(args.packageDir, "package-index.json", packageBaseline.files["package-index.json"]);
  const packageIndex = JSON.parse(packageIndexBytes);
  assertEvidence(packageIndex.report_digest === packageBaseline.package_index_digest, "E-READER-BROWSER-INPUT", "package index digest differs from pinned baseline");

  for (const [relative, expected] of Object.entries(packageBaseline.files)) {
    await verifyInputFile(args.packageDir, relative, expected);
  }

  const recommenderDir = path.join(args.packageDir, "packages/recommender");
  const catalaseDir = path.join(args.packageDir, "packages/catalase");
  const recommenderShell = await readJson(path.join(recommenderDir, "data/workspace-shell-data.json"));
  const recommenderExport = await readJson(path.join(recommenderDir, "data/workspace-export.json"));
  const catalaseShell = await readJson(path.join(catalaseDir, "data/workspace-shell-data.json"));
  const catalaseExport = await readJson(path.join(catalaseDir, "data/workspace-export.json"));
  const catalaseManifest = await readJson(path.join(catalaseDir, "data/workspace-manifest.json"));
  const catalaseExportBytes = await readFile(path.join(catalaseDir, "data/workspace-export.json"));
  assertEvidence(catalaseShell.accepted_export.artifact.sha256 === sha256(catalaseExportBytes), "E-READER-BROWSER-INPUT", "Catalase shell export identity must match package bytes");
  assertEvidence(catalaseExport.report_digest === catalaseShell.accepted_export.report_digest, "E-READER-BROWSER-INPUT", "Catalase export digest must match shell data");
  assertEvidence(catalaseManifest.report_digest === catalaseShell.accepted_manifest.report_digest, "E-READER-BROWSER-INPUT", "Catalase manifest digest must match shell data");
  assertEvidence(recommenderShell.accepted_export.artifact.sha256 === packageBaseline.files["packages/recommender/data/workspace-export.json"].sha256, "E-READER-BROWSER-INPUT", "recommender regression identity differs");

  const browser = await chromium.launch({ headless: true });
  const networkRecords = [];
  const catalaseBaseUrl = `${args.baseUrl}/packages/catalase`;
  try {
    const selector = await selectorEvidence(browser, args.baseUrl, networkRecords);
    const recommender = await recommenderRegression(browser, args.baseUrl, recommenderShell, recommenderExport, networkRecords);
    setRoutes(catalaseShell.routes);
    const catalaseDesktop = await desktopEvidence(
      browser,
      catalaseBaseUrl,
      catalaseShell,
      catalaseExport,
      catalaseExportBytes,
      networkRecords,
    );
    const mobile = await catalaseMobileEvidence(browser, catalaseBaseUrl, networkRecords);
    const missingArtifact = await catalaseMissingArtifactEvidence(browser, args.baseUrl, catalaseBaseUrl, networkRecords);
    const evidence = await writeEvidence(
      args.outputDir,
      browser,
      args,
      packageIndex,
      packageBaseline,
      catalaseShell,
      catalaseExport,
      catalaseManifest,
      catalaseExportBytes,
      selector,
      recommender,
      catalaseDesktop,
      mobile,
      missingArtifact,
      networkRecords,
    );
    console.log(`reader-reuse-browser-engine=chromium@${browser.version()}`);
    console.log(`reader-reuse-browser-report-digest=${evidence.report.report_digest}`);
    console.log(`reader-reuse-browser-routes=${evidence.report.route_count}`);
    console.log(`reader-reuse-browser-selector-choices=${evidence.report.selector_choice_count}`);
    console.log(`reader-reuse-browser-external-requests=${evidence.report.external_request_count}`);
    console.log(`reader-reuse-browser-decision=${evidence.report.decision}; implementation-authorized=false`);
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
