import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_svg  # noqa: E402

OK = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M1 1h2"/></svg>'


def svg(inner: str, attrs: str = "") -> bytes:
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" {attrs}>{inner}</svg>'.encode()


class CheckSvg(unittest.TestCase):
    def bad(self, data, needle):
        problems = check_svg.check_bytes(data)
        self.assertTrue(any(needle in p for p in problems), problems)

    def test_clean(self):
        self.assertEqual(check_svg.check_bytes(OK), [])

    def test_script(self):
        self.bad(svg("<script>alert(1)</script>"), "script")

    def test_event_attribute(self):
        self.bad(svg('<path d="M0 0" onclick="x()"/>'), "event attribute")
        self.bad(svg("", 'onload="x()"'), "event attribute")

    def test_data_attribute_with_on_prefix_is_not_an_event(self):
        self.assertEqual(check_svg.check_bytes(svg('<path d="M0 0" only_selected="1"/>')), [])

    def test_external_href(self):
        self.bad(svg('<image href="https://example.org/a.png"/>'), "external reference")
        self.bad(svg('<use xlink:href="other.svg#a"/>'), "external reference")

    def test_local_fragment_allowed(self):
        self.assertEqual(check_svg.check_bytes(svg('<defs><path id="a" d="M0 0"/></defs><use href="#a"/>')), [])

    def test_external_url(self):
        self.bad(svg('<path fill="url(http://x.org/g)"/>'), "external url()")
        self.bad(svg("<style>@import url(http://x.org/a.css);</style>"), "<style>")

    def test_foreign_object(self):
        self.bad(svg("<foreignObject><div/></foreignObject>"), "foreignobject")

    def test_javascript_uri(self):
        self.bad(svg('<a href="javascript:alert(1)"><path d="M0 0"/></a>'), "external reference")

    def test_size_limit(self):
        self.bad(OK + b" " * 70000, "too large")

    def test_entity(self):
        self.bad(b'<!DOCTYPE svg [<!ENTITY a "b">]><svg xmlns="http://www.w3.org/2000/svg"/>', "ENTITY")

    def test_not_xml_and_wrong_root(self):
        self.bad(b"<svg", "well-formed")
        self.bad(b"<html/>", "not <svg>")


class OurSet(unittest.TestCase):
    def test_freesynergy_set_is_clean(self):
        root = Path(__file__).resolve().parent.parent / "sets"
        for f in check_svg.collect([str(root)]):
            self.assertEqual(check_svg.check_bytes(f.read_bytes()), [], str(f))


if __name__ == "__main__":
    unittest.main()
