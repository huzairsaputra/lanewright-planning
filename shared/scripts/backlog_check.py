"""Check sprint backlog files for readiness before a sprint starts.

Usage:
  backlog_check.py <backlog.md> [more.md ...] [--kit .claude/kit.json] [--srs docs/requirements/srs.md] [--json]
  backlog_check.py --self-test

Reads Lanewright backlogs (| ID | Item | Region / module | Owner | SP | Acceptance criteria |) and
scrum-kit backlogs (| ID | Item | Wilayah / modul | PIC | SP | Kriteria penerimaan |), including
.proposed.md files. Prints one line per finding, "SEVERITY | file | item-id or - | rule | detail",
then a summary line. Exit 0: no ERROR; 1: at least one ERROR; 2: usage error or unreadable file.
A file and its .proposed.md twin are alternatives, so IDs are not compared between the two.

Python 3.8+, standard library only. Never writes a file.
"""

import json
import os
import re
import sys
import tempfile

HEADERS = {
    "Lanewright": ["ID", "Item", "Region / module", "Owner", "SP", "Acceptance criteria"],
    "scrum-kit": ["ID", "Item", "Wilayah / modul", "PIC", "SP", "Kriteria penerimaan"],
}
ID_RE = re.compile(r"^[A-Za-z0-9]+(-[A-Za-z0-9]+)*-S(\d{2})-\d{2}$")
CODE_RE = re.compile(r"^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$")
FILE_SPRINT_RE = re.compile(r"sprint-(\d+)-backlog[^/\\]*\.md$", re.I)
# <!-- ... --> or <word ...>; <br> separates criteria, and "<500 ms" or "a < b" are not placeholders
PLACEHOLDER_RE = re.compile(r"<!--.*?-->|<(?!br\s*/?>)[^\W\d_][^<>]*>", re.I | re.S)
CODE_SPAN_RE = re.compile(r"`[^`]*`")
SEP_RE = re.compile(r"^:?-+:?$")
GOAL_RE = re.compile(r"^(?:[-*]\s+)?\**sprint goal\s*:\s*\**(.*)$", re.I)
PERIOD_RE = re.compile(r"^(?:[-*]\s+)?\**(?:period|periode)\s*:\s*\**(.*)$", re.I)
DEPS_RE = re.compile(r"^(#{1,6})\s+(?:dependencies and risks|ketergantungan dan risiko)\s*$", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s")
VAGUE_RE = re.compile(r"\b(works|working|properly|correctly|good|fast|quickly|nice|user-friendly|appropriate|etc"
                      r"|and so on|baik|benar|cepat|bagus|sesuai|dll|dan seterusnya)\b", re.I)
QUOTED_RE = re.compile(r"`[^`]+`|\"[^\"]+\"|“[^”]+”")
REQ = r"(?:F|NFR|CR|BR|UC)-\d{2}"
REQ_RE = re.compile(r"\b(F|NFR|CR|BR|UC)-(\d{2})\b")
RANGE_RE = re.compile(r"\b(F|NFR|CR|BR|UC)-(\d{2})\s*(?:–|—|\.\.)\s*(?:(F|NFR|CR|BR|UC)-)?(\d{2})\b")
SRS_HEADING_RE = re.compile(r"^#{1,6}\s+(?:\d+(?:\.\d+)*\.?\s+)?[*`]*(" + REQ + r")\b")
SP_SCALE = (1, 2, 3, 5, 8, 10)
MIN_CRITERIA = 25


class UsageError(Exception):
    pass


def read(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    except (OSError, UnicodeDecodeError) as e:
        raise UsageError("cannot read %s: %s" % (path, e))


def cells(line):
    """Cells of a Markdown table row; an escaped \\| stays inside its cell."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def clean_id(value):
    """A cell value without surrounding backticks and bold or italic markers."""
    return re.sub(r"^[`*_]+|[`*_]+$", "", value.strip()).strip()


def parse_backlog(text):
    """{format, rows: [(line no, cells)], goal, period, deps, first_header}. deps is None when the
    section is missing, False when it is empty (template placeholders count as empty)."""
    lines = text.splitlines()
    out = {"format": None, "rows": [], "goal": None, "period": None, "deps": None, "first_header": None}
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        m_goal, m_period = GOAL_RE.match(s), PERIOD_RE.match(s)
        if m_goal and out["goal"] is None:
            out["goal"] = m_goal.group(1).strip().strip("*").strip()
        elif m_period and out["period"] is None:
            out["period"] = m_period.group(1).strip().strip("*").strip()
        if s.startswith("|"):
            head = [" ".join(c.split()) for c in cells(s)]
            fmt = next((k for k, v in HEADERS.items() if head == v), None)
            if fmt is None:
                out["first_header"] = out["first_header"] or s
                while i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
                    i += 1
            else:
                out["format"] = out["format"] or fmt
                i += 1
                # the table ends at the first line that is not a row (a blank line or text)
                while i < len(lines) and lines[i].strip().startswith("|"):
                    row = cells(lines[i])
                    if not (any(row) and all(SEP_RE.match(c) for c in row if c)):
                        out["rows"].append((i + 1, row))
                    i += 1
                continue
        m_deps = DEPS_RE.match(s)
        if m_deps:
            level, body, j = len(m_deps.group(1)), [], i + 1
            while j < len(lines):
                h = HEADING_RE.match(lines[j].strip())
                if h and len(h.group(1)) <= level:
                    break
                body.append(lines[j])
                j += 1
            content = PLACEHOLDER_RE.sub("", "\n".join(body))
            out["deps"] = bool(re.sub(r"[\s\-*–—]", "", content))
        i += 1
    return out


def cited(text):
    """Requirement IDs a cell cites, ranges such as F-03–F-05 expanded."""
    ids = set("%s-%s" % m for m in REQ_RE.findall(text))
    for m in RANGE_RE.finditer(text):
        if m.group(3) in (None, m.group(1)):
            a, b = int(m.group(2)), int(m.group(4))
            if 0 < b - a <= 50:
                ids.update("%s-%02d" % (m.group(1), n) for n in range(a, b + 1))
    return ids


def srs_ids(text):
    """IDs the SRS defines: at the start of a heading, or as the first cell of a table row (so a
    Source ID column or an Affects column does not count as a definition)."""
    ids = set()
    for line in text.splitlines():
        s = line.strip()
        m = SRS_HEADING_RE.match(s)
        if m:
            ids.add(m.group(1))
        elif s.startswith("|"):
            first = clean_id(cells(s)[0])
            if re.fullmatch(REQ, first):
                ids.add(first)
    return ids


def load_kit(path):
    """{format, regions: {name: {role, per_module, modules}}} from a Lanewright or scrum-kit kit.json."""
    try:
        kit = json.loads(read(path))
    except ValueError as e:
        raise UsageError("%s is not valid JSON: %s" % (path, e))
    if isinstance(kit, dict) and isinstance(kit.get("regions"), (dict, list)):
        raw, keys, fmt = kit["regions"], ("role", "per_module", "modules"), "Lanewright"
    elif isinstance(kit, dict) and isinstance(kit.get("wilayah"), (dict, list)):
        raw, keys, fmt = kit["wilayah"], ("agen", "per_modul", "modul"), "scrum-kit"
    else:
        raise UsageError("%s has neither regions nor wilayah" % path)
    if isinstance(raw, list):
        raw = {str(r.get("name") or r.get("key") or r.get("nama")): r for r in raw if isinstance(r, dict)}
    regions = {}
    for name, r in raw.items():
        r = r if isinstance(r, dict) else {}
        mods = r.get(keys[2]) or []
        if isinstance(mods, dict):
            mods = list(mods)
        mods = [m if isinstance(m, str) else str(m.get("name") or m.get("nama")) for m in mods
                if isinstance(m, (str, dict))]
        regions[name] = {"role": r.get(keys[0]), "per_module": bool(r.get(keys[1])), "modules": mods}
    return {"format": fmt, "regions": regions}


def twin(path):
    return re.sub(r"\.proposed\.md$", ".md", os.path.normcase(os.path.abspath(path)), flags=re.I)


def check_row(add, path, fmt, no, row, m_file, seen, kit, srs):
    """Check one item row; returns (SP or 0, cited requirement IDs)."""
    item = clean_id(row[0]) or "line %d" % no
    if len(row) != 6:
        add("ERROR", path, item, "columns", "line %d has %d cells, expected 6 (a | inside a cell?)" % (no, len(row)))
        row = (row + [""] * 6)[:6]
    names = HEADERS[fmt]
    for name, value in zip(names, row):
        if value and PLACEHOLDER_RE.search(CODE_SPAN_RE.sub("", value)):
            add("ERROR", path, item, "placeholder", "%s still has a template placeholder" % name)
    rid = clean_id(row[0])
    m = ID_RE.match(rid)
    if not rid:
        add("ERROR", path, item, "id", "ID is empty")
    elif not m:
        add("ERROR", path, item, "id", "ID does not match <team code>-S<nn>-<seq>")
    elif m_file and int(m.group(2)) != int(m_file.group(1)):
        add("ERROR", path, item, "id", "S%s differs from sprint %s in the file name" % (m.group(2), m_file.group(1)))
    if rid:
        prev = seen.get(rid.upper())
        if prev and (prev[0] == path or twin(prev[0]) != twin(path)):
            add("ERROR", path, item, "id", "duplicate ID (also at %s line %d)" % prev)
        seen.setdefault(rid.upper(), (path, no))
    for name, value in zip(names[1:], row[1:]):
        if not value:
            add("ERROR", path, item, "empty-cell", "%s is empty" % name)
    sp, points = row[4].strip("* "), 0
    if sp:
        if not re.fullmatch(r"\d+", sp):
            add("ERROR", path, item, "sp", "SP %r is not a whole number" % sp)
        elif not 1 <= int(sp) <= 10:
            add("ERROR", path, item, "sp", "SP %s is outside 1-10" % sp)
        else:
            points = int(sp)
            if points not in SP_SCALE:
                add("WARN", path, item, "sp-scale", "SP %s is not one of 1, 2, 3, 5, 8, 10" % sp)
    region, owner = clean_id(row[2]), clean_id(row[3])
    if kit and region:
        regs = kit["regions"]
        hit = region if region in regs else next(
            (k for k, r in regs.items() if r["per_module"] and region in r["modules"]), None)
        if hit is None:
            add("ERROR", path, item, "region", "%r is not a region or module in kit.json" % region)
        roles = [regs[hit]["role"]] if hit else [r["role"] for r in regs.values()]
        if owner and owner not in roles and not CODE_RE.match(owner):
            add("WARN", path, item, "owner", "%r is neither the region's role nor a team code" % owner)
    crit = row[5]
    if crit:
        if len(crit) < MIN_CRITERIA:
            add("WARN", path, item, "criteria-short", "acceptance criteria under %d characters" % MIN_CRITERIA)
        vague = VAGUE_RE.search(crit)
        if vague and not re.search(r"\d", crit) and not QUOTED_RE.search(crit):
            add("WARN", path, item, "criteria-vague", "vague word %r and no number or quoted value" % vague.group(0))
    refs = set()
    for value in row[1:]:
        refs |= cited(value)
    if srs is not None:
        for ref in sorted(refs - srs):
            add("WARN", path, item, "trace", "%s is not defined in the SRS" % ref)
    return points, refs


def check(paths, kit_path=None, srs_path=None):
    """[(severity, file, item, rule, detail)]. Raises UsageError for unreadable input."""
    texts = [(p, read(p)) for p in paths]
    kit = load_kit(kit_path) if kit_path else None
    srs = srs_ids(read(srs_path)) if srs_path else None
    found, seen, all_cited = [], {}, set()

    def add(sev, path, item, rule, detail):
        found.append((sev, path, item or "-", rule, detail))

    for path, text in texts:
        b = parse_backlog(text)
        if b["format"] is None:
            got = ("first table header: %s" % b["first_header"]) if b["first_header"] else "no table found"
            add("ERROR", path, None, "header", "no Lanewright or scrum-kit backlog table header (%s)" % got)
            continue
        add("INFO", path, None, "format", b["format"])
        if kit and kit["format"] != b["format"]:
            add("WARN", path, None, "format", "kit.json is %s but the file is %s format" % (kit["format"], b["format"]))
        for label, value in (("Sprint goal", b["goal"]), ("Period", b["period"])):
            if not value:
                add("ERROR", path, None, "placeholder", "%s line missing or empty" % label)
            elif PLACEHOLDER_RE.search(CODE_SPAN_RE.sub("", value)):
                add("ERROR", path, None, "placeholder", "%s line still has a template placeholder" % label)
        m_file = FILE_SPRINT_RE.search(os.path.basename(path))
        total = 0
        for no, row in b["rows"]:
            points, refs = check_row(add, path, b["format"], no, row, m_file, seen, kit, srs)
            total += points
            all_cited |= refs
        if len(b["rows"]) > 3 and not b["deps"]:
            add("WARN", path, None, "deps", "Dependencies and risks section is %s with %d items"
                % ("empty" if b["deps"] is False else "missing", len(b["rows"])))
        add("INFO", path, None, "total-sp", "%d SP in %d items" % (total, len(b["rows"])))
    if srs is not None:
        wanted = sorted(i for i in srs if i.startswith(("F-", "CR-")))
        missing = [i for i in wanted if i not in all_cited]
        detail = ("not cited by any item: " + ", ".join(missing)) if missing else \
            "all %d F/CR requirements are cited" % len(wanted)
        add("INFO", srs_path, None, "coverage", detail)
    return found


def summary(found, nfiles):
    count = {s: sum(1 for f in found if f[0] == s) for s in ("ERROR", "WARN", "INFO")}
    verdict = "NOT READY" if count["ERROR"] else "READY WITH WARNINGS" if count["WARN"] else "READY"
    return count, verdict, "SUMMARY | %d file(s) | %d error(s), %d warning(s), %d info | %s" % (
        nfiles, count["ERROR"], count["WARN"], count["INFO"], verdict)


def run(argv):
    """(exit code, output text). Raises UsageError."""
    paths, opts, as_json = [], {"--kit": None, "--srs": None}, False
    args = list(argv)
    while args:
        a = args.pop(0)
        if a in opts:
            if not args:
                raise UsageError("%s needs a path" % a)
            opts[a] = args.pop(0)
        elif a == "--json":
            as_json = True
        elif a.startswith("-"):
            raise UsageError("unknown option %s" % a)
        else:
            paths.append(a)
    if not paths:
        raise UsageError("no backlog file given")
    found = check(paths, opts["--kit"], opts["--srs"])
    count, verdict, line = summary(found, len(paths))
    if as_json:
        keys = ("severity", "file", "item", "rule", "detail")
        text = json.dumps({"files": paths, "findings": [dict(zip(keys, f)) for f in found],
                           "errors": count["ERROR"], "warnings": count["WARN"], "verdict": verdict},
                          ensure_ascii=False, indent=2) + "\n"
    else:
        text = "".join("%s | %s | %s | %s | %s\n" % f for f in found) + line + "\n"
    return (1 if count["ERROR"] else 0), text


SAMPLE = """# Sprint 01 backlog

Sprint goal: A resident can sign in and see an empty dashboard.

Period: 3 – 9 August 2026

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| OPS-S01-01 | CI pipeline | ops | OPS | 3 | Pipeline runs lint and tests on every merge request; a failing test blocks merge |
| `BE-1-S01-01` | Login API (F-01) | api | BE-1 | 5 | F-01 AC1: POST `/api/login` with valid data returns 200 and a token |

## Dependencies and risks

- BE-1-S01-01 needs OPS-S01-01 (day 1–2)
"""


def self_test():
    d = tempfile.mkdtemp()
    try:
        def write(name, text):
            path = os.path.join(d, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return path
        good = write("sprint-01-backlog.md", SAMPLE)
        code, out = run([good])
        assert code == 0 and out.endswith("| READY\n") and "8 SP in 2 items" in out, out
        bad = write("sprint-02-backlog.md", SAMPLE.replace("| 5 |", "| 13 |").replace("goal: A", "goal: <x>"))
        code, out = run([bad])
        assert code == 1 and "| sp |" in out and "| placeholder |" in out and "S01 differs" in out, out
        srs = write("srs.md", "#### F-01 Login\n\n#### F-02 Logout\n\n| NFR-01 | Security |\n")
        code, out = run([good, "--srs", srs])
        assert code == 0 and "not cited by any item: F-02" in out, out
        kit = write("kit.json", json.dumps({"docs": {}, "regions": {"api": {"role": "module-dev"}}}))
        code, out = run([good, "--kit", kit])
        assert code == 1 and "'ops' is not a region" in out, out
        try:
            run([os.path.join(d, "missing.md")])
            raise AssertionError("missing file accepted")
        except UsageError:
            pass
    finally:
        for name in os.listdir(d):
            os.remove(os.path.join(d, name))
        os.rmdir(d)
    print("self-test OK")


def main(argv):
    if argv == ["--self-test"]:
        self_test()
        return 0
    try:
        code, text = run(argv)
    except UsageError as e:
        sys.stderr.write("backlog_check: %s\n\n%s" % (e, __doc__))
        return 2
    sys.stdout.buffer.write(text.encode("utf-8"))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
