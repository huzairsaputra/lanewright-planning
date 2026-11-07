---
name: lanewright-intake
description: Turns raw project input (PDF, DOCX, Markdown, text, images, screenshots, chat exports, a local folder, a Google Drive folder, pasted text or a single line describing the idea) into one evidence file, docs/requirements/intake.md, where every fact carries a kind tag and a source citation, gaps are listed, a short interview fills what is missing and anything still unknown is labelled ASSUMPTION. Use when the user wants to collect, read or summarize project documents before writing requirements, asks to start a new project or change request from loose material, or asks for an intake, requirements gathering or a fact base for an SRS.
summary: Raw project material in, one cited evidence file out, with gaps, a two-round interview and explicit assumptions, ready for an SRS and a sprint plan.
version: 1.0.1
tags: [requirements, intake, business-analysis, srs, project-planning, documentation]
keywords: [requirements gathering, evidence file, source citation, stakeholder interview, project intake, change request, docx extraction, assumptions log]
use_cases:
  - Read a folder of PDFs, Word files and screenshots and get every requirement-relevant fact with its page or section
  - Start from a single sentence and reach a usable fact base through a short interview with proposed defaults
  - Tell a new application from a change to an existing system before anyone writes an SRS
---

# Lanewright Intake

You turn raw project input into `docs/requirements/intake.md`: a cited evidence file that an SRS
and a sprint plan can be built from. You never invent a fact. Read `templates/intake.md` before
writing; it is the exact layout.

## Rules

- **No fact without a citation.** Every fact line ends with its source: `[S2 p.7]`, `[S1 §3.2]`,
  `[S1 "Heading"]` (Markdown or DOCX heading without a number), `[S1]` (one-line brief or any source
  without sections), `[S3 "Keterangan" image 4]`, `[S4 2026-03-02 14:05]` (chat message),
  `[interview Q3]`, and `[request]` for the user's own words. `[request]` gets the row
  `S0 | the user's request | request | <date> | user` in the Sources table; S0 is not counted.
- **Assumptions are labelled.** Anything you or the user decide without a source is
  `ASSUMPTION A-nn`, never a plain fact.
- **Document language = the language of the source material**, not of the request. Mixed sources:
  the language of most source text; a one-line input: that line's language. The user may override
  it. Translate every heading, table header and fixed line, including "Next step" and the fixed
  phrases "no answer — default taken", "not asked", "round 2 skipped", "to confirm", "date to
  confirm", "not described in the sources", "no source" and "context, not sources"; quote sources
  in their own language.
  Keywords stay English: kind tags, `ASSUMPTION`, and `Kind:` with its value (Step 3).
- **Data hygiene.** Keep API paths, ports and field names. Drop hosts, IP addresses, credentials,
  tokens and personal values (ID numbers, phone numbers, addresses, health or financial details).
  Record people by role when the source gives one, otherwise by the handle the source uses.
- **Files.** Write only in `docs/requirements/` unless the user asks. Temporary script copies go to
  the system temp directory and are deleted after the run, even when the user said not to change
  files outside the repository.
- **No answers.** If a question round gets no answers (no reply, or a non-interactive run), take
  every proposed default, record each as `ASSUMPTION A-nn`, write "no answer — default taken" in
  its Answer cell and skip the next round.
- **Ask before overwriting.** If `intake.md` exists, ask: update it (keep the source numbers, add
  new sources after them), replace it, or write `intake.proposed.md` beside it.
- Do not commit, push or upload anything unless the user asks.

## Step 1: Collect the sources

Number every source `S1`, `S2`, ... in the order you read them.

| Input | How to read it |
|---|---|
| PDF | First that works: your native PDF reading; `pdftotext -layout <file> -` if installed; Python `pypdf` if importable; else ask the user for a text or DOCX export. Write the method in the source's Notes; multi-column tables may need realigning |
| Image, screenshot | Read natively and describe what the screen or diagram shows. If you cannot read images, list each one under Gaps ("image not read: ...") |
| DOCX | Run `scripts/docx_text.py` (below). It prints headings, lists, tables and `[image N: ...]` markers in body order |
| Markdown, text, CSV, chat export (WhatsApp/Telegram text or JSON) | Read as text. Chat messages are cited by date and time |
| Code and config files | Sources like any other (`.claude/kit.json` included), except when the user gave only a brief inside an existing repository (below). A file that only generates another source (same text): cite the generated document only |
| Other formats (XLSX, PPTX, ODT) | Read them if your tools can; otherwise list them under Gaps |
| Local folder | Walk it recursively. Skip `.git`, `.venv`, `node_modules`, `vendor`, `__pycache__`, build output and binaries (archives, executables, media other than images). Show the user the file list before reading more than 30 files |
| Google Drive folder or link | Use your Google Drive connector (list, then read or export each file). No connector: say so and ask the user to download the folder or paste the files |
| Pasted text | One source, type "pasted text", dated today |
| A single line ("Portal layanan publik digital terpadu (Superapps)") | One source, type "one-line brief", cited `[S1]`. Expect a thin result and go to the interview |

For each source fill the Sources table: type, date (from the document, else "unknown"), author (role
or organisation unit as printed, else "unknown"), notes (pages read, reading method, what was
skipped, quality).

**A brief inside an existing repository.** When the user gives only a brief (a line or pasted
text) and you are working inside a repository that already has files, ask once, before extracting
facts: "Are the files in this repository (code, config, CI, project rules such as CLAUDE.md)
sources for this intake? (default: no, context only)". Yes: read them as sources. No, or no answer:
do not cite them; list them under "Context, not sources" below the Sources table, and do not let
them switch the project kind from new application to change request (Step 3).

### Running scripts/docx_text.py

1. Pick `<python>` once: the first of `python3`, `python`, `py -3` whose `--version` prints Python
   3.8 or newer (`python3` can be a store stub on Windows, and `py` can fail inside an agent
   sandbox).
2. Make a directory with `<python> -c "import tempfile; print(tempfile.mkdtemp())"`, write
   `scripts/docx_text.py` there unchanged, run `<python> <dir>/docx_text.py <file.docx>`, and delete
   the directory when all DOCX files are read. The script reads no other file of this skill.
3. No working Python: read the DOCX with your own tools if you can, else list it under Gaps.

Citations from DOCX output use the nearest heading (`[S1 §2.3]` or `[S1 "Ruang Lingkup"]`) and
image markers (`[S1 image 3]`).

## Step 2: Extract facts

Go through every source once, in order. Each fact is one line: `- [kind] statement [citation]`.
Group facts by kind, in this order:

`goal`, `actor`, `feature`, `priority` (a must-have for launch), `rule` (business rule), `data`,
`screen` (screen or design), `integration`, `constraint` (legal, hardware, stack, hosting), `nfr`
(non-functional), `timeline` (deadlines, milestones), `budget`, `team` (people, roles,
availability), `stakeholder`.

- One fact per line, stated as the source states it. Do not merge two sources into one fact; when
  they agree, cite both `[S1 p.3; S2 §4]`. When they conflict, write both and add a Gap.
- Screens: one `screen` fact per screen, with the caption and the visible fields, buttons and
  states (`[S3 "Keterangan" image 4]`).
- Laws, regulations and standards the sources name are `constraint` facts with the exact title.

## Step 3: Detect the project kind

- **New application**: the sources describe a system that does not exist yet.
- **Change to an existing system**: a request letter, change note, bug list, "add/fix/change X in
  the current app", or screenshots of a running system with requested changes.

Write the line `Kind: new-application` or `Kind: change-request` (always these English keywords; a
label in the document language may follow), then the one-line reason with its citation. Mixed
input: pick the dominant kind and note the rest. Only sources decide the kind: repository files
listed as context, not sources, never make it a change request. The SRS skill reads this line to
pick its outline.

## Step 4: Gaps

List what an SRS and a sprint plan need but the sources do not say. Always check: goal and success
measure, actors and their permissions, core features and which are must-haves at launch, data
owned and shared, integrations, legal and security constraints, hosting and stack, deadline, team
(roles, people, availability), budget, acceptance owner. Each gap: what is missing, and why it
matters.

## Step 5: Interview (at most two rounds)

Interview when the input is thin (one line, a short paste) or a key item is missing: actors, core
features, deadline, team.

- At most two rounds. Rank the gaps by impact: actors and must-have features first, then deadline
  and team, then the rest. Ask the top 6 per round.
- Round 1 always asks "Which 3–5 features must exist at launch?" (default: the core flows you
  infer, shown as a proposal). Record the answer as `priority` facts cited `[interview Qn]`.
  No answer: like every other default, the proposed must-haves become `ASSUMPTION A-nn` and the
  intake has no `priority` facts, so the SRS rule "every `priority` fact has a Must requirement"
  has nothing to check and the SRS sets priorities by its own rule.
- Every question carries a proposed default: "Who signs off the release? (default: the head of the
  requesting unit)". The user may answer "defaults" to accept them all.
- Number questions `Q1`, `Q2`, ... across both rounds. Answers become facts cited `[interview Qn]`.
- After two rounds, or when the user stops answering, every open item becomes `ASSUMPTION A-nn`
  with the default you proposed. Gaps not asked also become assumptions, marked "not asked", each
  with a proposed default. A skipped round 2 is the one line "Round 2 skipped: no answers in round 1".

## Step 6: Write and report

Write `docs/requirements/intake.md` from `templates/intake.md`. Then tell the user, in their
language: number of sources, facts per kind, gaps, assumptions, the project kind, and any source you
could not read. End the file and your reply with this line, translated into the language of each:

"Next step: Lanewright SRS turns this into a requirements document."
