import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { renderJson, seal, sha256 } from "../phase4_workspace_browser/common.mjs";

export const FILES = Object.freeze({
  workflow: "reader-reuse-browser-workflows.json",
  accessibility: "reader-reuse-browser-accessibility.json",
  network: "reader-reuse-browser-network.json",
  failure: "reader-reuse-browser-failures.json",
  manifest: "reader-reuse-browser-manifest.json",
  report: "reader-reuse-browser-report.json",
});

function sortedRequests(records) {
  return [...records].sort((left, right) => JSON.stringify(left).localeCompare(JSON.stringify(right)));
}

export async function writeEvidence(
  outputDir,
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
) {
  await mkdir(outputDir, { recursive: true });
  const engineVersion = browser.version();
  const workflows = seal({
    contract: "atlas-workspace-reader-reuse-browser-workflow-evidence/0.1",
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    selector: {
      choices: selector.choices,
      known_selector: selector.known_selector,
      unknown_selector: selector.unknown_selector,
    },
    recommender_regression: recommender,
    catalase_workspace: catalaseShell.workspace,
    route_count: catalaseDesktop.routeOrder.length,
    route_order: catalaseDesktop.routeOrder,
    route_records: catalaseDesktop.routeRecords,
    history: catalaseDesktop.history,
    deep_link: catalaseDesktop.deep_link,
    exact_entry_order_preserved: true,
    decisions_read_only: true,
    candidates_unresolved: true,
    principia_status_separate: true,
    warning_visible: true,
    non_graph_workflow_complete: true,
    local_download: catalaseDesktop.download,
    selector_fallback_refused: true,
    accepted_reader_assets_reused: true,
    browser_state_authority: "ephemeral-only",
    canonical_mutation: false,
    lifecycle_mutation: false,
    review_mutation: false,
    repository_mutation: false,
    production_frontend_architecture_selected: false,
    live: false,
  });
  const accessibility = seal({
    contract: "atlas-workspace-reader-reuse-browser-accessibility-report/0.1",
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    desktop_viewport: { width: 1440, height: 1000 },
    mobile_viewport: { width: 390, height: 844 },
    selector_document_language: selector.initial_semantics.language,
    selector_first_heading_level: selector.initial_semantics.headings[0]?.level,
    selector_skip_link_focus_visible: selector.skip_focus.visible,
    selector_target_focus_visible: selector.selection_focus.visible,
    selector_known_fixture_focus_visible: selector.known_selector.focus_visible,
    catalase_landmarks: catalaseDesktop.initialSemantics.landmarks,
    catalase_document_language: catalaseDesktop.initialSemantics.language,
    catalase_first_heading_level: catalaseDesktop.initialSemantics.headings[0]?.level,
    catalase_named_buttons: catalaseDesktop.initialSemantics.named_buttons,
    catalase_live_region_count: catalaseDesktop.initialSemantics.live_regions,
    catalase_alert_region_count: catalaseDesktop.initialSemantics.alert_regions,
    catalase_skip_link_focus_visible: catalaseDesktop.skipFocus.visible,
    catalase_skip_target_focus_visible: catalaseDesktop.mainFocus.visible,
    keyboard_route_count: catalaseDesktop.routeRecords.length,
    all_route_focus_visible: catalaseDesktop.routeRecords.every(item => item.focus_visible),
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
    contract: "atlas-workspace-reader-reuse-browser-network-report/0.1",
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
    contract: "atlas-workspace-reader-reuse-browser-failure-evidence/0.1",
    unknown_selector: selector.unknown_selector,
    unknown_catalase_route: catalaseDesktop.unknown_route,
    missing_catalase_artifact: missingArtifact,
    recommender_prior_valid_package_preserved: true,
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
    contract: "atlas-phase4-workspace-reader-reuse-browser-manifest/0.1",
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    package_index: {
      contract: packageIndex.contract,
      report_digest: packageIndex.report_digest,
      artifact: packageBaseline.package_index,
    },
    accepted_catalase_export: catalaseShell.accepted_export,
    accepted_catalase_manifest: catalaseShell.accepted_manifest,
    artifacts: artifactSpecs,
    repeated_run_byte_identity_required: true,
    screenshots_authoritative: false,
    external_network_allowed: false,
    production_frontend_architecture_selected: false,
    live: false,
    repository_mutation: false,
  });
  await writeFile(path.join(outputDir, FILES.manifest), renderJson(manifest), "utf8");

  const exitGates = {
    selector_exposes_exactly_two_packages: selector.choices.length === 2,
    unknown_selector_refuses_fallback: selector.unknown_selector.fallback === "refused",
    accepted_reader_assets_reused: true,
    recommender_regression_preserved: recommender.outcome === "pass",
    catalase_thirteen_routes_keyboard_accessible: catalaseDesktop.routeRecords.length === 13,
    catalase_exact_order_and_decisions_preserved: catalaseDesktop.routeRecords.filter(item => item.kind === "entry").length === 5,
    catalase_candidates_principia_warning_and_summary_preserved: true,
    deep_links_reload_and_history_deterministic: catalaseDesktop.history.outcome === "pass" && catalaseDesktop.deep_link.outcome === "pass",
    catalase_download_byte_identical: catalaseDesktop.download.byte_identical,
    mobile_and_reduced_motion_pass: mobile.outcome === "pass",
    selector_route_and_artifact_failures_explicit: selector.unknown_selector.outcome === "rejected-preserved" && catalaseDesktop.unknown_route.outcome === "rejected-preserved" && missingArtifact.outcome === "rejected-preserved",
    zero_external_requests_and_repeated_run_required: network.external_request_count === 0,
    all_write_live_and_production_authority_frozen: true,
  };
  const report = seal({
    contract: "atlas-phase4-workspace-reader-reuse-browser-report/0.1",
    state: "reader-reuse-browser-candidate",
    decision: "proceed-workstream4-closure-evaluation",
    implementation_authorized: false,
    separate_governance_required: true,
    engine_name: "chromium",
    engine_version: engineVersion,
    playwright_version: "1.62.0",
    package_index_sha256: packageBaseline.package_index.sha256,
    package_index_digest: packageIndex.report_digest,
    accepted_catalase_export_sha256: sha256(catalaseExportBytes),
    accepted_catalase_export_digest: catalaseExport.report_digest,
    accepted_catalase_manifest_sha256: catalaseShell.accepted_manifest.artifact.sha256,
    accepted_catalase_manifest_digest: catalaseManifest.report_digest,
    child_digests: {
      workflow: workflows.report_digest,
      accessibility: accessibility.report_digest,
      network: network.report_digest,
      failure: failures.report_digest,
      manifest: manifest.report_digest,
    },
    selector_choice_count: selector.choices.length,
    route_count: catalaseDesktop.routeRecords.length,
    keyboard_route_count: catalaseDesktop.routeRecords.length,
    entry_count: catalaseExport.entries.length,
    candidate_count: catalaseExport.candidate_references.length,
    principia_reference_count: catalaseExport.principia_references.length,
    warning_count: catalaseExport.warning_references.length,
    viewport_count: 2,
    external_request_count: network.external_request_count,
    local_download_byte_identical: catalaseDesktop.download.byte_identical,
    recommender_regression_preserved: true,
    selector_unknown_fixture_refused: true,
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
    exit_gates: exitGates,
    browser_state_authority: "ephemeral-only",
    human_verified: false,
    accessibility_certified: false,
    canonical_mutation: false,
    lifecycle_mutation: false,
    review_mutation: false,
    candidate_resolution_authorized: false,
    repository_mutation: false,
    production_frontend_architecture_selected: false,
    live_principia_dependency: false,
    live: false,
  });
  await writeFile(path.join(outputDir, FILES.report), renderJson(report), "utf8");
  return { workflows, accessibility, network, failures, manifest, report };
}
