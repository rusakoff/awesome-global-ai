import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from catalog_lib import FILES, REQUIRED_COMMON, ROOT, all_rows, load_catalog, md  # noqa: E402


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def test_all_files_have_rows(self):
        for name in FILES:
            self.assertTrue(self.catalog[name], name)

    def test_required_values_are_present(self):
        for entity_type, row in all_rows(self.catalog):
            for field in REQUIRED_COMMON:
                self.assertTrue(row.get(field), f"{entity_type}:{row.get('id')} missing {field}")

    def test_ids_are_globally_unique(self):
        ids = [row["id"] for _, row in all_rows(self.catalog)]
        self.assertEqual(len(ids), len(set(ids)))

    def test_catalog_is_substantial(self):
        self.assertGreaterEqual(sum(len(rows) for rows in self.catalog.values()), 250)

    def test_readme_contains_every_catalog_entry(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for entity_type, row in all_rows(self.catalog):
            expected_link = f"[{md(row['name'])}]({row['website']})"
            self.assertIn(expected_link, readme, f"README missing {entity_type}:{row['id']}")


if __name__ == "__main__":
    unittest.main()
