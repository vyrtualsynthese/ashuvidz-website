import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check_site.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class CheckSiteTest(unittest.TestCase):
    def run_check(self, name: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / name)],
            capture_output=True,
            text=True,
        )

    def test_good_tree_passes(self):
        result = self.run_check("good")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_ignores_non_public_directories(self):
        result = self.run_check("ignored-dirs")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_internal_link_missing_file(self):
        result = self.run_check("broken-internal")
        self.assertEqual(result.returncode, 1)
        self.assertIn("LINK-INTERNAL", result.stdout)

    def test_empty_href(self):
        result = self.run_check("broken-empty")
        self.assertEqual(result.returncode, 1)
        self.assertIn("LINK-EMPTY", result.stdout)

    def test_page_without_og_image(self):
        result = self.run_check("broken-head")
        self.assertEqual(result.returncode, 1)
        self.assertIn("HEAD-REQUIRED", result.stdout)

    def test_hreflang_not_reciprocal(self):
        result = self.run_check("broken-hreflang")
        self.assertEqual(result.returncode, 1)
        self.assertIn("HREFLANG", result.stdout)

    def test_twins_link_different_hosts(self):
        result = self.run_check("broken-parity")
        self.assertEqual(result.returncode, 1)
        self.assertIn("PARITY", result.stdout)

    def test_english_page_without_french_twin(self):
        result = self.run_check("broken-orphan-en")
        self.assertEqual(result.returncode, 1)
        self.assertIn("HREFLANG", result.stdout)

    def test_hreflang_pointing_at_itself(self):
        result = self.run_check("broken-hreflang-self")
        self.assertEqual(result.returncode, 1)
        self.assertIn("HREFLANG", result.stdout)

    def test_stylesheet_link_missing_file(self):
        result = self.run_check("broken-link-href")
        self.assertEqual(result.returncode, 1)
        self.assertIn("LINK-INTERNAL", result.stdout)

    def test_french_typography_in_meta_description(self):
        result = self.run_check("broken-typo-attr")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FR-TYPO", result.stdout)

    def test_page_missing_from_sitemap(self):
        result = self.run_check("broken-sitemap")
        self.assertEqual(result.returncode, 1)
        self.assertIn("SITEMAP", result.stdout)

    def test_straight_apostrophe_in_french(self):
        result = self.run_check("broken-typo")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FR-TYPO", result.stdout)

    def test_blank_target_without_noopener(self):
        result = self.run_check("broken-rel")
        self.assertEqual(result.returncode, 1)
        self.assertIn("EXTERNAL-REL", result.stdout)


if __name__ == "__main__":
    unittest.main()
