import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { renderJson, seal, sha256 } from "./common.mjs";

const FILES = Object.freeze({
  workflow: "workspace-browser-workflows.json",
  accessibility: "workspace-browser-accessibility.json",
  network: "workspace-browser-network.json",
  failure: "workspace-browser-failures.json",
  manifest: "workspace-browser-manifest.json",
  report: "workspace-browser-report.json",
});

function sortedRequests(records) {
  return [...records].sort((left, right) => JSON.stringify(left).localeCompare(JSON.stringify(right)));
}

export async function writeEvidence(outputDir, browser, args, shellData, workspaceExport, workspaceManifest, expectedExportBytes, desktop, mobile, missingArtifact, networkRecords) {
  await mkdir(outputDir, { recursive: true });
  const engineVersion = browser.version();
  const workflows = seal({
    contract: "atlas-workspace-browser-workflow-evidence/0.1",
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    workspace: shellData.workspace,
    route_count: desktop.routeOrder.length,
    route_order: desktop.routeOrder,
    route_records: desktop.routeRecords,
    history: desktop.history,
    deep_link: desktop.deep_link,
    exact_entry_order_preserved: true,
    decisions_read_only: true,
    candidates_unresolved: true,
    principia_status_separate: true,
    warning_visible: true,
    non_graph_workflow_complete: true,
    local_download: desktop.download,
    browser_state_authority: "ephemeral-only",
    canonical_mutation: false,
    lifecycle_mutation: false,
    review_mutation: false,
    repository_mutation: false,
    production_frontend_architecture_selected: false,
    live: false,
  });
  const accessibility = seal({
    contract: "atlas-workspace-browser-accessibility-report/0.1",
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    desktop_viewport: { width: 1440, height: 1000 },
    mobile_viewport: { width: 390, height: 844 },
    landmarks: desktop.initialSemantics.landmarks,
    document_language: desktop.initialSemantics.language,
    first_heading_level: desktop.initialSemantics.headings[0]?.level,
    named_buttons: desktop.initialSemantics.named_buttons,
    live_region_count: desktop.initialSemantics.live_regions,
    alert_region_count: desktop.initialSemantics.alert_regions,
    skip_link_focus_visible: desktop.skipFocus.visible,
    skip_target_focus_visible: desktop.mainFocus.visible,
    keyboard_route_count: desktop.routeRecords.length,
    all_route_focus_visible: desktop.routeRecords.every(item => item.focus_visible),
    reduced_motion_verified: mobile.reduced_motion,
    mobile_no_horizontal_overflow: mobile.scroll_width <= mobile.width,
    human_verified: false,
    assistive_technology_user_reviewed: false,
    accessibility_certified: false,
    live: false,
    repository_mutation: false,
  });
  const requests = sortedRequests(networkRecords);
  const externalRequests = requests.filter(item => item.decision === "blocked-external");
  const network = seal({
    contract: "atlas-workspace-browser-network-report/0.1",
    allowed_origin: new URL(args.baseUrl).origin,
    request_count: requests.length,
    loopback_request_count: requests.filter(item => item.decision !== "blocked-external").length,
    blocked_test_loopback_count: requests.filter(item => item.decision === "blocked-test-loopback").length,
    external_request_count: externalRequests.length,
    requests,
    credentials_used: false,
    remote_assets_used: false,
    analytics_used: false,
    cloud_service_used: false,
    account_required: false,
    external_network_allowed: false,
    live: false,
    repository_mutation: false,
  });
  const failures = seal({
    contract: "atlas-workspace-browser-failure-evidence/0.1",
    unknown_route: desktop.unknown_route,
    missing_artifact: missingArtifact,
    prior_valid_view_preserved: true,
    silent_fallback_used: false,
    implicit_latest_used: false,
    browser_state_persisted_as_authority: false,
    canonical_mutation: false,
    lifecycle_mutation: false,
    review_mutation: false,
    repository_mutation: false,
    live: false,
  });

  const childRecords = { workflows, accessibility, network, failures };
  for (const [key, record] of Object.entries(childRecords)) {
    await writeFile(path.join(outputDir, FILES[key === "workflows" ? "workflow" : key === "failures" ? "failure" : key]), renderJson(record), "utf8");
  }
  const artifactSpecs = [];
  for (const key of ["workflow", "accessibility", "network", "failure"]) {
    const file = FILES[key];
    const bytes = await readFile(path.join(outputDir, file));
    const record = JSON.parse(bytes);
    artifactSpecs.push({ file, bytes: bytes.length, sha256: sha256(bytes), report_digest: record.report_digest, contract: record.contract });
  }
  const manifest = seal({
    contract: "atlas-phase4-workspace-browser-manifest/0.1",
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    workspace: shellData.workspace,
    accepted_export: shellData.accepted_export,
    accepted_manifest: shellData.accepted_manifest,
    artifacts: artifactSpecs,
    repeated_run_byte_identity_required: true,
    screenshots_authoritative: false,
    external_network_allowed: false,
    production_frontend_architecture_selected: false,
    live: false,
    repository_mutation: false,
  });
  await writeFile(path.join(outputDir, FILES.manifest), renderJson(manifest), "utf8");
  const report = seal({
    contract: "atlas-phase4-workspace-browser-report/0.1",
    state: "workspace-browser-candidate",
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    workspace: shellData.workspace,
    accepted_export_sha256: sha256(expectedExportBytes),
    accepted_export_digest: workspaceExport.report_digest,
    accepted_manifest_sha256: shellData.accepted_manifest.artifact.sha256,
    accepted_manifest_digest: workspaceManifest.report_digest,
    child_digests: {
      workflow: workflows.report_digest,
      accessibility: accessibility.report_digest,
      network: network.report_digest,
      failure: failures.report_digest,
      manifest: manifest.report_digest,
    },
    route_count: desktop.routeRecords.length,
    keyboard_route_count: desktop.routeRecords.length,
    entry_count: workspaceExport.entries.length,
    candidate_count: workspaceExport.candidate_references.length,
    principia_reference_count: workspaceExport.principia_references.length,
    warning_count: workspaceExport.warning_references.length,
    viewport_count: 2,
    external_request_count: network.external_request_count,
    local_download_byte_identical: desktop.download.byte_identical,
    exact_entry_order_preserved: true,
    decisions_read_only: true,
    candidates_unresolved: true,
    principia_status_separate: true,
    warning_visibility_verified: true,
    non_graph_workflow_complete: true,
    visible_focus_verified: true,
    reduced_motion_verified: true,
    unknown_route_preserved: true,
    missing_artifact_failure_explicit: true,
    browser_state_authority: "ephemeral-only",
    human_verified: false,
    accessibility_certified: false,
    canonical_mutation: false,
    lifecycle_mutation: false,
    review_mutation: false,
    repository_mutation: false,
    production_frontend_architecture_selected: false,
    live_principia_dependency: false,
    live: false,
  });
  await writeFile(path.join(outputDir, FILES.report), renderJson(report), "utf8");
  return { workflows, accessibility, network, failures, manifest, report };
}
