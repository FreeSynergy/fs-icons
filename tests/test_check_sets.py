import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_sets  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

TOML = """[set]
id = "t"
name = "T"
kind = "icon-theme"
version = "0.1.0"
license = "MIT"
license_files = ["LICENSE-MIT"]
origin = "test"
[[icon]]
name = "{name}"
file = "scalable/actions/a.svg"
context = "actions"
naming = "{naming}"
meaning = "m"
purpose = "p"
purpose_de = "z"
sizes = ["scalable"]
"""
INDEX = "[Icon Theme]\nName=T\nDirectories=scalable/actions\n\n[scalable/actions]\nSize=24\nType=Scalable\n"


def make(name="edit-copy", naming="spec", svg=True):
    d = Path(tempfile.mkdtemp()) / "t"
    (d / "scalable/actions").mkdir(parents=True)
    (d / "icons.toml").write_text(TOML.format(name=name, naming=naming))
    (d / "index.theme").write_text(INDEX)
    (d / "LICENSE-MIT").write_text("x")
    if svg:
        (d / "scalable/actions/a.svg").write_text("<svg/>")
    return d


class CheckSets(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(check_sets.check_set(make()), [])

    def test_missing_file(self):
        self.assertTrue(any("not found" in e for e in check_sets.check_set(make(svg=False))))

    def test_own_prefix(self):
        self.assertTrue(any("freesynergy-" in e for e in check_sets.check_set(make(naming="own"))))
        self.assertTrue(any("freesynergy-" in e for e in check_sets.check_set(make(name="freesynergy-x"))))

    def test_variant_file_needed(self):
        d = make()
        (d / "icons.toml").write_text((d / "icons.toml").read_text() + 'variants = ["symbolic"]\n')
        self.assertTrue(any("variant file" in e for e in check_sets.check_set(d)))
        (d / "scalable/actions/a-symbolic.svg").write_text("<svg/>")
        self.assertEqual(check_sets.check_set(d), [])

    def test_purpose_required(self):
        d = make()
        (d / "icons.toml").write_text((d / "icons.toml").read_text().replace('purpose_de = "z"\n', ""))
        self.assertTrue(any("purpose_de missing" in e for e in check_sets.check_set(d)))

    def test_unlisted_svg(self):
        d = make()
        (d / "scalable/actions/extra.svg").write_text("<svg/>")
        self.assertTrue(any("not listed" in e for e in check_sets.check_set(d)))

    def test_repo_sets(self):
        self.assertEqual(check_sets.main(ROOT), 0)


if __name__ == "__main__":
    unittest.main()
