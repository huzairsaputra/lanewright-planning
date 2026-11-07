"""Print the text of a .docx as Markdown-ish text, in body order.

Usage:
  docx_text.py <file.docx>     print the document
  docx_text.py --self-test     build a small .docx in memory and check the output

Output: core properties (title, author, created) when present and not a known generator default,
then the body: headings as # .. ###### (Title and Heading1..6 styles), a short all-bold paragraph
followed by normal text as "## ", list paragraphs (Word numbering or List* styles) as "- ",
tables as Markdown tables (cell paragraphs joined with " / ", merged cells padded), and a line
"[image N: <description, title or nearby caption>]" for every embedded image.

Python 3.8+, standard library only. Reads no other file.
"""

import io
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {
    "w": W,
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "v": "urn:schemas-microsoft-com:vml",
    "o": "urn:schemas-microsoft-com:office:office",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
}
MAX_PART = 200 * 1024 * 1024  # refuse absurdly large XML parts (zip bombs)
GENERATOR_DEFAULTS = {"Author": "python-docx", "Created": "2013-12-23T23:15:00Z"}  # python-docx template values
MAX_BOLD_HEADING = 120


def q(tag):
    prefix, name = tag.split(":")
    return "{%s}%s" % (NS[prefix], name)


def wval(el, attr="val"):
    return el.get("{%s}%s" % (W, attr)) if el is not None else None


def read_xml(z, name):
    try:
        info = z.getinfo(name)
    except KeyError:
        return None
    if info.file_size > MAX_PART:
        raise ValueError("%s is too large (%d bytes)" % (name, info.file_size))
    return ET.fromstring(z.read(name))


def style_names(z):
    """(styleId -> lower-case style name, styleIds whose definition carries Word numbering).
    Built-in names stay English in localized documents."""
    root = read_xml(z, "word/styles.xml")
    names, numbered = {}, set()
    if root is not None:
        for s in root.iter(q("w:style")):
            name = s.find(q("w:name"))
            names[wval(s, "styleId")] = (wval(name) or "").lower()
            if s.find("w:pPr/w:numPr", NS) is not None:
                numbered.add(wval(s, "styleId"))
    return names, numbered


def core(z):
    root = read_xml(z, "docProps/core.xml")
    lines = []
    if root is not None:
        for label, tag in (("Title", "dc:title"), ("Author", "dc:creator"), ("Created", "dcterms:created")):
            el = root.find(q(tag))
            value = (el.text or "").strip() if el is not None else ""
            if value and GENERATOR_DEFAULTS.get(label) != value:
                lines.append("%s: %s" % (label, value))
    return lines


class Reader:
    def __init__(self, z):
        self.styles, self.numbered = style_names(z)
        self.images = 0

    def style(self, p):
        sid = wval(p.find("w:pPr/w:pStyle", NS))
        return self.styles.get(sid, (sid or "").lower())

    def text(self, p):
        out = []
        for el in p.iter():
            if el.tag == q("w:t") and el.text:
                out.append(el.text)
            elif el.tag == q("w:tab"):
                out.append("\t")
            elif el.tag in (q("w:br"), q("w:cr")):
                out.append(" ")
        return re.sub(r"[ \t]+", " ", "".join(out)).strip()

    def bold(self, p):
        """True when every run with visible text is bold by direct formatting (bold styles are not resolved)."""
        def on(r):
            b = r.find("w:rPr/w:b", NS)
            return b is not None and wval(b) not in ("0", "false", "off")
        runs = [r for r in p.iter(q("w:r")) if any((t.text or "").strip() for t in r.iter(q("w:t")))]
        return bool(runs) and all(on(r) for r in runs)

    def image_labels(self, p):
        labels = []
        for el in p.iter():
            if el.tag == q("wp:docPr"):
                labels.append((el.get("descr") or el.get("title") or "").strip())
            elif el.tag == q("v:imagedata"):
                labels.append((el.get(q("o:title")) or "").strip())
        return labels

    def is_caption(self, p):
        return p is not None and p.tag == q("w:p") and self.style(p) == "caption"

    def paragraph(self, p, prev=None, nxt=None, plain=False, following=None):
        """Lines for one paragraph; prev/next blocks give a nearby caption for images, following is the
        next block with text (a bold-only paragraph before normal text is a heading)."""
        style, text = self.style(p), self.text(p)
        lines = []
        if text and plain:
            lines.append(text)
        elif text:
            heading = re.fullmatch(r"heading ?([1-6])", style)
            if style == "title":
                lines.append("# " + text)
            elif heading:
                lines.append("#" * int(heading.group(1)) + " " + text)
            elif (p.find("w:pPr/w:numPr", NS) is not None or style.startswith("list")
                  or wval(p.find("w:pPr/w:pStyle", NS)) in self.numbered):
                level = wval(p.find("w:pPr/w:numPr/w:ilvl", NS)) or "0"
                lines.append("  " * min(int(level) if level.isdigit() else 0, 5) + "- " + text)
            elif (len(text) <= MAX_BOLD_HEADING and self.bold(p) and following is not None
                  and following.tag == q("w:p") and not self.bold(following)):
                lines.append("## " + text)
            else:
                lines.append(text)
        for label in self.image_labels(p):
            if not label:
                near = [b for b in (nxt, prev) if self.is_caption(b)]
                label = self.text(near[0]) if near else (text or "no caption")
            self.images += 1
            lines.append("[image %d: %s]" % (self.images, label))
        return lines

    def cell_text(self, tc):
        parts = []
        for el in tc:
            if el.tag == q("w:p"):
                parts.extend(self.paragraph(el, plain=True))
            elif el.tag == q("w:tbl"):
                for row in self.rows(el):
                    parts.extend(c for c in row if c)
            elif el.tag == q("w:sdt") and el.find("w:sdtContent", NS) is not None:
                parts.append(self.cell_text(el.find("w:sdtContent", NS)))
        return " / ".join(x for x in parts if x)

    def rows(self, tbl):
        rows = []
        for tr in tbl.findall("w:tr", NS):
            row = []
            for tc in tr.findall("w:tc", NS):
                merge = tc.find("w:tcPr/w:vMerge", NS)
                continued = merge is not None and wval(merge) != "restart"
                row.append("" if continued else self.cell_text(tc))
                span = wval(tc.find("w:tcPr/w:gridSpan", NS)) or "1"
                row.extend([""] * (max(int(span), 1) - 1 if span.isdigit() else 0))
            rows.append(row)
        return rows

    def table(self, tbl):
        rows = [r for r in self.rows(tbl) if r]
        if not rows:
            return []
        width = max(len(r) for r in rows)
        cell = lambda c: c.replace("|", "\\|")  # noqa: E731
        out = []
        for i, r in enumerate(rows):
            out.append("| " + " | ".join(cell(c) for c in r + [""] * (width - len(r))) + " |")
            if i == 0:
                out.append("|" + "---|" * width)
        return out

    def blocks(self, parent):
        """Body-order paragraphs and tables, unwrapping content controls."""
        out = []
        for el in parent:
            if el.tag in (q("w:p"), q("w:tbl")):
                out.append(el)
            elif el.tag == q("w:sdt"):
                content = el.find("w:sdtContent", NS)
                if content is not None:
                    out.extend(self.blocks(content))
        return out

    def body(self, root):
        body = root.find("w:body", NS)
        blocks = self.blocks(body) if body is not None else []
        texts = [self.text(b) if b.tag == q("w:p") else None for b in blocks]  # None = table
        out = []
        for i, b in enumerate(blocks):
            if b.tag == q("w:tbl"):
                lines = self.table(b)
            else:
                prev = blocks[i - 1] if i else None
                nxt = blocks[i + 1] if i + 1 < len(blocks) else None
                following = next((x for x, t in zip(blocks[i + 1:], texts[i + 1:]) if t != ""), None)
                lines = self.paragraph(b, prev, nxt, following=following)
            if lines:
                out.append("\n".join(lines))
        return out


def docx_to_text(source):
    """source: a path or a binary file object."""
    with zipfile.ZipFile(source) as z:
        root = read_xml(z, "word/document.xml")
        if root is None:
            raise ValueError("not a Word document: word/document.xml is missing")
        head = core(z)
        blocks = Reader(z).body(root)
    return "\n\n".join(([("\n".join(head))] if head else []) + blocks) + "\n"


def _sample_docx():
    def p(text, style=None, extra=""):
        ppr = '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % style if style else ""
        return '<w:p>%s<w:r><w:t xml:space="preserve">%s</w:t></w:r>%s</w:p>' % (ppr, text, extra)

    drawing = ('<w:r><w:drawing><wp:inline><wp:docPr id="1" name="Picture 1" descr="Login screen"/>'
               '</wp:inline></w:drawing></w:r>')
    plain_img = '<w:r><w:drawing><wp:inline><wp:docPr id="2" name="Picture 2"/></wp:inline></w:drawing></w:r>'
    tc = lambda t, pr="": "<w:tc>%s%s</w:tc>" % ("<w:tcPr>%s</w:tcPr>" % pr if pr else "", p(t))  # noqa: E731
    table = ("<w:tbl><w:tr>%s%s</w:tr><w:tr>%s</w:tr><w:tr>%s%s</w:tr></w:tbl>" % (
        tc("Actor"), tc("Need", '<w:vMerge w:val="restart"/>'),
        tc("Merged | wide", '<w:gridSpan w:val="2"/>'),
        tc("Officer"), tc("", "<w:vMerge/>")))
    numbered = ('<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>'
                '<w:r><w:t>First item</w:t></w:r></w:p>')
    body = (p("Kebutuhan Sistem", "Judul1") + p("Intro paragraph with ") + numbered + table
            + '<w:p>%s</w:p>' % drawing + '<w:p>%s</w:p>' % plain_img + p("Figure 2. Dashboard", "Caption"))
    doc = ('<w:document xmlns:w="%s" xmlns:wp="%s"><w:body>%s</w:body></w:document>' % (W, NS["wp"], body))
    styles = ('<w:styles xmlns:w="%s"><w:style w:type="paragraph" w:styleId="Judul1"><w:name w:val="heading 1"/>'
              '</w:style><w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/></w:style>'
              '</w:styles>' % W)
    props = ('<cp:coreProperties xmlns:cp="%s" xmlns:dc="%s" xmlns:dcterms="%s"><dc:title>Sample</dc:title>'
             '<dc:creator>Writer</dc:creator></cp:coreProperties>' % (NS["cp"], NS["dc"], NS["dcterms"]))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", styles)
        z.writestr("docProps/core.xml", props)
    buf.seek(0)
    return buf


def self_test():
    out = docx_to_text(_sample_docx())
    for want in ("Title: Sample", "Author: Writer", "# Kebutuhan Sistem", "Intro paragraph with",
                 "- First item", "| Actor | Need |", "| Merged \\| wide |  |", "| Officer |  |",
                 "[image 1: Login screen]", "[image 2: Figure 2. Dashboard]"):
        assert want in out, "missing %r in:\n%s" % (want, out)
    assert out.index("# Kebutuhan") < out.index("| Actor") < out.index("[image 1"), out
    print("self-test OK")


def main(argv):
    if argv == ["--self-test"]:
        self_test()
        return 0
    if len(argv) != 1 or argv[0].startswith("-"):
        sys.stderr.write(__doc__)
        return 2
    try:
        text = docx_to_text(argv[0])
    except (OSError, zipfile.BadZipFile, ValueError, ET.ParseError) as e:
        sys.stderr.write("docx_text: %s: %s\n" % (argv[0], e))
        return 1
    sys.stdout.buffer.write(text.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
