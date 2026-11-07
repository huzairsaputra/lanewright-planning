"""Build one zip per skill, dist/<name>-<version>.zip, and refuse a skill that breaks the upload rules.

Run:
  py -I build.py                    build every zip
  py -I build.py --install [DIR]    build, then install every skill for a local trial
                                    (default DIR: ~/.claude/skills)
  py -I build.py --uninstall [DIR]  remove the skills a previous --install wrote

Each zip holds skills/<dir>/ (SKILL.md at the zip root, templates, README.md, LICENSE) plus the
shared scripts that skill lists in SKILLS, under scripts/. The zip name and version come from the
frontmatter of that SKILL.md.
"""

import json
import os
import re
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(ROOT, "skills")
SHARED = os.path.join(ROOT, "shared", "scripts")
DIST = os.path.join(ROOT, "dist")
DEFAULT_SKILLS = os.path.join(os.path.expanduser("~"), ".claude", "skills")
MARKER = ".lanewright-dev-install"  # only directories carrying this file are replaced or removed
# skill directory -> shared scripts copied into its zip as scripts/<file>
SKILLS = {
    "intake": ["docx_text.py"],
    "srs": ["md_to_docx.py"],
    "sprint-planner": ["md_to_docx.py"],
    "backlog-check": ["backlog_check.py"],
}
REQUIRED = ("SKILL.md", "README.md", "LICENSE")
MAX_SCRIPT = 20 * 1024
MAX_FILES = 200
MAX_CHARS = 6_000_000
# The author's organisation and real project names (whole words) must never ship.
FORBIDDEN = re.compile(r"\b(pemko|banda|aceh|diskominfo\w*|saleum|simagang|jdih|sppd|pppk)\b", re.IGNORECASE)


def collect(directory):
    files = []
    for d, dirs, names in os.walk(directory):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for n in sorted(names):
            if not n.endswith(".pyc"):
                files.append(os.path.join(d, n))
    return files


def frontmatter(text):
    """Top-level `key: value` scalars of a leading --- block."""
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    return dict(re.findall(r"^([A-Za-z_]+):[ \t]*(\S[^\r\n]*?)[ \t]*$", m.group(1), re.M))


def skill(entries):
    """(frontmatter of the root SKILL.md, errors). A zip is one skill: Agensi turns every other
    SKILL.md, at any depth, into a separate skill."""
    fm, errors = None, []
    for rel, data in entries:
        if rel == "SKILL.md":
            fm = frontmatter(data.decode("utf-8"))
        elif rel.endswith("/SKILL.md"):
            errors.append("%s: only the root SKILL.md may exist (Agensi would list this as another skill)" % rel)
    if fm is None:
        return None, errors + ["no SKILL.md at the skill root"]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", fm.get("name", "")):
        errors.append("SKILL.md has no valid name in its frontmatter")
    if not fm.get("description"):
        errors.append("SKILL.md has no description in its frontmatter")
    if not re.fullmatch(r"\d+\.\d+\.\d+", fm.get("version", "")):
        errors.append("SKILL.md version %r is not X.Y.Z" % fm.get("version"))
    return fm, errors


def entries_for(name):
    """[(zip path, bytes)] for one skill directory plus its shared scripts, and errors."""
    base = os.path.join(SKILLS_DIR, name)
    real_base = os.path.realpath(base) + os.sep
    entries, errors = [], []
    for path in collect(base):
        rel = os.path.relpath(path, base).replace(os.sep, "/")
        if not os.path.realpath(path).startswith(real_base):
            errors.append("%s/%s resolves outside the skill directory" % (name, rel))
            continue
        with open(path, "rb") as f:
            entries.append((rel, f.read()))
    for script in SKILLS[name]:
        rel = "scripts/" + script
        if any(e[0] == rel for e in entries):
            errors.append("%s/%s: keep scripts only in shared/scripts/" % (name, rel))
            continue
        with open(os.path.join(SHARED, script), "rb") as f:
            entries.append((rel, f.read()))
    return sorted(entries), errors


def check(entries):
    """(frontmatter, characters, errors) for the entries of one zip."""
    errors, chars = [], 0
    for rel, data in entries:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append("%s is not UTF-8 text" % rel)
            continue
        chars += len(text)
        for no, line in enumerate(text.splitlines(), 1):
            m = FORBIDDEN.search(line)
            if m:
                errors.append("%s:%d: forbidden word '%s'" % (rel, no, m.group(0)))
        if rel.endswith(".json"):
            try:
                json.loads(text)
            except ValueError as e:
                errors.append("%s is not valid JSON: %s" % (rel, e))
        if rel.startswith("scripts/") and len(data) > MAX_SCRIPT:
            errors.append("%s is %d bytes, over the %d-byte script limit" % (rel, len(data), MAX_SCRIPT))
    names = [e[0] for e in entries]
    errors += ["%s is missing" % r for r in REQUIRED if r not in names]
    if len(entries) > MAX_FILES:
        errors.append("%d files, over %d" % (len(entries), MAX_FILES))
    if chars > MAX_CHARS:
        errors.append("%d characters, over %d" % (chars, MAX_CHARS))
    fm, skill_errors = skill(entries)
    return fm, chars, errors + skill_errors


def check_all():
    """[(dir, entries, frontmatter, chars)] and errors (prefixed with the skill directory)."""
    results, errors = [], []
    for name in sorted(SKILLS):
        entries, errs = entries_for(name)
        fm, chars, check_errors = check(entries)
        errors += ["%s: %s" % (name, e) for e in errs + check_errors]
        results.append((name, entries, fm, chars))
    return results, errors


def build(entries, chars, fm, dist=None):
    out = os.path.join(dist or DIST, "%s-%s.zip" % (fm["name"], fm["version"]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, data in entries:
            info = zipfile.ZipInfo(rel, date_time=(2026, 1, 1, 0, 0, 0))  # fixed time: same input, same zip
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    for rel, data in entries:
        print("%8d  %s" % (len(data), rel))
    print("%d files, %d characters -> %s (%d bytes)\n" % (len(entries), chars, out, os.path.getsize(out)))
    return out


def install(entries, fm, dest):
    """The whole skill goes to <dest>/<name>/, the layout a buyer's agent receives."""
    target = os.path.join(dest, fm["name"])
    if os.path.exists(target) and not os.path.exists(os.path.join(target, MARKER)):
        return ["%s exists and was not written by --install; remove it yourself" % target]
    if os.path.exists(target):
        shutil.rmtree(target)
    for rel, data in entries:
        path = os.path.join(target, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    open(os.path.join(target, MARKER), "w").close()
    print("installed %s" % target)
    return []


def uninstall(fm, dest):
    if not fm or not fm.get("name"):
        return
    target = os.path.join(dest, fm["name"])
    if os.path.exists(os.path.join(target, MARKER)):
        shutil.rmtree(target)
        print("removed %s" % target)
    elif os.path.exists(target):
        print("kept %s (not written by --install)" % target)


def main(argv, dist=None):
    mode = argv[0] if argv else None
    if mode not in (None, "--install", "--uninstall") or len(argv) > 2:
        sys.stderr.write(__doc__)
        return 2
    dest = argv[1] if len(argv) == 2 else DEFAULT_SKILLS
    results, errors = check_all()
    if mode == "--uninstall":
        for _, _, fm, _ in results:
            uninstall(fm, dest)
        return 0
    if errors:
        sys.stderr.write("BUILD FAILED\n  " + "\n  ".join(errors) + "\n")
        return 1
    for _, entries, fm, chars in results:
        build(entries, chars, fm, dist)
    if mode == "--install":
        for _, entries, fm, _ in results:
            errors += install(entries, fm, dest)
        if errors:
            sys.stderr.write("INSTALL FAILED\n  " + "\n  ".join(errors) + "\n")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
