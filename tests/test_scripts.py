import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shared", "scripts")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCRIPTS, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


docx_text = load("docx_text")
md_to_docx = load("md_to_docx")

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def p(text, style=None):
    ppr = '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % style if style else ""
    return '<w:p>%s<w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (ppr, text)


def cell(text, props=""):
    return "<w:tc>%s%s</w:tc>" % ("<w:tcPr>%s</w:tcPr>" % props if props else "", p(text))


def test_docx():
    image = ('<w:p><w:r><w:drawing><wp:inline><wp:docPr id="1" name="Picture 1" descr="Complaint form"/>'
             '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData>'
             '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:blipFill>'
             '<a:blip r:embed="rId5"/></pic:blipFill></pic:pic></a:graphicData></a:graphic>'
             '</wp:inline></w:drawing></w:r></w:p>')
    table = ("<w:tbl><w:tr>%s%s%s</w:tr><w:tr>%s%s</w:tr></w:tbl>" % (
        cell("Actor"), cell("Need"), cell("Note"),
        cell("Citizen", '<w:gridSpan w:val="2"/>'), cell("Submit complaint")))
    body = p("Requirements", "Heading1") + p("The portal serves residents.") + table + image
    doc = '<w:document xmlns:w="%s" xmlns:wp="%s" xmlns:r="%s"><w:body>%s</w:body></w:document>' % (W, WP, R, body)
    rels = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId5" Type="%s/image" Target="media/image1.png"/></Relationships>' % R)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", doc)
        z.writestr("word/_rels/document.xml.rels", rels)
        z.writestr("word/media/image1.png", b"\x89PNG\r\n\x1a\n")
    buf.seek(0)
    return buf


def make_docx(body, core=None, styles=None):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", '<w:document xmlns:w="%s"><w:body>%s</w:body></w:document>' % (W, body))
        if core is not None:
            z.writestr("docProps/core.xml", core)
        if styles is not None:
            z.writestr("word/styles.xml", '<w:styles xmlns:w="%s">%s</w:styles>' % (W, styles))
    buf.seek(0)
    return docx_text.docx_to_text(buf)


def bold(text):
    return '<w:p><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % text


def numbered(text, bold_run=False):
    rpr = "<w:rPr><w:b/></w:rPr>" if bold_run else ""
    return ('<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="3"/></w:numPr></w:pPr>'
            '<w:r>%s<w:t>%s</w:t></w:r></w:p>' % (rpr, text))


class TestDocxText(unittest.TestCase):
    def test_bold_paragraph_before_normal_text_is_heading(self):
        out = make_docx(bold("Latar Belakang") + p("Normal text.") + bold("Bold line") + bold("Bold next")
                        + p("Text.") + bold("X" * 121) + p("Text.") + bold("Before table")
                        + "<w:tbl><w:tr>%s</w:tr></w:tbl>" % cell("A"))
        self.assertIn("## Latar Belakang\n\nNormal text.", out)
        self.assertIn("\nBold line\n", out)  # followed by bold text: not a heading
        self.assertIn("## Bold next", out)
        self.assertNotIn("## X", out)  # over 120 characters
        self.assertNotIn("## Before table", out)

    def test_list_items_one_line_each(self):
        out = make_docx(numbered("1. Satu") + numbered("Dua", bold_run=True) + p("Tiga", "ListParagraph")
                        + p("Empat", "ListBullet") + p("Lima", "Poin") + p("Normal text."),
                        styles='<w:style w:type="paragraph" w:styleId="Poin"><w:name w:val="Poin"/>'
                               '<w:pPr><w:numPr><w:numId w:val="4"/></w:numPr></w:pPr></w:style>')
        for line in ("- 1. Satu", "- Dua", "- Tiga", "- Empat", "- Lima"):
            self.assertIn("\n" + line + "\n", "\n" + out)

    def test_generator_default_metadata_skipped(self):
        core = ('<cp:coreProperties xmlns:cp="%s" xmlns:dc="%s" xmlns:dcterms="%s"><dc:title></dc:title>'
                '<dc:creator>python-docx</dc:creator><dcterms:created>2013-12-23T23:15:00Z</dcterms:created>'
                '</cp:coreProperties>' % (docx_text.NS["cp"], docx_text.NS["dc"], docx_text.NS["dcterms"]))
        out = make_docx(p("Body."), core)
        self.assertEqual(out, "Body.\n")
        real = core.replace("python-docx", "Planning unit").replace("2013-12-23", "2026-03-02")
        out = make_docx(p("Body."), real)
        self.assertIn("Author: Planning unit", out)
        self.assertIn("Created: 2026-03-02T23:15:00Z", out)

    def test_body_order_heading_table_image(self):
        out = docx_text.docx_to_text(test_docx())
        self.assertIn("# Requirements", out)
        self.assertIn("The portal serves residents.", out)
        self.assertIn("| Actor | Need | Note |", out)
        self.assertIn("| Citizen |  | Submit complaint |", out)  # gridSpan padded, no crash
        self.assertIn("[image 1: Complaint form]", out)
        self.assertLess(out.index("# Requirements"), out.index("| Actor"))
        self.assertLess(out.index("| Actor"), out.index("[image 1"))

    def test_not_a_docx(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "x.docx")
            with open(path, "wb") as f:
                f.write(b"not a zip")
            self.assertEqual(docx_text.main([path]), 1)

    def test_self_test(self):
        docx_text.self_test()


MARKDOWN = """# Rencana Sprint Mingguan

Paragraf dengan **tebal**, *miring* dan `kode` — 17 – 23 Agustus.

## 1 Pendahuluan

- Butir satu
- Butir dua

1. Langkah pertama

| Peran | Kapasitas |
|---|---|
| BE-1 | 10 SP |

<!-- pagebreak -->

### 6.1 Sprint 1

---
"""


class TestMdToDocx(unittest.TestCase):
    def test_round_trip(self):
        data = md_to_docx.docx_bytes(MARKDOWN)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            self.assertIn("word/numbering.xml", z.namelist())
            root = ET.fromstring(z.read("word/document.xml"))
        self.assertIsNotNone(root.find("{%s}body" % W))
        out = docx_text.docx_to_text(io.BytesIO(data))
        for want in ("# Rencana Sprint Mingguan", "## 1 Pendahuluan", "### 6.1 Sprint 1",
                     "- Butir satu", "- Butir dua", "- Langkah pertama",
                     "| Peran | Kapasitas |", "| BE-1 | 10 SP |",
                     "Paragraf dengan tebal, miring dan kode — 17 – 23 Agustus."):
            self.assertIn(want, out)

    def test_formatting_and_page_break(self):
        doc = zipfile.ZipFile(io.BytesIO(md_to_docx.docx_bytes(MARKDOWN))).read("word/document.xml").decode()
        for want in ('w:val="Title"', 'w:val="Heading2"', "<w:b/>", "<w:i/>", 'w:type="page"', "<w:pBdr>"):
            self.assertIn(want, doc)

    def test_deterministic_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "in.md")
            with open(src, "w", encoding="utf-8") as f:
                f.write(MARKDOWN)
            outs = []
            for n in (1, 2):
                out = os.path.join(tmp, "out%d.docx" % n)
                subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "md_to_docx.py"), src, out],
                               check=True, stdout=subprocess.DEVNULL)
                with open(out, "rb") as f:
                    outs.append(f.read())
            self.assertEqual(outs[0], outs[1])

    def test_self_test(self):
        md_to_docx.self_test()


if __name__ == "__main__":
    unittest.main()
