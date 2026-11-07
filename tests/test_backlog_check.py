import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shared", "scripts",
                      "backlog_check.py")
spec = importlib.util.spec_from_file_location("backlog_check", SCRIPT)
backlog_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backlog_check)

LANEWRIGHT = """# Sprint 01 backlog

Sprint goal: A resident can register, sign in and see an empty dashboard.

Period: 3 – 9 August 2026

|  ID  | Item | Region / module |  Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| OPS-S01-01 | CI pipeline with lint and tests | ops | ops-dev | 3 | Every merge request runs lint and tests; a failing test blocks the merge |
| **BE-1-S01-01** | Database schema and migrations | api | module-dev | 5 | `migrate up` creates the users table; `migrate down` removes it without errors |
| BE-1-S01-02 | Registration API (F-01) | api | module-dev | 5 | F-01 AC1: POST `/api/register` with a new e-mail returns 201; AC2: a used e-mail returns 409 |
| FE-1-S01-01 | Sign-in screen (F-02) | web | web-dev | 3 | F-02 AC1: valid credentials open the dashboard within 2 s<br>AC2: a wrong password shows "Login failed" |

## Out of scope this sprint

- F-03 password reset — sprint 2

## Dependencies and risks

- BE-1-S01-02 needs BE-1-S01-01 (same owner)
- FE-1-S01-01 needs the API contract (day 1–2)
"""

SCRUM_KIT = """# Backlog Sprint 02

Sprint Goal: Warga dapat mengirim pengaduan dan melihat statusnya.

Periode: 10 – 16 Agustus 2026

| ID | Item | Wilayah / modul | PIC | SP | Kriteria penerimaan |
|---|---|---|---|---|---|
| BE-1-S02-01 | API pengaduan (F-03) | pengaduan | module-dev | 5 | F-03 AC1: POST `/api/pengaduan` mengembalikan 201 dan nomor tiket |
| FE-1-S02-01 | Layar status pengaduan (F-04) | web | web-dev | 3 | F-04 AC1: status "Diterima" tampil dalam 5 detik setelah dikirim |

## Ketergantungan dan risiko

- FE-1-S02-01 butuh BE-1-S02-01 (hari 1–2)
"""

KIT = {"docs": {"backlog": "docs/sprints/sprint-{nn}-backlog.md"},
       "regions": {"ops": {"role": "ops-dev"}, "api": {"role": "module-dev"}, "web": {"role": "web-dev"}}}
KIT_SCRUM = {"dokumen": {"backlog": "docs/sprints/sprint-{nn}-backlog.md"},
             "wilayah": {"modules": {"agen": "module-dev", "per_modul": True, "modul": ["pengaduan"]},
                         "web": {"agen": "web-dev"}}}

SRS = """# SRS

#### F-01 Registration

#### F-02 Sign in

#### F-05 Export

| ID | Category | Requirement | Target | Source | Source ID |
|---|---|---|---|---|---|
| NFR-01 | Security | Passwords hashed | bcrypt | [S1] | NFR-07 |
"""


class BacklogCheckTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write(self, name, text):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text if isinstance(text, str) else json.dumps(text))
        return path

    def run_cli(self, *args):
        p = subprocess.run([sys.executable, "-I", SCRIPT] + list(args), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        return p.returncode, p.stdout.decode("utf-8") + p.stderr.decode("utf-8")

    def assert_error(self, text, rule, name="sprint-01-backlog.md", *extra):
        code, out = self.run_cli(self.write(name, text), *extra)
        self.assertEqual(code, 1, out)
        self.assertIn("ERROR | ", out)
        self.assertIn("| %s |" % rule, out)
        self.assertIn("NOT READY", out)
        return out

    # valid files
    def test_valid_lanewright_passes(self):
        code, out = self.run_cli(self.write("sprint-01-backlog.md", LANEWRIGHT), "--kit", self.write("kit.json", KIT))
        self.assertEqual(code, 0, out)
        self.assertIn("| format | Lanewright", out)
        self.assertIn("| total-sp | 16 SP in 4 items", out)
        self.assertTrue(out.endswith("| READY\n"), out)

    def test_valid_scrum_kit_passes(self):
        code, out = self.run_cli(self.write("sprint-02-backlog.md", SCRUM_KIT), "--kit",
                                 self.write("kit.json", KIT_SCRUM))
        self.assertEqual(code, 0, out)
        self.assertIn("| format | scrum-kit", out)
        self.assertNotIn("WARN", out)

    def test_proposed_file_accepted_and_not_a_duplicate_of_its_twin(self):
        a = self.write("sprint-01-backlog.md", LANEWRIGHT)
        b = self.write("sprint-01-backlog.proposed.md", LANEWRIGHT)
        code, out = self.run_cli(a, b)
        self.assertEqual(code, 0, out)

    # one case per ERROR rule
    def test_header(self):
        out = self.assert_error(LANEWRIGHT.replace("  Owner |", " Assignee |"), "header")
        self.assertIn("first table header", out)

    def test_placeholder_cell_and_goal(self):
        self.assert_error(LANEWRIGHT.replace("CI pipeline with lint and tests", "<item title>"), "placeholder")
        out = self.assert_error(LANEWRIGHT.replace("Sprint goal: A resident", "Sprint goal: <one outcome> A"),
                                "placeholder")
        self.assertIn("Sprint goal line", out)
        self.assert_error(LANEWRIGHT.replace("Period: 3 – 9 August 2026", "Period:"), "placeholder")

    def test_id_format(self):
        out = self.assert_error(LANEWRIGHT.replace("OPS-S01-01 |", "OPS_S1_1 |"), "id")
        self.assertIn("does not match", out)

    def test_id_sprint_mismatch(self):
        out = self.assert_error(LANEWRIGHT.replace("OPS-S01-01 |", "OPS-S02-01 |"), "id")
        self.assertIn("differs from sprint 01", out)

    def test_duplicate_id_within_and_across_files(self):
        out = self.assert_error(LANEWRIGHT.replace("FE-1-S01-01 |", "BE-1-S01-02 |"), "id")
        self.assertIn("duplicate ID", out)
        other = self.write("sprint-01-backlog-extra.md", LANEWRIGHT)
        out = self.assert_error(LANEWRIGHT, "id", "sprint-01-backlog.md", other)
        self.assertIn("duplicate ID", out)

    def test_empty_cell(self):
        out = self.assert_error(LANEWRIGHT.replace("| ops | ops-dev |", "|  | ops-dev |"), "empty-cell")
        self.assertIn("Region / module is empty", out)

    def test_sp_13(self):
        out = self.assert_error(LANEWRIGHT.replace("| ops-dev | 3 |", "| ops-dev | 13 |"), "sp")
        self.assertIn("outside 1-10", out)

    def test_region_not_in_kit(self):
        out = self.assert_error(LANEWRIGHT.replace("| ops | ops-dev |", "| infra | ops-dev |"), "region",
                                "sprint-01-backlog.md", "--kit", self.write("kit.json", KIT))
        self.assertIn("'infra' is not a region", out)

    # warnings keep exit 0
    def test_warnings_exit_zero(self):
        text = (LANEWRIGHT.replace("| ops-dev | 3 |", "| ops-dev | 4 |")
                .replace("Every merge request runs lint and tests; a failing test blocks the merge", "CI is green")
                .replace("`migrate up` creates the users table; `migrate down` removes it without errors",
                         "The schema works properly for every module"))
        code, out = self.run_cli(self.write("sprint-01-backlog.md", text))
        self.assertEqual(code, 0, out)
        for rule in ("sp-scale", "criteria-short", "criteria-vague"):
            self.assertIn("WARN | ", out)
            self.assertIn("| %s |" % rule, out)
        self.assertIn("READY WITH WARNINGS", out)

    def test_owner_warning_and_deps_warning(self):
        text = LANEWRIGHT.replace("| api | module-dev | 5 | `migrate", "| api | Jane Doe | 5 | `migrate")
        text = text.split("## Dependencies and risks")[0] + "## Dependencies and risks\n\n- <dependency> — <fix>\n"
        code, out = self.run_cli(self.write("sprint-01-backlog.md", text), "--kit", self.write("kit.json", KIT))
        self.assertEqual(code, 0, out)
        self.assertIn("| owner |", out)
        self.assertIn("| deps | Dependencies and risks section is empty", out)

    # SRS
    def test_srs_coverage_and_trace(self):
        text = LANEWRIGHT.replace("Sign-in screen (F-02)", "Sign-in screen (F-02, UC-04)")
        code, out = self.run_cli(self.write("sprint-01-backlog.md", text), "--srs", self.write("srs.md", SRS))
        self.assertEqual(code, 0, out)
        self.assertIn("| coverage | not cited by any item: F-05\n", out)  # NFR-01 is not counted
        self.assertIn("| FE-1-S01-01 | trace | UC-04 is not defined in the SRS", out)
        self.assertNotIn("F-03", out)  # cited only outside the table
        self.assertNotIn("| trace | F-0", out)
        self.assertNotIn("NFR-07", out)  # a Source ID cell is not a definition and not cited

    def test_json_output(self):
        code, out = self.run_cli(self.write("sprint-01-backlog.md", LANEWRIGHT), "--json")
        self.assertEqual(code, 0, out)
        data = json.loads(out)
        self.assertEqual(data["verdict"], "READY")
        self.assertEqual(data["errors"], 0)

    # usage
    def test_unreadable_file_exit_2(self):
        code, out = self.run_cli(os.path.join(self.dir, "missing.md"))
        self.assertEqual(code, 2, out)
        self.assertEqual(self.run_cli()[0], 2)
        self.assertEqual(self.run_cli(self.write("sprint-01-backlog.md", LANEWRIGHT), "--kit")[0], 2)

    def test_self_test(self):
        with contextlib.redirect_stdout(io.StringIO()):
            backlog_check.self_test()
        code, out = self.run_cli("--self-test")
        self.assertEqual(code, 0, out)
        self.assertIn("self-test OK", out)


if __name__ == "__main__":
    unittest.main()
