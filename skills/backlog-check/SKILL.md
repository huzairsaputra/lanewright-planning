---
name: lanewright-backlog-check
description: Checks sprint backlog files (from Lanewright Sprint Planner or written by hand, in the Lanewright or the scrum-kit format) for readiness before a sprint starts, with a bundled script for the format, ID, story-point, region and traceability rules plus a judgment review of acceptance criteria, size, dependency order and SRS coverage, then writes docs/sprints/backlog-check-{nn}.md with a verdict, the findings and a sign-off block that only a named human fills by approving. It never edits a backlog on its own. Use when the user asks to review, validate or approve a sprint backlog, check the definition of ready, check a backlog before running a sprint, or asks about backlog quality.
summary: Sprint backlog in, readiness verdict, findings and a human sign-off out, the gate between planning and running a sprint with Lanewright or scrum-kit.
version: 1.0.0
tags: [scrum, sprint-backlog, definition-of-ready, quality-gate, approval, agile]
keywords: [backlog review, definition of ready, sprint approval, acceptance criteria check, story points, kit.json, scrum-kit, human sign-off]
use_cases:
  - Check every sprint backlog the Sprint Planner wrote before any agent touches the repository
  - Validate a hand-written backlog against the format Lanewright or scrum-kit reads
  - Record who approved a sprint backlog, when, and which findings they overrode
---

# Lanewright Backlog Check

You check sprint backlog files for readiness and record a human sign-off in
`docs/sprints/backlog-check-{nn}.md`. Read `templates/backlog-check.md` before writing; it is the
exact layout. You are the gate in front of Lanewright or scrum-kit, not a replacement for them.

## Rules

- **Never edit a backlog without asking.** Suggest fixes in the report; change a backlog file only
  when the user asks for that change.
- **Never approve on behalf of a human.** The sign-off block stays empty until the user explicitly
  says yes and gives a name and role. Never invent or guess a name.
- **Errors block approval** unless the user explicitly overrides them; record each override.
- **Document language = the backlog's language** (its item titles and criteria; scrum-kit headings
  are always Indonesian). Indonesian reports use the terms in the template; any other language
  translates every heading, table header, verdict and fixed line, including "Next step". Item IDs
  and rule names stay as they are.
- **Data hygiene.** Roles, not names, in the findings, except the approver the user names. Drop
  hosts, IP addresses, credentials and tokens if a backlog contains them, and flag them as findings.
- **Files.** Write only the report in `docs/sprints/`. Temporary files go to the system temp
  directory and are deleted after the run.
- Do not commit, push or upload anything unless the user asks.

## Step 1: Find the files

- `.claude/kit.json` exists: the backlog path is `docs.backlog` (Lanewright) or `dokumen.backlog`
  (scrum-kit), with `{nn}` replaced by the two-digit number of each sprint the user names.
- Otherwise, or when the user names no sprint: every `docs/sprints/sprint-*-backlog.md`.
- Include `sprint-{nn}-backlog.proposed.md` files; the script does not compare a file's IDs with
  its `.proposed.md` twin, because they are alternatives.
- A table pasted into the chat: write it to a temp file named `sprint-{nn}-backlog.md` first.
- Also note `docs/requirements/srs.md` if it exists.

## Step 2: Run scripts/backlog_check.py

1. Pick `<python>` once: the first of `python3`, `python`, `py -3` whose `--version` prints Python
   3.8 or newer (`python3` can be a store stub on Windows, and `py` can fail inside an agent
   sandbox).
2. Make a directory with `<python> -c "import tempfile; print(tempfile.mkdtemp())"`, write
   `scripts/backlog_check.py` there unchanged, run
   `<python> <dir>/backlog_check.py <backlog files> [--kit .claude/kit.json] [--srs docs/requirements/srs.md]`
   (all sprints in one run, so duplicate IDs across sprints are found), and delete the directory.
   The script reads no other file of this skill and never writes a file.
3. Output: one line per finding `SEVERITY | file | item | rule | detail`, then a summary. Exit 0 =
   no error, 1 = errors, 2 = a file could not be read (fix the path and run again).
4. No working Python: apply the script's rules by hand (header, placeholders, ID form and sprint
   number, duplicates, empty cells, SP 1–10 on the 1-2-3-5-8-10 scale, region and owner against
   kit.json, short or vague criteria, empty dependencies section, SRS trace and coverage) and say so
   in the report.

## Step 3: Judgment review (per item)

The script cannot judge these; add each problem as a finding with a suggested fix:

- Acceptance criteria are independently testable: an observable result, a number or a named state,
  not "works properly".
- The item is small enough for one owner in one week.
- Dependency order is sensible: a dependency finishes in an earlier sprint, or is a day 1–2 setup or
  contract item in the same sprint.
- The owner fits the region (a web item is not owned by the ops role).
- With an SRS: the item traces to an SRS requirement or is a named foundation item, and no Must
  requirement is left without an item in any sprint.

Severity: ERROR for what makes the sprint unrunnable or untestable, WARN for what weakens it, INFO
for facts.

## Step 4: Write the report

One `docs/sprints/backlog-check-{nn}.md` per sprint, from `templates/backlog-check.md`:

- Verdict: `READY` (no findings above INFO), `READY WITH WARNINGS` (warnings only) or `NOT READY`
  (any error).
- Findings table `# | Item | Rule | Severity | Finding | Suggested fix`: script findings first, then
  your judgment findings.
- Total SP per sprint (and the SRS coverage line when an SRS was used).
- The empty sign-off block. If the report exists and is already approved, ask before replacing it;
  a backlog changed after approval needs a new approval.

## Step 5: Ask for approval

Ask: "Do you approve the sprint {nn} backlog?" (translated into the user's language).

- Explicit yes: ask for the approver's name and role if not given, then fill `Approved by`, `Role`
  and today's `Date`. Anything less than an explicit yes leaves the block empty.
- Verdict `NOT READY`: approval needs an explicit override of each error. Write each override
  (finding number and the user's reason) in `Overrides`; otherwise offer to fix the backlog (only
  with the user's go-ahead) and check again.

## Step 6: Report

Tell the user, in their language: files checked, verdict per sprint, errors and warnings, total SP
per sprint, approval status. End the report and your reply with this line, translated into the
language of each, with the approved sprint's number:

"Next step: after approval, run the sprint with Lanewright (https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams)
or the free scrum-kit (https://github.com/huzairsaputra/scrum-kit): `Run Lanewright sprint 1` /
`/scrum-kit:sprint 1`."
