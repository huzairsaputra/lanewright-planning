import contextlib
import hashlib
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
# Real shape: the modules are listed once at the top level; a per_modul region applies to each of them.
KIT_SCRUM = {"dokumen": {"backlog": "docs/sprints/sprint-{nn}-backlog.md"}, "modul": ["pengaduan"],
             "wilayah": {"modul": {"agen": "module-dev", "per_modul": True}, "web": {"agen": "web-dev"}}}
KIT_PER_MODULE = {"docs": {"backlog": "docs/sprints/sprint-{nn}-backlog.md"}, "modules": ["api", "portal"],
                  "regions": {"module": {"role": "module-dev", "per_module": True}, "tests": {"role": "qa-test-engineer"}}}

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

    def test_module_names_are_valid_regions_when_per_module(self):
        # Regression: a module listed at the top level of kit.json is a valid value for a per_module region.
        text = ("# Sprint 01 backlog\n\nSprint goal: A resident can register and sign in.\n\n"
                "Period: 3 – 9 August 2026\n\n"
                "| ID | Item | Region / module | Owner | SP | Acceptance criteria |\n|---|---|---|---|---|---|\n"
                "| BE-1-S01-01 | Registration API (F-01) | api | module-dev | 5 | F-01 AC1: POST `/api/register` returns 201 for a new e-mail |\n"
                "| FE-1-S01-01 | Sign-in screen (F-02) | portal | module-dev | 3 | F-02 AC1: valid credentials open the dashboard within 2 s |\n"
                "| QA-S01-01 | Registration tests (F-01) | tests | qa-test-engineer | 2 | F-01 AC1: the 201 and 409 cases are covered by passing tests |\n\n"
                "## Out of scope this sprint\n\n- none\n\n## Dependencies and risks\n\n- none\n")
        kit = self.write("kit.json", KIT_PER_MODULE)
        code, out = self.run_cli(self.write("sprint-01-backlog.md", text), "--kit", kit)
        self.assertEqual(code, 0, out)
        self.assertNotIn("| region |", out)
        code, out = self.run_cli(self.write("sprint-01-backlog.md", text.replace("| portal |", "| billing |")),
                                 "--kit", kit)
        self.assertEqual(code, 1)
        self.assertIn("'billing' is not a region or module", out)

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
        path = self.write("sprint-01-backlog.md", LANEWRIGHT)
        code, out = self.run_cli(path, "--json")
        self.assertEqual(code, 0, out)
        data = json.loads(out)
        self.assertEqual(data["verdict"], "READY")
        self.assertEqual(data["errors"], 0)
        self.assertEqual(data["file_verdicts"], [{"file": path, "errors": 0, "warnings": 0, "verdict": "READY"}])

    # verdict per file, placeholder-only official files
    def test_verdict_per_file_and_twin_judged_separately(self):
        official = self.write("sprint-01-backlog.md", LANEWRIGHT.replace("| ops-dev | 3 |", "| ops-dev | 4 |"))
        proposed = self.write("sprint-01-backlog.proposed.md", LANEWRIGHT)
        code, out = self.run_cli(official, proposed)
        self.assertEqual(code, 0, out)
        self.assertIn("VERDICT | %s | 0 error(s), 1 warning(s) | READY WITH WARNINGS\n" % official, out)
        self.assertIn("VERDICT | %s | 0 error(s), 0 warning(s) | READY\n" % proposed, out)
        self.assertTrue(out.endswith("| READY WITH WARNINGS\n"), out)  # SUMMARY stays the overall verdict
        self.assertNotIn("placeholder-official", out)  # the official file has real items

    def test_placeholder_official_when_proposal_has_items(self):
        rows = ("| BE-1-S01-01 | <item title> | <region key or module; no kit.json: api, web or ops> "
                "| <region's role, e.g. module-dev; no kit.json: BE-1> | 3 | <F-03 AC1: ...; AC2: ...> |\n")
        head = LANEWRIGHT.split("| OPS-S01-01")[0]
        proposed = self.write("sprint-01-backlog.proposed.md", LANEWRIGHT)
        for body in (rows, "<!--\n" + rows + "-->\n"):  # template row, or the row commented out
            official = self.write("sprint-01-backlog.md", head + body)
            code, out = self.run_cli(official, proposed, "--srs", self.write("srs.md", SRS))
            self.assertEqual(code, 1, out)
            self.assertIn("ERROR | %s | - | placeholder-official | only template placeholders, but %s has 4 items: "
                          "move the proposal into this file" % (official, proposed), out)
            self.assertIn("VERDICT | %s | 0 error(s), 0 warning(s) | READY\n" % proposed, out)
            self.assertIn("VERDICT | %s | " % official, out)
            self.assertNotIn("F-03", out)  # a template example is not a citation
        self.assertIn("| placeholder | the table has no item rows", out)
        # without a proposal with items there is nothing to move
        code, out = self.run_cli(self.write("sprint-01-backlog.md", head + rows))
        self.assertEqual(code, 1, out)
        self.assertNotIn("placeholder-official", out)

    # vague wording, broad citations
    def test_vague_when_only_digits_are_references(self):
        for crit in ("F-01 AC1: the page works properly (BR-03, NFR-02, A-04)",
                     "BE-1-S01-02 berfungsi untuk semua modul F-01",
                     "Halaman pendaftaran berjalan dengan baik di portal"):
            out = self.run_cli(self.write("sprint-01-backlog.md", LANEWRIGHT.replace(
                "Every merge request runs lint and tests; a failing test blocks the merge", crit)))[1]
            self.assertIn("| OPS-S01-01 | criteria-vague |", out, crit)
        out = self.run_cli(self.write("sprint-01-backlog.md", LANEWRIGHT.replace(
            "Every merge request runs lint and tests; a failing test blocks the merge",
            "F-01 AC1: the page works properly and loads within 2 s")))[1]
        self.assertNotIn("criteria-vague", out)

    def test_broad_citation_and_weak_coverage(self):
        text = LANEWRIGHT.replace("Every merge request runs lint and tests; a failing test blocks the merge",
                                  "F-01, F-02, F-05 and NFR-01: every merge request runs lint and tests")
        code, out = self.run_cli(self.write("sprint-01-backlog.md", text), "--srs", self.write("srs.md", SRS))
        self.assertEqual(code, 0, out)
        self.assertIn("WARN | %s | OPS-S01-01 | broad-citation | cites 4 requirement IDs"
                      % os.path.join(self.dir, "sprint-01-backlog.md"), out)
        self.assertIn("| coverage | all 3 F/CR requirements are cited, 1 only weakly\n", out)
        self.assertIn("| coverage | weakly covered, cited only by items with more than 3 requirement IDs: F-05\n", out)
        code, out = self.run_cli(self.write("sprint-01-backlog.md", LANEWRIGHT.replace(
            "Registration API (F-01)", "Registration API (F-01–F-03)")))
        self.assertNotIn("broad-citation", out)  # three IDs are not broad

    # fingerprint
    def test_sha256_same_for_crlf_and_lf(self):
        lf = LANEWRIGHT.encode("utf-8")
        crlf = lf.replace(b"\n", b"\r\n")
        self.assertNotEqual(lf, crlf)
        self.assertEqual(backlog_check.fingerprint(crlf), backlog_check.fingerprint(lf))
        self.assertEqual(backlog_check.fingerprint(lf), hashlib.sha256(lf).hexdigest())
        hashes, path = [], os.path.join(self.dir, "sprint-01-backlog.md")
        for data in (lf, crlf):
            with open(path, "wb") as f:
                f.write(data)
            code, out = self.run_cli(path)
            self.assertEqual(code, 0, out)
            line = next(x for x in out.splitlines() if "| sha256 |" in x)
            self.assertEqual(line.rsplit(" | ", 1)[0], "INFO | %s | - | sha256" % path)
            hashes.append(line.rsplit(" | ", 1)[1])
        self.assertEqual(hashes[0], hashes[1])
        self.assertRegex(hashes[0], r"^[0-9a-f]{64}$")

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
