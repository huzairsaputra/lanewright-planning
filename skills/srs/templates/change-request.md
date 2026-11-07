<!--
SRS outline for a change to an existing system. Translate every heading, label and table header
the Next step line and fixed phrases ("to be confirmed", "not described in the sources", "no
source") into the document language. Keep the IDs (CR-01, NFR-01, BR-01, A-01) and the word
ASSUMPTION exactly as shown. Delete these comments. Source citations come from the intake file.
-->

# Change Request Specification — <system name>

| Item | Value |
|---|---|
| Document | Software Requirements Specification — change request |
| System | <existing system and version, as the sources name it> |
| Version | 0.1 (draft) |
| Date | <YYYY-MM-DD> |
| Basis | docs/requirements/intake.md (<n> sources) |
| Status | Draft for review |

## 1 Introduction

### 1.1 Purpose

<Which changes this document specifies, who requested them and why.> [S1 p.1]

### 1.2 Scope

| In scope | Out of scope |
|---|---|
| <change> | <related change not requested> |

### 1.3 Definitions and abbreviations

| Term | Meaning |
|---|---|
| ... | ... |

### 1.4 References

| # | Source | Type | Date |
|---|---|---|---|
| S1 | <request letter, change note, bug list, screenshots> | PDF | ... |

## 2 Current system

### 2.1 Context

<What the system does today, who uses it, what it connects to.> [citations]

### 2.2 Actors affected

| Actor | Description | Main needs |
|---|---|---|
| <role> | ... | <what the change gives them> |

### 2.3 Constraints

- <deployment window, backwards compatibility, data migration, law> [citation]

### 2.4 Assumptions

- A-01 ASSUMPTION: <statement> — confirm with <role>

## 3 Requested changes

<!-- Group changes by area under ### 3.x headings; each change is a #### block. CR numbers are this
document's own and never reuse the existing system's IDs. -->

### 3.1 <area>

#### CR-01 <short name>

- **Current behaviour:** <what happens today> [S3 image 2] — or "not described in the sources"
  plus an open question in section 8; never guessed
- **Requested change:** The system shall <new behaviour>.
- **Impact:**
  - Screens: <screens changed or added>
  - Data: <fields, tables, migrations, existing records to convert>
  - API: <endpoints changed, added, deprecated; consumers affected>
- **Priority:** Must / Should / Could (an intake `priority` fact or the source's; matches a stated
  must-have = Must even with assumed detail (name A-nn); else core flow = Must, supporting = Should,
  nice-to-have = Could; exists only because of an unconfirmed assumption = at most Should)
- **Acceptance criteria (two to five):**
  - AC1: Given <state>, when <action>, then <observable result>.
  - AC2: Existing <behaviour that must not change> still gives <the same observable result>.
- **Source:** [S1 p.2] / ASSUMPTION A-02
- **Source ID:** <the request's own item number, e.g. item 3; omit when it has none>

## 4 Non-functional impact

<!-- One row per category a source or the user mentions; other categories go to 8 Open questions.
Our IDs run NFR-01, NFR-02, ... in order. Source ID is the same field as for CR-nn: the source's
own number (e.g. its NFR-05) goes there, so it is mapped, never silently renumbered. -->

| ID | Category | Requirement | Target | Source | Source ID |
|---|---|---|---|---|---|
| NFR-01 | <category a source names> | <statement> | <target or "to be confirmed"> | [citation] | <the source's number, e.g. NFR-05; omit (—) when it has none> |

## 5 Entities and business rules

### 5.1 Entities changed

| Entity | Key fields | Notes |
|---|---|---|
| <entity> | <added or changed fields> | <migration of existing data> |

### 5.2 Business rules

| ID | Rule | Source |
|---|---|---|
| BR-01 | <new or changed rule> | [citation] |

## 6 Use cases changed

### UC-01 <name>

- **Actor:** <actor>
- **Precondition:** <state before>
- **Main flow:**
  1. <step>
- **Result:** <state after>
- **Changes:** CR-01

## 7 External interfaces and integrations

| System | Direction | Change | Source |
|---|---|---|---|
| <system> | In / Out / Both | <what changes for it> | [citation] |

## 8 Open questions

| # | Question | Rests on | Affects | Owner |
|---|---|---|---|---|
| OQ-01 | Confirm ASSUMPTION A-01: <statement> | A-01 | CR-02, CR-04 | <role> |
| OQ-02 | <question> | Gap G2 | CR-03 | <role> |
| OQ-03 | What does the system do today for <CR-05 area>? (not described in the sources) | No source | CR-05 | <role> |
| OQ-04 | Is <category> needed (no source mentions it)? | Not in any source | — | <role> |

## Traceability

| Requirement | Source | Source ID |
|---|---|---|
| CR-01 | [S1 p.2] | item 1 |

Next step: Lanewright Sprint Planner turns this into a weekly sprint plan.
