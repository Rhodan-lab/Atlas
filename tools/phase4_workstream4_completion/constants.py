"""Pinned contracts and identities for Phase 4 Workstream 4 closure."""
from __future__ import annotations

COMPLETION_CONTRACT = "atlas-phase4-workstream4-completion-report/0.1"
VALIDATION_CONTRACT = "atlas-phase4-workstream4-completion-validation/0.1"
BASELINE_CONTRACT = "atlas-phase4-workstream4-completion-baseline/0.1"
MODE = "interactive-experience-foundation"
ALLOWED_DECISIONS = (
    "proceed-phase4-completion-governance",
    "hold-accepted-workstream4",
    "reject-workstream4-generalization",
)

GENERALIZATION_CONTRACT = "atlas-phase4-workspace-generalization-baseline/0.1"
PACKAGE_CONTRACT = "atlas-phase4-workspace-reader-reuse-baseline/0.1"
BROWSER_CONTRACT = "atlas-phase4-workspace-reader-reuse-browser-baseline/0.1"

EXPECTED_GENERALIZATION = {
    "accepted_pr": 58,
    "accepted_candidate_head": "4b25e0ac7e5b31f05629b19cef6388ca823ad9fa",
    "accepted_merge_commit": "a7e04f377389cb003aec8faadcd3eccdfd78ba2b",
    "fixture_sha256": "0a3c76134b72351b9e3c331d7058563f24cd9eef498af1053e60c4b96ef031cd",
    "report_sha256": "9028a6a4aa7d3841201d9273b42466ad217b283df93e84192933792ed1d6f2f6",
    "report_digest": "75e5b93d288bd459e7ccc4e134b042f50dc1ef4a4eab24889fdb29b0b7a67121",
    "workspace_report_sha256": "5a8c307e858b348bc695e7dcffe0c5a3577e4ccf83d282631a25f1b623facb91",
    "workspace_report_digest": "3390157fd3935cb3f17ea2519a006589e299bbb922d87e28315e13172dc8fc32",
    "export_sha256": "b05617cac685873cd472b157efde835365b36d846db5eecf941db3495cc79893",
    "export_digest": "d8280f4aa5cfbb5ba91569190ce7836676a5eabc22c113eccd4474ade6a25154",
    "manifest_sha256": "170a943ceecd306eb02251c92a143137d8f3dc6b047d52d5f5efcc9facf13a5f",
    "manifest_digest": "0e1d2ee3674457844740b17100be298924293f1a9f7b0fab93ecae478197ca21",
}

EXPECTED_PACKAGE = {
    "accepted_pr": 60,
    "accepted_tested_head": "c5b76df4eb303bce5820044ebacc51a178938111",
    "accepted_merge_commit": "694ee1346045e79a843b02242a51dcba0e5b3928",
    "file_count": 18,
    "fixture_packages": 2,
    "generalized_fixtures": 1,
    "package_index_sha256": "225aff2dd97b3fb0adfc528b10ac2a485eadb2db68758b8605fa633675810b53",
    "package_index_digest": "209daa4d90de4271d2d09ea5942e561811a8f4d907553ff3eecb09943c6f5b18",
    "report_sha256": "c55e3a1ce55b735ed01c43eb47b3b7ca95fe7eee8914d8913133a6614ef1d752",
    "report_digest": "cebaba8c4e9dfca355c2b771e86a53f95e18de6c2d88fead996f314c87b812f2",
    "validation_sha256": "4499e674dc272f3037ae16c307f9c4c762e795f524ce035d8170055e40146512",
    "recommender_export_sha256": "43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a",
    "recommender_manifest_sha256": "8240d78b29f610cb7c566dfad50432473949c5a63b9de9c522ab28751d80fd09",
    "recommender_shell_sha256": "a2dd3979c35cee4d081511cadf98499e325dfd22d814cae097cfd3e98f3f5c0c",
    "catalase_export_sha256": "b05617cac685873cd472b157efde835365b36d846db5eecf941db3495cc79893",
    "catalase_manifest_sha256": "170a943ceecd306eb02251c92a143137d8f3dc6b047d52d5f5efcc9facf13a5f",
    "catalase_shell_sha256": "9a45af3d8ec29aef03aafd472db1669a8ed5f60026eff9b784abe0a0f3be3815",
    "reader_app_sha256": "0f44b35ccd3a6c59abc9eecdcf176dbc3bbf53cc155ddedb32fb518003d5c50f",
    "reader_index_sha256": "ae7eafc4dccae669f25ed4f6e6e5bc8e81bce8dcabcc81b5d585d4d09fb5e921",
    "reader_styles_sha256": "6016098e9461be50f6b5346d76b58d0111dfae8d42355884bf25e9885546e98f",
}

EXPECTED_BROWSER = {
    "accepted_pr": 61,
    "accepted_tested_head": "ee22fa0e999b8a863ca08f1511a3a54f9449d3b2",
    "accepted_merge_commit": "8481b32cfa8fef538c5bd51833894d6ee52de64a",
    "engine": {"name": "chromium", "playwright_version": "1.62.0", "version": "151.0.7922.34"},
    "report_sha256": "bb2d7c4f2d195a6161329ac2a62e96e733768007749d19e75b7574c6983dc8f9",
    "report_digest": "e367bb46d43e0de6886f3ce9dffa22624c65cdb45ba5470e4ec48f544ac57ced",
    "validation_sha256": "d83844150b1a20273d79f343d44421e8dba01e183243d4e44d003247731fdf29",
    "workflow_sha256": "1c3fd948458cb46819a10d959e6d61e13092b778d1fc9c706225dfabecf6f709",
    "accessibility_sha256": "6f69665debcc22517a84872e36a546bd95850ee105f89fd5cfcf8ba7d03e1f9f",
    "network_sha256": "318c5bd0d19ddf9f89aa59708c62c5c5f6fc368751e78476e0548473554f45b7",
    "failure_sha256": "f06d60986526dead5bc84bc2d03b7312ce08af9d0b02d474ba57613ca6479786",
    "manifest_sha256": "529299543121252550d394c60b979b312d3cff905ca32ac6373d8a15c155e9ba",
}

NEGATIVE_CASES = (
    "E-W4-CLOSURE-GENERALIZATION-DRIFT",
    "E-W4-CLOSURE-PACKAGE-DRIFT",
    "E-W4-CLOSURE-BROWSER-DRIFT",
    "E-W4-CLOSURE-SECOND-FIXTURE",
    "E-W4-CLOSURE-READER-MUTATION",
    "E-W4-CLOSURE-IMPLICIT-LATEST",
    "E-W4-CLOSURE-CANDIDATE-RESOLUTION",
    "E-W4-CLOSURE-PRINCIPIA-STATUS",
    "E-W4-CLOSURE-WARNING-REMOVAL",
    "E-W4-CLOSURE-SELECTOR-FALLBACK",
    "E-W4-CLOSURE-ROUTE-FALLBACK",
    "E-W4-CLOSURE-DOWNLOAD-DRIFT",
    "E-W4-CLOSURE-EXTERNAL-NETWORK",
    "E-W4-CLOSURE-HUMAN-VERIFICATION",
    "E-W4-CLOSURE-ACCESSIBILITY-CERTIFICATION",
    "E-W4-CLOSURE-PRODUCTION-AUTHORITY",
    "E-W4-CLOSURE-REPOSITORY-MUTATION",
    "E-W4-CLOSURE-SELF-AUTHORIZATION",
    "E-W4-CLOSURE-GATE-TAMPER",
    "E-W4-CLOSURE-DIGEST-TAMPER",
)
