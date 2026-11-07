"""Convert a Markdown file to a .docx that Word, LibreOffice and Google Docs open.

Usage:
  md_to_docx.py <in.md> <out.docx>   convert
  md_to_docx.py --self-test          convert a sample in memory and check the result

Supported: headings 1-4 (a first-line "# " heading becomes the Title style; deeper levels use
Heading4), paragraphs, **bold**, *italic*, `code`, [text](url) (written as "text (url)"), bullet and
numbered lists (nested by indentation), Markdown tables (bold header row, borders), "> " quotes,
fenced code blocks, a page break for a line <!-- pagebreak -->, other HTML comments dropped,
<br> as a line break, and a horizontal rule for ---, *** or ___.
Output is deterministic: fixed timestamps and file order, so the same input gives the same bytes.

Python 3.8+, standard library only. Reads no other file.
"""

import io
import re
import sys
import zipfile
from xml.sax.saxutils import escape

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
TEXT_WIDTH = 9638  # twips: A4 width 11906 minus two 2 cm margins
INLINE = re.compile(r"`([^`]+)`|\*\*(?=\S)(.+?)(?<=\S)\*\*|\*(?=[^\s*])([^*]+?)(?<=\S)\*")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BAD_XML = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RULE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")
PAGEBREAK = "<!-- pagebreak -->"


def runs(text, bold=False, italic=False):
    """[(text, bold, italic, code)] for inline Markdown."""
    out, pos = [], 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], bold, italic, False))
        if m.group(1) is not None:
            out.append((m.group(1), bold, italic, True))
        elif m.group(2) is not None:
            out += runs(m.group(2), True, italic)
        else:
            out += runs(m.group(3), bold, True)
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], bold, italic, False))
    return out


def run_xml(text, bold=False, italic=False, code=False):
    props = ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "")
    if code:
        props += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:shd w:val="clear" w:fill="F2F2F2"/>'
    rpr = "<w:rPr>%s</w:rPr>" % props if props else ""
    parts = []
    for i, line in enumerate(BAD_XML.sub("", text).split("\n")):
        if i:
            parts.append("<w:br/>")
        for j, chunk in enumerate(line.split("\t")):
            if j:
                parts.append("<w:tab/>")
            if chunk:
                parts.append('<w:t xml:space="preserve">%s</w:t>' % escape(chunk))
    return "<w:r>%s%s</w:r>" % (rpr, "".join(parts))


def inline_xml(text, bold=False):
    text = LINK.sub(r"\1 (\2)", text)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    return "".join(run_xml(t, b or bold, i, c) for t, b, i, c in runs(text))


def para(content, ppr=""):
    return "<w:p>%s%s</w:p>" % ("<w:pPr>%s</w:pPr>" % ppr if ppr else "", content)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


def table_xml(rows, header):
    cols = max(len(r) for r in rows)
    width = TEXT_WIDTH // cols
    border = '<w:%s w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
    borders = "".join(border % s for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/>'
           '<w:tblBorders>%s</w:tblBorders><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" '
           'w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>%s</w:tblGrid>'
           % (borders, '<w:gridCol w:w="%d"/>' % width * cols)]
    for i, row in enumerate(rows):
        is_head = header and i == 0
        out.append("<w:tr>%s" % ("<w:trPr><w:tblHeader/></w:trPr>" if is_head else ""))
        for cell in row + [""] * (cols - len(row)):
            shade = '<w:shd w:val="clear" w:fill="E7E6E6"/>' if is_head else ""
            out.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>%s</w:tc>'
                       % (width, shade, para(inline_xml(cell, bold=is_head), '<w:spacing w:after="0"/>')))
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out) + para("")  # Word needs a paragraph between adjacent tables


class Converter:
    def __init__(self):
        self.body, self.title, self.numbered_lists = [], None, 0
        self.list_num = None  # numId of the open numbered list

    def heading(self, level, text, first):
        style = "Title" if level == 1 and first else "Heading%d" % min(level, 4)
        if self.title is None:
            self.title = re.sub(r"[*`]", "", text)
        self.body.append(para(inline_xml(text), '<w:pStyle w:val="%s"/>' % style))

    def list_item(self, indent, marker, text):
        level = min(len(indent.replace("\t", "    ")) // 2, 3)
        if marker[0].isdigit():
            if self.list_num is None:
                self.numbered_lists += 1
                self.list_num = 2 + self.numbered_lists  # 1 = bullets, 2 = unused decimal base
            num = self.list_num
        else:
            num = 1
        ppr = ('<w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr>'
               % (level, num))
        self.body.append(para(inline_xml(text), ppr))

    def convert(self, markdown):
        lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        i, paragraph = 0, []

        def flush():
            if paragraph:
                self.body.append(para(inline_xml(" ".join(s.strip() for s in paragraph))))
                del paragraph[:]

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            item = LIST.match(line)
            if not item and stripped:
                self.list_num = None
            if stripped.startswith("```"):
                flush()
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    self.body.append(para(run_xml(lines[i], code=True), '<w:spacing w:after="0"/>'))
                    i += 1
            elif not stripped:
                flush()
            elif stripped == PAGEBREAK:
                flush()
                self.body.append(para('<w:r><w:br w:type="page"/></w:r>'))
            elif stripped.startswith("<!--"):
                while "-->" not in lines[i] and i + 1 < len(lines):
                    i += 1
            elif HEADING.match(stripped):
                flush()
                m = HEADING.match(stripped)
                self.heading(len(m.group(1)), m.group(2), first=not self.body)
            elif RULE.match(stripped):
                flush()
                self.body.append(para("", '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="auto"/></w:pBdr>'))
            elif stripped.startswith("|") and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]) \
                    or stripped.startswith("|") and not paragraph:
                flush()
                rows, header = [split_row(line)], False
                i += 1
                while i < len(lines) and lines[i].strip().startswith("|"):
                    if TABLE_SEP.match(lines[i]) and len(rows) == 1 and not header:
                        header = True
                    else:
                        rows.append(split_row(lines[i]))
                    i += 1
                self.body.append(table_xml(rows, header))
                continue
            elif item:
                flush()
                self.list_item(*item.groups())
            elif stripped.startswith(">"):
                flush()
                self.body.append(para(inline_xml(stripped.lstrip("> ")), '<w:ind w:left="567"/>'))
            else:
                paragraph.append(line)
            i += 1
        flush()
        return self


def numbering_xml(numbered_lists):
    def lvl(i, fmt, text):
        return ('<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="%s"/><w:lvlText w:val="%s"/>'
                '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" w:hanging="360"/></w:pPr></w:lvl>'
                % (i, fmt, text, 720 * (i + 1)))

    bullets = "".join(lvl(i, "bullet", ch) for i, ch in enumerate("•◦▪•"))
    decimals = "".join(lvl(i, "decimal", "%%%d." % (i + 1)) for i in range(4))
    nums = ['<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>',
            '<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>']
    for n in range(3, 3 + numbered_lists):  # one num per list so each restarts at 1
        nums.append('<w:num w:numId="%d"><w:abstractNumId w:val="1"/><w:lvlOverride w:ilvl="0">'
                    '<w:startOverride w:val="1"/></w:lvlOverride></w:num>' % n)
    return ('<w:numbering xmlns:w="%s"><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'
            '%s</w:abstractNum><w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="hybridMultilevel"/>%s'
            '</w:abstractNum>%s</w:numbering>' % (W_NS, bullets, decimals, "".join(nums)))


def styles_xml():
    def pstyle(sid, name, ppr="", rpr="", extra=""):
        return ('<w:style w:type="paragraph" w:styleId="%s"><w:name w:val="%s"/><w:basedOn w:val="Normal"/>'
                '<w:next w:val="Normal"/><w:qFormat/>%s<w:pPr>%s</w:pPr><w:rPr>%s</w:rPr></w:style>'
                % (sid, name, extra, ppr, rpr))

    head = '<w:keepNext/><w:keepLines/><w:spacing w:before="%d" w:after="120"/><w:outlineLvl w:val="%d"/>'
    color = '<w:color w:val="1F3864"/>'
    return (
        '<w:styles xmlns:w="%s"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" '
        'w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US"/></w:rPr>'
        '</w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr>'
        '</w:pPrDefault></w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
        % W_NS
        + pstyle("Title", "Title", '<w:spacing w:after="240"/>', '<w:b/><w:sz w:val="40"/><w:szCs w:val="40"/>' + color)
        + pstyle("Heading1", "heading 1", head % (360, 0), '<w:b/><w:sz w:val="32"/><w:szCs w:val="32"/>' + color)
        + pstyle("Heading2", "heading 2", head % (280, 1), '<w:b/><w:sz w:val="28"/><w:szCs w:val="28"/>' + color)
        + pstyle("Heading3", "heading 3", head % (240, 2), '<w:b/><w:sz w:val="24"/><w:szCs w:val="24"/>' + color)
        + pstyle("Heading4", "heading 4", head % (200, 3), '<w:b/><w:i/>' + color)
        + pstyle("ListParagraph", "List Paragraph", '<w:spacing w:after="60"/><w:ind w:left="720"/>',
                 extra='<w:uiPriority w:val="34"/>')
        + '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
          '<w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
          '<w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/>'
          '</w:tblCellMar></w:tblPr></w:style>'
          '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/>'
          '<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:tblPr><w:tblBorders>'
          + "".join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="auto"/>' % s
                    for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
        + "</w:tblBorders></w:tblPr></w:style></w:styles>")


def docx_bytes(markdown):
    c = Converter().convert(markdown)
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document xmlns:w="%s"><w:body>%s'
                '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" '
                'w:left="1134" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr></w:body></w:document>'
                % (W_NS, "".join(c.body)))
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    rel = '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/%s" Target="%s"/>'
    ct = "application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"
    parts = [
        ("[Content_Types].xml",
         xml + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
         '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
         '<Default Extension="xml" ContentType="application/xml"/>'
         '<Override PartName="/word/document.xml" ContentType="%s"/>'
         '<Override PartName="/word/styles.xml" ContentType="%s"/>'
         '<Override PartName="/word/numbering.xml" ContentType="%s"/>'
         '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
         '</Types>' % (ct % "document.main", ct % "styles", ct % "numbering")),
        ("_rels/.rels",
         xml + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         + rel % ("rId1", "officeDocument/2006/relationships/officeDocument", "word/document.xml")
         + rel % ("rId2", "package/2006/relationships/metadata/core-properties", "docProps/core.xml")
         + "</Relationships>"),
        ("word/document.xml", document),
        ("word/styles.xml", xml + styles_xml()),
        ("word/numbering.xml", xml + numbering_xml(c.numbered_lists)),
        ("word/_rels/document.xml.rels",
         xml + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         + rel % ("rId1", "officeDocument/2006/relationships/styles", "styles.xml")
         + rel % ("rId2", "officeDocument/2006/relationships/numbering", "numbering.xml")
         + "</Relationships>"),
        ("docProps/core.xml",
         xml + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
         'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
         'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>%s</dc:title>'
         '<dcterms:created xsi:type="dcterms:W3CDTF">2026-01-01T00:00:00Z</dcterms:created>'
         '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-01-01T00:00:00Z</dcterms:modified>'
         '</cp:coreProperties>' % escape(BAD_XML.sub("", c.title or ""))),
    ]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data.encode("utf-8"))
    return buf.getvalue()


SAMPLE = """# Rencana Sprint Mingguan

Dokumen ini **wajib** dibaca — *semua* peran; lihat `docs/sprints` dan [panduan](https://example.com).

## 1 Pendahuluan

- Butir pertama
  - Butir bertingkat
1. Langkah satu
2. Langkah dua

| Peran | SP |
|---|---|
| BE-1 | 10 |
| Kode \\| pipa | 6 |

<!-- pagebreak -->

<!-- a comment
over two lines -->

### 6.1 Sprint 1 — 17 – 23 Agustus 2026 (Hari 1–7)

---

# Lampiran A
"""


def self_test():
    import xml.etree.ElementTree as ET

    data = docx_bytes(SAMPLE)
    assert data == docx_bytes(SAMPLE), "output is not deterministic"
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        for need in ("[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/styles.xml",
                     "word/_rels/document.xml.rels", "docProps/core.xml"):
            assert need in names, need
        for name in names:
            ET.fromstring(z.read(name))
        doc = z.read("word/document.xml").decode("utf-8")
        styles = z.read("word/styles.xml").decode("utf-8")
    for sid in ("Title", "Heading1", "Heading2", "Heading3", "Heading4", "ListParagraph", "TableGrid"):
        assert 'w:styleId="%s"' % sid in styles, sid
    for want in ('w:val="Title"', 'w:val="Heading1"', 'w:val="Heading2"', "<w:b/>", "<w:i/>", "Consolas",
                 'w:type="page"', "<w:tbl>", "<w:tblHeader/>", "Kode | pipa", "Agustus 2026 (Hari 1–7)",
                 "panduan (https://example.com)", '<w:ilvl w:val="1"/>', '<w:numId w:val="3"/>', "<w:pBdr>"):
        assert want in doc, want
    assert "comment" not in doc
    print("self-test OK")


def main(argv):
    if argv == ["--self-test"]:
        self_test()
        return 0
    if len(argv) != 2 or argv[0].startswith("-"):
        sys.stderr.write(__doc__)
        return 2
    try:
        with open(argv[0], encoding="utf-8-sig") as f:
            data = docx_bytes(f.read())
        with open(argv[1], "wb") as f:
            f.write(data)
    except (OSError, UnicodeDecodeError) as e:
        sys.stderr.write("md_to_docx: %s\n" % e)
        return 1
    print("wrote %s (%d bytes)" % (argv[1], len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
