<!--
Layout of docs/requirements/intake.md. Translate every heading, label, table header, the Next
step line and the fixed phrases ("no answer — default taken", "not asked", "Round 2 skipped: no
answers in round 1", "to confirm", "date to confirm", "not described in the sources", "no source",
"Context, not sources") into the document language (the language of the sources). Keep the kind
tags, citation forms, S/Q/A numbering, the word ASSUMPTION and the "Kind:" line exactly as shown,
so the SRS skill can parse them. The Kind value is always new-application or change-request in
English; a label in the document language may follow it. Delete these comments.
-->

# Intake — <project name>

Kind: new-application (<optional label in the document language>)

| Item | Value |
|---|---|
| Project | <name as the sources give it, or the user's working title> |
| Project kind | <label in the document language> — <one-line reason> <citation> |
| Document language | <language> |
| Prepared | <YYYY-MM-DD> |
| Sources | <count, without S0> |
| Facts | <count> |
| Gaps | <count> |
| Assumptions | <count> |

## Sources

<!-- S0 only when a fact cites [request]; it is not counted in Sources. Citation forms: [S1 p.7],
[S1 §3.2], [S1 "Heading"] (heading without a number), [S1] (one-line brief or a source without
sections), [S3 "Caption" image 4], [S4 2026-03-02 14:05], [interview Q3], [request]. -->

| # | Source | Type | Date | Author | Notes |
|---|---|---|---|---|---|
| S0 | the user's request | request | <YYYY-MM-DD> | user | <what the user asked or decided> |
| S1 | <file name, folder path, Drive link title, "pasted text" or "one-line brief"> | PDF | 2026-03-02 | <role or unit> | <pages read, skipped parts, quality> |
| S2 | ... | DOCX | unknown | unknown | ... |

<!-- Only when the user gave just a brief inside an existing repository and did not confirm its
files as sources (no answer counts as no). No fact cites these, and they never change the Kind. -->

Context, not sources: `<file or folder>`, `<file or folder>`

## Facts

<!-- One line per fact: "- [kind] statement [citation]". Keep the groups in this order. A group
with a gap but no facts keeps its heading with the gap line under it (see Budget); drop a group
with neither. -->

### Goals

- [goal] <statement> [S1 p.2]

### Actors

- [actor] <who, and what they do with the system> [S1 §2.1]

### Features

- [feature] <capability> [S2 §3.2]

### Priorities

- [priority] <feature that must exist at launch> [interview Q1]

<!-- Q1 got no answer: no [priority] lines; write the gap line instead, pointing to the ASSUMPTION
that holds the proposed must-haves. -->

### Business rules

- [rule] <rule, condition, threshold> [S2 p.7]

### Data

- [data] <entity or field names, owner, retention> [S1 §4]

### Screens and design

- [screen] <screen name: visible fields, buttons, states> [S3 "Caption" image 4]

### Integrations

- [integration] <external system, direction, data exchanged> [S1 §5]

### Constraints

- [constraint] <law or regulation by exact title, hardware, stack, hosting> [S1 p.1]

### Non-functional

- [nfr] <security, privacy, performance, availability, accessibility target> [S2 §6]

### Timeline

- [timeline] <deadline or milestone with date> [S4 2026-03-02 14:05]

### Budget

- [budget] <amount, source of funds, fiscal year> [S1 p.9]

<!-- Gap line, when the group has no facts: -->

- Gap G4: <what is missing> — see Gaps

### Team

- [team] <role, number of people, availability or part-time share, planned leave> [interview Q4]

### Stakeholders

- [stakeholder] <role, interest, decision rights> [interview Q2]

## Conflicts

<!-- Only when two sources disagree. -->

| Topic | Source A says | Source B says | Resolution |
|---|---|---|---|
| ... | ... [S1 p.3] | ... [S2 §2] | Open / decided in interview Q4 |

## Gaps

| # | Missing | Why it matters | Status |
|---|---|---|---|
| G1 | <what the sources do not say> | <SRS or sprint plan needs it for ...> | Asked Q1 / ASSUMPTION A-01 / ASSUMPTION A-02 (not asked) / Open |

## Interview

<!-- At most 6 questions per round, gaps ranked by impact: actors and must-haves first, then
deadline and team, then the rest. Q1 is always the must-have question. -->

### Round 1 — <YYYY-MM-DD>

| # | Question | Proposed default | Answer |
|---|---|---|---|
| Q1 | Which 3–5 features must exist at launch? | <the core flows you infer> | <answer, "default accepted" or "no answer — default taken"> |
| Q2 | ... | ... | ... |

### Round 2 — <YYYY-MM-DD>

| # | Question | Proposed default | Answer |
|---|---|---|---|
| Q7 | ... | ... | ... |

<!-- Round 1 got no answers: write only this line instead of the Round 2 heading and table: -->

Round 2 skipped: no answers in round 1

## Assumptions

| # | ASSUMPTION | Basis | Confirm with |
|---|---|---|---|
| A-01 | ASSUMPTION: <statement> | Default proposed in Q3, no answer — default taken | <role> |
| A-02 | ASSUMPTION: <statement> | Not asked; proposed default for gap G5 | <role> |

## Sources not read

- <file> — <reason: format not supported, image not readable, access denied>

Next step: Lanewright SRS turns this into a requirements document.
