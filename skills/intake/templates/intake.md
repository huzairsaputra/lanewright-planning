<!--
Layout of docs/requirements/intake.md. Translate every heading, label, table header and the Next
step line into the document language (the language of the sources). Keep the kind tags, citation forms, S/Q/A numbering and
the word ASSUMPTION exactly as shown, so the SRS skill can parse them. Delete these comments.
-->

# Intake — <project name>

| Item | Value |
|---|---|
| Project | <name as the sources give it, or the user's working title> |
| Project kind | New application / Change to an existing system — <one-line reason> <citation> |
| Document language | <language> |
| Prepared | <YYYY-MM-DD> |
| Sources | <count> |
| Facts | <count> |
| Gaps | <count> |
| Assumptions | <count> |

## Sources

| # | Source | Type | Date | Author | Notes |
|---|---|---|---|---|---|
| S1 | <file name, folder path, Drive link title, "pasted text" or "one-line brief"> | PDF | 2026-03-02 | <role or unit> | <pages read, skipped parts, quality> |
| S2 | ... | DOCX | unknown | unknown | ... |

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

### Round 1 — <YYYY-MM-DD>

| # | Question | Proposed default | Answer |
|---|---|---|---|
| Q1 | ... | ... | <answer, "default accepted" or "no answer — default taken"> |

### Round 2 — <YYYY-MM-DD>

| # | Question | Proposed default | Answer |
|---|---|---|---|
| Q5 | ... | ... | ... |

## Assumptions

| # | ASSUMPTION | Basis | Confirm with |
|---|---|---|---|
| A-01 | ASSUMPTION: <statement> | Default proposed in Q3, no answer — default taken | <role> |
| A-02 | ASSUMPTION: <statement> | Not asked; proposed default for gap G5 | <role> |

## Sources not read

- <file> — <reason: format not supported, image not readable, access denied>

Next step: Lanewright SRS turns this into a requirements document.
