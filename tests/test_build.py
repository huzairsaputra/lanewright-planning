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
            self.assertEqual(zips, ["lanewright-backlog-check-1.0.2.zip", "lanewright-intake-1.0.1.zip",
                                    "lanewright-sprint-planner-1.0.2.zip", "lanewright-srs-1.0.0.zip"])
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


def skill_text(*parts):
    with open(os.path.join(build.SKILLS_DIR, *parts), encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")


def flat(text):
    return " ".join(text.split())


class TestDodContract(unittest.TestCase):
    """Labels other tools read: the plan's DoD proposals and the sign-off field (and the foundation rule)."""

    def test_plan_proposes_dod_items_that_may_not_apply(self):
        plan = skill_text("sprint-planner", "templates", "weekly-sprint-plan.md")
        self.assertIn("\n### 4.3 Definition of Done: items that may not apply\n", plan)
        self.assertIn("| 4.3 Butir Definition of Done yang mungkin tidak berlaku |", plan)
        self.assertIn("\n| DoD item | Why it may not apply | SRS reference |\n", plan)
        section = plan.split("### 4.3")[1].split("\n## 5")[0]
        self.assertNotIn("approved", section.split("-->")[1])  # the planner never approves
        self.assertIn("plan section 4.3", flat(skill_text("sprint-planner", "SKILL.md")))

    def test_sign_off_has_the_dod_field_after_overrides(self):
        report = skill_text("backlog-check", "templates", "backlog-check.md")
        self.assertIn("\nApproved by: ____   Role: ____   Date: ____   Overrides: ____\n"
                      "DoD not applicable (approved): ____\n", report)
        self.assertIn("| DoD not applicable (approved) / none | Butir DoD tidak berlaku (disetujui) / tidak ada |",
                      report)
        proposals = "\nDoD items proposed as not applicable (not approved until listed in the sign-off):\n"
        self.assertLess(report.index(proposals), report.index("\nApproved by: ____"))
        self.assertIn("An older report whose sign-off has no `DoD not applicable (approved)` field counts as "
                      "none approved", flat(skill_text("backlog-check", "SKILL.md")))

    def test_foundation_only_for_shared_module_and_tooling_roles(self):
        planner = flat(skill_text("sprint-planner", "SKILL.md"))
        self.assertIn('foundation (Indonesian "fondasi") may label only items owned by a shared-module or '
                      'tooling role', planner)
        self.assertIn('never called foundation, even when other items depend on it: write "first" or '
                      '"dependency of <ID>" instead', planner)
        self.assertNotIn("Foundations first", planner)
        plan = flat(skill_text("sprint-planner", "templates", "weekly-sprint-plan.md"))
        self.assertIn('"Foundation" (Indonesian "fondasi") labels only items owned by a shared-module or '
                      'tooling role', plan)


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
