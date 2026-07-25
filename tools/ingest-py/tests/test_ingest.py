from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from atlas_ingest.parser import IngestError, compile_directory, load_notes, render_atlas


class IngestionTests(unittest.TestCase):
    def write_note(self, directory: Path, name: str, text: str) -> None:
        (directory / name).write_text(text.strip() + "\n", encoding="utf-8")

    def test_compiles_deterministically_and_resolves_relations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_note(
                root,
                "zeta.md",
                """
                ---
                slug: zeta
                title: Zeta
                tags: foundation, Graph
                relation: depends-on | alpha | 0.75 | Needs Alpha
                ---
                A later concept.
                """,
            )
            self.write_note(
                root,
                "alpha.md",
                """
                ---
                slug: alpha
                title: Alpha
                source: Reference | https://example.test/alpha
                ---
                The first concept.
                """,
            )

            document = load_notes(root)
            self.assertEqual(document.ids_by_slug, {"alpha": 1, "zeta": 2})
            rendered = render_atlas(document)
            self.assertIn('C\t1\t"Alpha"', rendered)
            self.assertIn('R\t2\t1\t"depends-on"\t0.75\t"Needs Alpha"', rendered)

            output = root / "out.atlas"
            compile_directory(root, output)
            self.assertEqual(output.read_text(encoding="utf-8"), rendered)

    def test_rejects_unknown_relation_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_note(
                root,
                "one.md",
                """
                ---
                slug: one
                title: One
                relation: supports | missing
                ---
                Summary.
                """,
            )
            with self.assertRaisesRegex(IngestError, "does not exist"):
                load_notes(root)

    def test_rejects_duplicate_slug(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("one.md", "two.md"):
                self.write_note(
                    root,
                    name,
                    """
                    ---
                    slug: duplicate
                    title: Duplicate
                    ---
                    Summary.
                    """,
                )
            with self.assertRaisesRegex(IngestError, "duplicate slug"):
                load_notes(root)


if __name__ == "__main__":
    unittest.main()
