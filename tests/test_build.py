import contextlib
import io
import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build  # noqa: E402


def skill_md(name="kit", version="1.0.0"):
    return ("---\nname: %s\ndescription: d\nversion: %s\n---\n\n# x\n" % (name, version)).encode()


ENTRIES = [
    ("LICENSE", b"MIT\n"),
    ("README.md", b"# kit\n"),
    ("SKILL.md", skill_md()),
    ("scripts/md_to_docx.py", b"print(1)\n"),
    ("templates/plan.md", b"plan\n"),
]


def replace(rel, data):
    return [e if e[0] != rel else (rel, data) for e in ENTRIES]


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args)


class TestCheck(unittest.TestCase):
    def test_clean_entries(self):
        fm, _, errors = build.check(ENTRIES)
        self.assertEqual(errors, [])
        self.assertEqual((fm["name"], fm["version"]), ("kit", "1.0.0"))

    def test_forbidden_word_fails(self):
        for word in ("Pemko", "diskominfotik", "SPPD", "Banda Aceh"):  # public-scan: allow
            _, _, errors = build.check(replace("templates/plan.md", ("Made for %s.\n" % word).encode()))
            self.assertTrue(any("forbidden word" in e for e in errors), word)

    def test_forbidden_is_whole_word(self):
        _, _, errors = build.check(replace("templates/plan.md", b"Acehnese pemkot jdihx\n"))
        self.assertEqual(errors, [])

    def test_nested_skill_md_bad_frontmatter_and_missing_files(self):
        self.assertTrue(build.check(ENTRIES + [("templates/SKILL.md", skill_md("other"))])[2])
        self.assertTrue(build.check(replace("SKILL.md", skill_md(version="v1")))[2])
        self.assertTrue(build.check([e for e in ENTRIES if e[0] != "LICENSE"])[2])

    def test_oversized_script(self):
        _, _, errors = build.check(replace("scripts/md_to_docx.py", b"#" * (build.MAX_SCRIPT + 1)))
        self.assertTrue(any("script limit" in e for e in errors))


class TestRealBuild(unittest.TestCase):
    def test_one_zip_per_skill(self):
        with tempfile.TemporaryDirectory() as dist:
            self.assertEqual(quiet(build.main, [], dist), 0)
            zips = sorted(os.listdir(dist))
            self.assertEqual(zips, ["lanewright-backlog-check-1.0.0.zip", "lanewright-intake-1.0.0.zip",
                                    "lanewright-sprint-planner-1.0.0.zip", "lanewright-srs-1.0.0.zip"])
            expected = {"lanewright-intake": ["docx_text.py"], "lanewright-srs": ["md_to_docx.py"],
                        "lanewright-sprint-planner": ["md_to_docx.py"],
                        "lanewright-backlog-check": ["backlog_check.py"]}
            for name in zips:
                with zipfile.ZipFile(os.path.join(dist, name)) as z:
                    names = z.namelist()
                skill_name = name.rsplit("-", 1)[0]
                self.assertEqual([n for n in names if n.endswith("SKILL.md")], ["SKILL.md"])
                self.assertEqual(sorted(n[8:] for n in names if n.startswith("scripts/")), expected[skill_name])
                for need in ("README.md", "LICENSE"):
                    self.assertIn(need, names)
                self.assertTrue(any(n.startswith("templates/") for n in names))

    def test_build_is_deterministic(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            quiet(build.main, [], a)
            quiet(build.main, [], b)
            for name in os.listdir(a):
                with open(os.path.join(a, name), "rb") as fa, open(os.path.join(b, name), "rb") as fb:
                    self.assertEqual(fa.read(), fb.read())

    def test_mapping_matches_skill_dirs(self):
        self.assertEqual(sorted(build.SKILLS), sorted(os.listdir(build.SKILLS_DIR)))


class TestInstall(unittest.TestCase):
    def test_install_and_uninstall_respect_marker(self):
        with tempfile.TemporaryDirectory() as dist, tempfile.TemporaryDirectory() as dest:
            foreign = os.path.join(dest, "lanewright-srs")
            os.makedirs(foreign)
            self.assertEqual(quiet(build.main, ["--install", dest], dist), 1)  # refuses a foreign dir
            os.rmdir(foreign)
            self.assertEqual(quiet(build.main, ["--install", dest], dist), 0)
            self.assertTrue(os.path.exists(os.path.join(dest, "lanewright-intake", "scripts", "docx_text.py")))
            self.assertTrue(os.path.exists(os.path.join(dest, "lanewright-srs", build.MARKER)))
            self.assertTrue(os.path.exists(os.path.join(dest, "lanewright-backlog-check", "scripts",
                                                        "backlog_check.py")))
            self.assertEqual(len(os.listdir(dest)), 4)
            self.assertEqual(quiet(build.main, ["--uninstall", dest], dist), 0)
            self.assertEqual(os.listdir(dest), [])


if __name__ == "__main__":
    unittest.main()
