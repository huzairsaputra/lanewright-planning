---
name: lanewright-intake
description: Turns raw project input (PDF, DOCX, Markdown, text, images, screenshots, chat exports, a local folder, a Google Drive folder, pasted text or a single line describing the idea) into one evidence file, docs/requirements/intake.md, where every fact carries a kind tag and a source citation, gaps are listed, a short interview fills what is missing and anything still unknown is labelled ASSUMPTION. Use when the user wants to collect, read or summarize project documents before writing requirements, asks to start a new project or change request from loose material, or asks for an intake, requirements gathering or a fact base for an SRS.
summary: Raw project material in, one cited evidence file out, with gaps, a two-round interview and explicit assumptions, ready for an SRS and a sprint plan.
version: 1.0.0
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
  `[S3 "Keterangan" image 4]`, `[S4 2026-03-02 14:05]` (chat message), `[interview Q3]`.
- **Assumptions are labelled.** Anything you or the user decide without a source is
  `ASSUMPTION A-nn`, never a plain fact.
- **The user's language.** Write the file in the language of the user's request (Indonesian
  request, Indonesian file); translate the template headings. Quote sources in their own language.
- **Personal and government data stay out.** Record field names and kinds of data, never values:
  no ID numbers, phone numbers, addresses, health or financial details of individuals, passwords,
  tokens or internal URLs. Authors and stakeholders are recorded by role unless the user asks for
  names. Write nothing outside `docs/requirements/` unless the user asks.
- **Ask before overwriting.** If `intake.md` exists, ask: update it (keep the source numbers, add
  new sources after them), replace it, or write `intake.proposed.md` beside it.
- Do not commit, push or upload anything unless the user asks.

## Step 1: Collect the sources

Number every source `S1`, `S2`, ... in the order you read them.

| Input | How to read it |
|---|---|
| PDF, image, screenshot | Read natively. Images: describe what the screen or diagram shows. If you cannot read images, list each one under Gaps ("image not read: ...") |
| DOCX | Run `scripts/docx_text.py` (below). It prints headings, lists, tables and `[image N: ...]` markers in body order |
| Markdown, text, CSV, chat export (WhatsApp/Telegram text or JSON) | Read as text. Chat messages are cited by date and time |
| Other formats (XLSX, PPTX, ODT) | Read them if your tools can; otherwise list them under Gaps |
| Local folder | Walk it recursively. Skip `.git`, `.venv`, `node_modules`, `vendor`, `__pycache__`, build output and binaries (archives, executables, media other than images). Show the user the file list before reading more than 30 files |
| Google Drive folder or link | Use your Google Drive connector (list, then read or export each file). No connector: say so and ask the user to download the folder or paste the files |
| Pasted text | One source, type "pasted text", dated today |
| A single line ("Portal layanan publik digital terpadu (Superapps)") | One source, type "one-line brief". Expect a thin result and go to the interview |

For each source fill the Sources table: type, date (from the document, else "unknown"), author (role
or organisation unit as printed, else "unknown"), notes (pages read, what was skipped, quality).

### Running scripts/docx_text.py

1. Pick `<python>` once: the first of `python3`, `python`, `py -3` whose `--version` prints Python
   3.8 or newer (`python3` can be a store stub on Windows, and `py` can fail inside an agent
   sandbox).
2. Write `scripts/docx_text.py` from this skill, unchanged, to a temporary file outside the
   repository; run `<python> <temp>/docx_text.py <file.docx>`; delete the temporary file when all
   DOCX files are read. The script reads no other file of this skill.
3. No working Python: read the DOCX with your own tools if you can, else list it under Gaps.

Citations from DOCX output use the nearest heading (`[S1 §2.3]` or `[S1 "Ruang Lingkup"]`) and
image markers (`[S1 image 3]`).

## Step 2: Extract facts

Go through every source once, in order. Each fact is one line: `- [kind] statement [citation]`.
Group facts by kind, in this order:

`goal`, `actor`, `feature`, `rule` (business rule), `data`, `screen` (screen or design), `integration`,
`constraint` (legal, hardware, stack, hosting), `nfr` (non-functional), `timeline` (deadlines,
milestones), `budget`, `stakeholder`.

- One fact per line, stated as the source states it. Do not merge two sources into one fact; when
  they agree, cite both `[S1 p.3; S2 §4]`. When they conflict, write both and add a Gap.
- Screens: one `screen` fact per screen, with the caption and the visible fields, buttons and
  states (`[S3 "Keterangan" image 4]`).
- Laws, regulations and standards the sources name are `constraint` facts with the exact title.

## Step 3: Detect the project kind

- **New application**: the sources describe a system that does not exist yet.
- **Change to an existing system**: a request letter, change note, bug list, "add/fix/change X in
  the current app", or screenshots of a running system with requested changes.

Write the kind and the one-line reason with its citation. Mixed input: pick the dominant kind and
note the rest. The SRS skill uses this to pick its outline.

## Step 4: Gaps

List what an SRS and a sprint plan need but the sources do not say. Always check: goal and success
measure, actors and their permissions, core features, data owned and shared, integrations, legal
and security constraints, hosting and stack, deadline, team (roles, people), budget, acceptance
owner. Each gap: what is missing, and why it matters.

## Step 5: Interview (at most two rounds)

Interview when the input is thin (one line, a short paste) or a key item is missing: actors, core
features, deadline, team.

- At most two rounds, three to six questions per round, most important first.
- Every question carries a proposed default: "Who signs off the release? (default: the head of the
  requesting unit)". The user may answer "defaults" to accept them all.
- Number questions `Q1`, `Q2`, ... across both rounds. Answers become facts cited `[interview Qn]`.
- After two rounds, or if the user stops answering or the run is non-interactive, every open item
  becomes `ASSUMPTION A-nn` with the default you proposed, listed in the Assumptions section.

## Step 6: Write and report

Write `docs/requirements/intake.md` from `templates/intake.md`. Then tell the user, in their
language: number of sources, facts per kind, gaps, assumptions, the project kind, and any source you
could not read. End your reply and the file with:

"Next step: Lanewright SRS turns this into a requirements document."
