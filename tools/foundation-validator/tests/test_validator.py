from __future__ import annotations

import sys
import unittest
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MODULE_ROOT))

import atlas_foundation_validator as validator


class ValidatorContractTests(unittest.TestCase):
    def base(self, entity_type: str, entity_id: str, **extra):
        metadata = {
            "contract": validator.SUPPORTED_CONTRACT,
            "id": entity_id,
            "work": "work:" + entity_id.replace(":", "-").replace("_", "-").lower(),
            "type": entity_type,
            "title": entity_id,
            "status": "draft",
            "revision": 1,
            "created": "2026-07-26",
            "updated": "2026-07-26",
            "language": "en",
        }
        metadata.update(extra)
        return metadata

    def document(self, path: str, metadata: dict, body: str = ""):
        return validator.Document(path=path, metadata=metadata, body=body)

    def codes(self, documents):
        return {item.code for item in validator.validate_corpus(documents)}

    def valid_supporting_corpus(self):
        source = self.document(
            "source.md",
            self.base(
                "source",
                "src:example-source",
                source={"title": "Example source", "locator": "https://example.org"},
                access={"class": "open"},
            ),
        )
        claim = self.document(
            "claim.md",
            self.base(
                "claim",
                "claim:en:example-claim",
                claim={
                    "kind": "descriptive",
                    "statement": "A scoped example claim.",
                    "confidence": "plausible",
                },
            ),
        )
        evidence = self.document(
            "evidence.md",
            self.base(
                "evidence",
                "evidence:en:example-result",
                source="src:example-source",
                locator={"kind": "section", "value": "Example section"},
                relations=[
                    {
                        "type": "supports",
                        "target": "claim:en:example-claim",
                        "note": "The scoped observation supports the scoped claim.",
                    }
                ],
            ),
        )
        model = self.document(
            "model.md",
            self.base(
                "model",
                "model:en:example-model",
                purpose="Represent the example.",
                inputs=["input"],
                outputs=["output"],
                assumptions=["bounded scope"],
                failure_modes=["outside the scope"],
            ),
        )
        concept = self.document(
            "concept.md",
            self.base(
                "concept",
                "concept:en:example-concept",
                definition="A concept used by the validator fixture.",
                claims=["claim:en:example-claim"],
                models=["model:en:example-model"],
            ),
        )
        question = self.document(
            "question.md",
            self.base(
                "question",
                "question:en:example-question",
                state="partially-answered",
                question="What does the example establish?",
                resolution_criteria=["trace conclusion to evidence"],
                related=["concept:en:example-concept"],
            ),
        )
        synthesis = self.document(
            "synthesis.md",
            self.base(
                "synthesis",
                "synthesis:en:example-synthesis",
                question="question:en:example-question",
                claims=["claim:en:example-claim"],
                models=["model:en:example-model"],
                evidence_selection="Use the one scoped result.",
                conclusion="The example supports only its stated scope.",
                revision_triggers=["the evidence changes"],
            ),
        )
        return [source, claim, evidence, model, concept, question, synthesis]

    def test_valid_minimal_corpus_has_no_errors(self):
        diagnostics = validator.validate_corpus(self.valid_supporting_corpus())
        self.assertEqual([], [item for item in diagnostics if item.severity == "error"])

    def test_f001_missing_contract(self):
        meta = self.base("concept", "concept:en:no-contract", definition="Example")
        meta.pop("contract")
        self.assertIn("E-CONTRACT-MISSING", self.codes([self.document("f001.md", meta)]))

    def test_f002_unsupported_contract(self):
        meta = self.base("concept", "concept:en:future-format", definition="Example")
        meta["contract"] = "atlas-content/99.0"
        self.assertIn("E-CONTRACT-UNSUPPORTED", self.codes([self.document("f002.md", meta)]))

    def test_f003_duplicate_id(self):
        meta = self.base("concept", "concept:en:duplicate-id", definition="Example")
        self.assertIn(
            "E-ID-DUPLICATE",
            self.codes([self.document("a.md", meta), self.document("b.md", dict(meta))]),
        )

    def test_f004_numeric_id(self):
        meta = self.base("concept", "concept:en:temporary", definition="Example")
        meta["id"] = 17
        self.assertIn("E-ID-NONCANONICAL", self.codes([self.document("f004.md", meta)]))

    def test_f005_evidence_without_source(self):
        meta = self.base(
            "evidence",
            "evidence:en:no-source",
            locator={"kind": "page", "value": 4},
        )
        self.assertIn("E-EVIDENCE-SOURCE-MISSING", self.codes([self.document("f005.md", meta)]))

    def test_f006_imprecise_locator_structure(self):
        meta = self.base(
            "evidence",
            "evidence:en:vague-location",
            source="src:example-source",
            locator="somewhere in the paper",
        )
        source = self.valid_supporting_corpus()[0]
        self.assertIn("E-LOCATOR-STRUCTURE", self.codes([source, self.document("f006.md", meta)]))

    def test_f007_reversed_support_relation(self):
        corpus = self.valid_supporting_corpus()
        claim = corpus[1]
        claim.metadata["relations"] = [
            {"type": "supports", "target": "evidence:en:example-result", "note": "reversed"}
        ]
        self.assertIn("E-RELATION-PAIR", self.codes(corpus))

    def test_f008_unknown_relation(self):
        corpus = self.valid_supporting_corpus()
        corpus[4].metadata["relations"] = [
            {"type": "related-to", "target": "concept:en:example-concept"}
        ]
        self.assertIn("E-RELATION-UNKNOWN", self.codes(corpus))

    def test_f009_reviewed_without_record(self):
        meta = self.base(
            "claim",
            "claim:en:unreviewed-reviewed",
            status="reviewed",
            claim={"kind": "descriptive", "statement": "Example."},
        )
        self.assertIn("E-REVIEW-RECORD-MISSING", self.codes([self.document("f009.md", meta)]))

    def test_f010_review_revision_mismatch(self):
        meta = self.base(
            "claim",
            "claim:en:review-mismatch",
            status="reviewed",
            revision=3,
            claim={"kind": "descriptive", "statement": "Example."},
            review={"entity_revision": 2, "types": ["editorial"]},
        )
        self.assertIn("E-REVIEW-REVISION-MISMATCH", self.codes([self.document("f010.md", meta)]))

    def test_f011_translation_review_is_independent(self):
        source = self.document(
            "source-claim.md",
            self.base(
                "claim",
                "claim:en:translated-claim",
                claim={"kind": "descriptive", "statement": "English claim."},
            ),
        )
        translation = self.document(
            "translation.md",
            self.base(
                "claim",
                "claim:id:translated-claim",
                status="reviewed",
                language="id",
                translation_of="claim:en:translated-claim",
                translation={"source_revision": 1, "method": "machine"},
                claim={"kind": "descriptive", "statement": "Klaim Indonesia."},
                review={"entity_revision": 1, "types": ["editorial"]},
            ),
        )
        codes = self.codes([source, translation])
        self.assertIn("E-TRANSLATION-REVIEW-MISSING", codes)
        self.assertIn("W-AI-ASSISTED-DRAFT-REQUIRED", codes)

    def test_f012_normative_claim_requires_values(self):
        meta = self.base(
            "claim",
            "claim:en:hidden-values",
            claim={"kind": "normative", "statement": "Platforms should act."},
        )
        self.assertIn("E-NORMATIVE-VALUES-MISSING", self.codes([self.document("f012.md", meta)]))

    def test_f013_prediction_requires_horizon_and_evaluation(self):
        meta = self.base(
            "claim",
            "claim:en:prediction-without-test",
            claim={"kind": "predictive", "statement": "The intervention will help."},
        )
        codes = self.codes([self.document("f013.md", meta)])
        self.assertIn("E-PREDICTION-HORIZON-MISSING", codes)
        self.assertIn("E-PREDICTION-EVALUATION-MISSING", codes)

    def test_f014_correlational_claim_warns_on_causal_wording(self):
        meta = self.base(
            "claim",
            "claim:en:causal-language-conflict",
            claim={"kind": "correlational", "statement": "Frequency causes stronger belief."},
        )
        self.assertIn("W-CLAIM-KIND-LANGUAGE-CONFLICT", self.codes([self.document("f014.md", meta)]))

    def test_f015_numeric_measurement_requires_unit(self):
        source = self.valid_supporting_corpus()[0]
        meta = self.base(
            "evidence",
            "evidence:en:unitless-temperature",
            source="src:example-source",
            locator={"kind": "table", "value": "row 1"},
            measurement={"quantity": "temperature", "value": 37},
        )
        self.assertIn("E-MEASUREMENT-UNIT-MISSING", self.codes([source, self.document("f015.md", meta)]))

    def test_f016_conversion_preserves_original(self):
        source = self.valid_supporting_corpus()[0]
        meta = self.base(
            "evidence",
            "evidence:en:lost-conversion",
            source="src:example-source",
            locator={"kind": "table", "value": "row 1"},
            measurement={
                "quantity": "length",
                "value": 10,
                "unit": "cm",
                "transformation": "converted",
            },
        )
        self.assertIn("E-CONVERSION-LINEAGE-MISSING", self.codes([source, self.document("f016.md", meta)]))

    def test_f017_derived_evidence_requires_inputs(self):
        source = self.valid_supporting_corpus()[0]
        meta = self.base(
            "evidence",
            "evidence:en:no-input-lineage",
            source="src:example-source",
            locator={"kind": "analysis", "value": "result 1"},
            transformation={"procedure": "analysis:summary-v1", "parameters": {"aggregation": "mean"}},
        )
        self.assertIn("E-TRANSFORMATION-INPUT-MISSING", self.codes([source, self.document("f017.md", meta)]))

    def test_f018_model_derived_claim_requires_model(self):
        meta = self.base(
            "claim",
            "claim:en:periodic-without-model",
            claim={"kind": "model-derived", "statement": "The sequence is periodic."},
        )
        self.assertIn("E-MODEL-REFERENCE-MISSING", self.codes([self.document("f018.md", meta)]))

    def test_f019_argument_premises_are_claims(self):
        meta = self.base(
            "claim",
            "claim:en:bad-premise",
            claim={"kind": "interpretive", "statement": "A conclusion."},
            argument={
                "mode": "inductive",
                "premises": ["src:paper-1"],
                "conclusion": "claim:en:bad-premise",
            },
        )
        self.assertIn("E-ARGUMENT-PREMISE-TYPE", self.codes([self.document("f019.md", meta)]))

    def test_f020_normative_inference_exposes_values(self):
        empirical = self.document(
            "empirical.md",
            self.base(
                "claim",
                "claim:en:ranking-changes-exposure",
                claim={"kind": "causal", "statement": "Ranking changes exposure."},
            ),
        )
        normative = self.document(
            "normative.md",
            self.base(
                "claim",
                "claim:en:platforms-should-be-banned",
                claim={"kind": "normative", "statement": "Platforms should be banned."},
                values=["autonomy"],
                argument={
                    "mode": "deductive",
                    "premises": ["claim:en:ranking-changes-exposure"],
                    "conclusion": "claim:en:platforms-should-be-banned",
                },
            ),
        )
        self.assertIn("W-NORMATIVE-INFERENCE-HIDDEN", self.codes([empirical, normative]))

    def test_f021_restricted_excerpt_is_bounded(self):
        source = self.valid_supporting_corpus()[0]
        meta = self.base(
            "evidence",
            "evidence:en:restricted-chapter",
            source="src:example-source",
            locator={"kind": "chapter", "value": "1"},
            access={"class": "licensed"},
            excerpt="word " * 121,
        )
        self.assertIn("E-RESTRICTED-CONTENT-PUBLIC", self.codes([source, self.document("f021.md", meta)]))

    def test_f022_hash_does_not_prove_truth(self):
        meta = self.base(
            "claim",
            "claim:en:hash-proves-truth",
            claim={"kind": "interpretive", "statement": "The digest proves the source is true."},
        )
        self.assertIn("W-INTEGRITY-SEMANTIC-OVERREACH", self.codes([self.document("f022.md", meta)]))

    def test_f023_semantic_split_requires_mapping(self):
        diagnostics = validator.validate_migration_manifest(
            {
                "mode": "semantic-split",
                "inputs": ["claim:en:compound"],
                "outputs": ["claim:en:a", "claim:en:b"],
                "mappings": {},
            },
            "f023.json",
        )
        self.assertIn("E-MIGRATION-IDENTITY-MAPPING-MISSING", {item.code for item in diagnostics})

    def test_f024_unknown_field_is_not_ignored(self):
        meta = self.base(
            "concept",
            "concept:en:magic-score",
            definition="Example.",
            magic_truth_score=0.98,
        )
        self.assertIn("E-FIELD-UNKNOWN", self.codes([self.document("f024.md", meta)]))

    def test_mechanical_migration_preserves_required_fields(self):
        before = {
            "id": "claim:en:example",
            "work": "work:example",
            "status": "draft",
            "revision": 1,
        }
        after = dict(before, optional_note="added")
        diagnostics = validator.validate_migration_manifest(
            {
                "mode": "mechanical",
                "before": before,
                "after": after,
                "preserve": ["id", "work", "status", "revision"],
            },
            "mechanical.json",
        )
        self.assertEqual([], diagnostics)

    def test_identity_alias_and_federation_manifest(self):
        diagnostics = validator.validate_identity_manifest(
            {
                "canonical_ids": ["claim:en:new-id"],
                "aliases": {"claim:en:old-id": "claim:en:new-id"},
                "federated_ids": ["atlas://rhodan-lab/claim:en:new-id"],
            },
            "identity.json",
        )
        self.assertEqual([], diagnostics)

    def test_translation_staleness_is_computed_from_revision(self):
        self.assertEqual(
            "possibly-stale",
            validator.compute_translation_staleness(
                {"source_revision": 2, "translation_source_revision": 1}
            ),
        )
        self.assertEqual(
            "current",
            validator.compute_translation_staleness(
                {"source_revision": 2, "translation_source_revision": 2}
            ),
        )

    def test_feedback_sequence_is_reproducible(self):
        values = [1, 0]
        for _ in range(6):
            values.append(values[-1] - values[-2])
        self.assertEqual([1, 0, -1, -1, 0, 1, 1, 0], values)

    def test_repository_canonical_corpus_has_no_errors(self):
        paths = [REPO_ROOT / "content" / "canonical", REPO_ROOT / "content" / "translations"]
        documents, parse_diagnostics = validator.discover_documents(paths)
        diagnostics = parse_diagnostics + validator.validate_corpus(documents)
        errors = [item for item in diagnostics if item.severity == "error"]
        self.assertEqual([], errors, "\n".join(str(item) for item in errors))


if __name__ == "__main__":
    unittest.main()
