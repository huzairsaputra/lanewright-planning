---
name: lanewright-srs
description: Turns a cited evidence file (docs/requirements/intake.md) into a Software Requirements Specification in IEEE 29148 style, docs/requirements/srs.md plus a Word copy srs.docx, with numbered functional and non-functional requirements, testable acceptance criteria, data and business rules, use cases, integrations, open questions and a traceability table back to the sources; for a change to an existing system it writes a change-request SRS instead. Use when the user asks for an SRS, a requirements document, a functional specification or a change-request specification, or wants the intake turned into requirements.
summary: Evidence file in, traceable SRS out (Markdown and DOCX), every requirement testable and cited, assumptions never silently promoted to requirements.
version: 1.0.0
tags: [requirements, srs, ieee-29148, business-analysis, specification, documentation]
keywords: [software requirements specification, functional requirements, acceptance criteria, traceability matrix, use cases, change request, non-functional requirements, docx export]
use_cases:
  - Turn an intake file into an SRS whose every requirement cites a source page or an interview answer
  - Write a change-request SRS for an existing system with current behaviour, requested change and impact per change
  - Hand stakeholders a Word copy of the SRS for review while the Markdown stays the working source
---

# Lanewright SRS

You write `docs/requirements/srs.md` and `docs/requirements/srs.docx` from the evidence in
`docs/requirements/intake.md`. Every requirement traces to a source or to a labelled assumption.

## Rules

- **Never invent a requirement.** Each requirement cites intake citations (`[S2 p.7]`,
  `[interview Q3]`, `[request]`) or `ASSUMPTION A-nn`. A requirement that exists only because of an
  assumption keeps that label; never upgrade it to a plain requirement silently.
- **Testable acceptance criteria.** Observable, with numbers or concrete examples ("given ...
  when ... then ..."). Never "works well", "user-friendly", "fast".
- **Document language = the language of the source material**: the intake's language (it already
  follows its sources); without an intake, the language of most source text, or of the line for a
  one-line input. The user may override it. Translate every heading, table header and fixed line
  (including "Next step"); keep the IDs (`F-01`, `NFR-01`, `BR-01`, `UC-01`, `CR-01`) and the word
  ASSUMPTION as they are.
- **Data hygiene.** Keep API paths, ports and field names. Drop hosts, IP addresses, credentials,
  tokens and personal values. Record people by role when the source gives one, otherwise by the
  handle the source uses.
- **Files.** Write only in `docs/requirements/` unless the user asks. Temporary script copies go to
  the system temp directory and are deleted after the run, even when the user said not to change
  files outside the repository.
- **No answers.** If a question gets no answer (no reply, or a non-interactive run), take the
  proposed default, record it as `ASSUMPTION A-nn` with "no answer — default taken", and go on.
- **Ask before overwriting** `srs.md` or `srs.docx`: update, replace, or write
  `srs.proposed.md` / `srs.proposed.docx` beside them.
- Do not commit, push or upload anything unless the user asks.

## Step 1: Load the evidence

Read `docs/requirements/intake.md` in full: project kind, language, facts, gaps, interview,
assumptions.

No intake file: offer two options and wait for the choice (default: 2).

1. Run Lanewright Intake first (recommended for documents or folders).
2. Do a short intake inline: read the input the user gives, list sources `S1..`, cited facts by
   kind, gaps and at most one interview round of three to six questions with proposed defaults,
   then save it as `docs/requirements/intake.md` in the intake layout (sources table, facts grouped
   by kind, gaps, interview, assumptions) before writing the SRS.

## Step 2: Pick the outline

- Project kind **new application** → `templates/srs.md`.
- Project kind **change to an existing system** → `templates/change-request.md`.
- Kind missing or mixed: ask the user; default to the dominant kind in the facts.

Read the chosen template in full before drafting.

## Step 3: Draft

Put the intake facts in these sections:

| Intake facts | New application (`srs.md`) | Change request (`change-request.md`) |
|---|---|---|
| goal, stakeholder | 1 Introduction | 1 Introduction |
| actor | 2.2 Actors and user classes | 2.2 Actors affected |
| constraint | 2.3 Constraints | 2.3 Constraints |
| assumptions A-nn | 2.4 Assumptions (same numbers) | 2.4 Assumptions (same numbers) |
| feature, screen | 3 Functional requirements, 6 Use cases | 2.1 Context (today), 3 Requested changes, 6 Use cases changed |
| nfr | 4 Non-functional requirements | 4 Non-functional impact |
| data, rule | 5 Entities and business rules | 5 Entities and business rules |
| integration | 7 External interfaces | 7 External interfaces |
| open gaps, conflicts, unmentioned NFR categories | 8 Open questions | 8 Open questions |

Requirements (`F-nn`, or `CR-nn` in a change request):

- One behaviour per requirement: "The system shall ..." (in the document language), two to five
  acceptance criteria `AC1`, `AC2`, ... A `CR` also gives current behaviour and impact (screens,
  data, API).
- **Priority:** the source's priority when it gives one; otherwise Must for core flows of the first
  release, Should for supporting features, Could for nice-to-haves. A sourced requirement with an
  assumed detail keeps its priority and names the assumption (`A-03`); only a requirement that
  exists only because of an assumption is at most Should.
- **Source ID:** when the source numbers its requirements (`F-01`, `NFR-05`, `UC-01`), fill the
  Source ID field or column so the mapping is explicit. Change requests are `CR-nn` and never reuse
  the existing system's IDs.
- Screens from the intake become requirements for the behaviour they show, cited to the image.

Non-functional requirements: include a category (security, privacy, performance, availability,
accessibility, maintainability, ...) only when a source or the user mentions it; any other category
goes to Open questions, not into the requirements. Use the measurable target the source gives; when
it gives none, write "Target: to be confirmed" and add it to Open questions; never make a number up.

Open questions: one row per assumption, listing every requirement that rests on it, then one row
per open gap or conflict.

## Step 4: Check before saving

- Every requirement (`F`, `NFR`, `BR`, `CR`) has a source citation or `ASSUMPTION A-nn`.
- Every requirement appears once in the traceability table.
- Every intake gap is either answered by a citation or listed in Open questions.
- Every intake source appears in 1 Introduction → References.
- No acceptance criterion uses an untestable word (fast, easy, good, user-friendly, robust).
- IDs are sequential and unique.

## Step 5: Write the files

1. Write `docs/requirements/srs.md`.
2. Convert it with `scripts/md_to_docx.py`: pick `<python>` once, the first of `python3`,
   `python`, `py -3` whose `--version` prints Python 3.8 or newer (`python3` can be a store stub on
   Windows, and `py` can fail inside an agent sandbox). Make a directory with
   `<python> -c "import tempfile; print(tempfile.mkdtemp())"`, write `scripts/md_to_docx.py` there
   unchanged, run `<python> <dir>/md_to_docx.py docs/requirements/srs.md docs/requirements/srs.docx`,
   and delete the directory. The script reads no other file of this skill. No working Python: skip
   the `.docx` and tell the user why.

## Step 6: Report

Tell the user, in their language: number of functional and non-functional requirements (or change
requests) by priority, entities and business rules (BR-nn), use cases, open questions, and each
assumption with the requirements that rest on it. Ask them to confirm or reject those assumptions.
End the file and your reply with this line, translated into the language of each:

"Next step: Lanewright Sprint Planner turns this into a weekly sprint plan."
