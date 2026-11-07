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
  `[interview Q3]`) or `ASSUMPTION A-nn`. A requirement resting on an assumption keeps that label
  and appears in Open questions; never upgrade it to a plain requirement silently.
- **Testable acceptance criteria.** Observable, with numbers or concrete examples ("given ...
  when ... then ..."). Never "works well", "user-friendly", "fast".
- **The document language** is the language of the intake file (or of the user's request when
  there is no intake). Translate the template headings; keep IDs (`F-01`, `NFR-01`, `BR-01`,
  `UC-01`, `CR-01`) and the word ASSUMPTION as they are.
- **Personal and government data stay out.** Field names and data kinds only, never values. No
  names of private individuals unless the user asks.
- **Ask before overwriting** `srs.md` or `srs.docx`: update, replace, or write
  `srs.proposed.md` / `srs.proposed.docx` beside them.
- Do not commit, push or upload anything unless the user asks.

## Step 1: Load the evidence

Read `docs/requirements/intake.md` in full: project kind, language, facts, gaps, interview,
assumptions.

No intake file: offer two options and wait for the choice.

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

Work through the facts kind by kind:

| Intake facts | SRS section |
|---|---|
| goal, stakeholder | 1 Introduction (purpose, scope) |
| actor | 2 Actors / user classes table |
| constraint | 2 Constraints |
| assumptions A-nn | 2 Assumptions (copied with their numbers) |
| feature, screen | 3 Functional requirements, 6 Use cases |
| nfr | 4 Non-functional requirements |
| data, rule | 5 Data and business rules |
| integration | 7 External interfaces |
| gaps still open, conflicts | 8 Open questions |

Functional requirements:

- One behaviour per requirement: "The system shall ..." (in the document language).
- Priority: **Must** when a source says it is required, core, mandated by law or needed for the
  first release; **Should** when a source asks for it without making it essential; **Could** when it
  is a nice-to-have or comes from an assumption only. A requirement that rests on an assumption is
  never Must unless the user confirms it.
- Two to five acceptance criteria each, numbered `AC1`, `AC2`.
- Screens from the intake become requirements for the behaviour they show, cited to the image.

Non-functional requirements: cover security, privacy, performance, availability, accessibility and
maintainability. Use the measurable target a source gives. When no source gives one, write the
requirement with "Target: to be confirmed" and add it to Open questions; do not make a number up.

Change-request SRS: one `CR-nn` per requested change, each with current behaviour, requested change,
impact (screens, data, API), acceptance criteria, priority and source.

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
   Windows, and `py` can fail inside an agent sandbox). Write `scripts/md_to_docx.py` from this
   skill, unchanged, to a temporary file outside the repository; run
   `<python> <temp>/md_to_docx.py docs/requirements/srs.md docs/requirements/srs.docx`; delete the
   temporary file. The script reads no other file of this skill. No working Python: skip the
   `.docx` and tell the user why.

## Step 6: Report

Tell the user, in their language: number of functional, non-functional and data requirements (or
change requests) by priority, use cases, open questions, and which requirements rest on
assumptions. Ask them to confirm or reject those assumptions. End your reply and the file with:

"Next step: Lanewright Sprint Planner turns this into a weekly sprint plan."
