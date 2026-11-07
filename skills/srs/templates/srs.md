<!--
SRS outline for a new application (IEEE 29148 style). Translate every heading, label and table
header, the Next step line and fixed phrases ("to be confirmed", "not described in the sources",
"no source") into the document language. Keep the IDs (F-01, NFR-01, BR-01, UC-01, A-01) and the
word ASSUMPTION exactly as shown. Delete these comments. Source citations come from the intake file.
-->

# Software Requirements Specification — <project name>

| Item | Value |
|---|---|
| Document | Software Requirements Specification (SRS) |
| Version | 0.1 (draft) |
| Date | <YYYY-MM-DD> |
| Basis | docs/requirements/intake.md (<n> sources) |
| Status | Draft for review |

## 1 Introduction

### 1.1 Purpose

<What this document specifies and for whom.> [S1 p.1]

### 1.2 Scope

<One paragraph: the product, its goal and benefit.> [citations]

| In scope | Out of scope |
|---|---|
| <capability> | <capability explicitly excluded, or not in any source> |

### 1.3 Definitions and abbreviations

| Term | Meaning |
|---|---|
| ... | ... |

### 1.4 References

| # | Source | Type | Date |
|---|---|---|---|
| S1 | <as in the intake Sources table> | PDF | ... |

## 2 Overall description

### 2.1 Product context

<Where the product sits: users, existing systems around it, channels.> [citations]

### 2.2 Actors and user classes

| Actor | Description | Main needs |
|---|---|---|
| <role> | <who they are> | <what they need from the system> |

### 2.3 Constraints

- <law or regulation by exact title, hosting, stack, hardware> [citation]

### 2.4 Assumptions

- A-01 ASSUMPTION: <statement> — confirm with <role>

## 3 Functional requirements

<!-- Group requirements by feature area under ### 3.x headings; each requirement is a #### block. -->

### 3.1 <feature area>

#### F-01 <short name>

- **Requirement:** The system shall <one behaviour>.
- **Actor:** <actor>
- **Priority:** Must / Should / Could (an intake `priority` fact or the source's; matches a stated
  must-have = Must even with assumed detail (name A-nn); else core flow of the first release = Must,
  supporting = Should, nice-to-have = Could; exists only because of an unconfirmed assumption = at
  most Should)
- **Acceptance criteria:**
  - AC1: Given <state>, when <action>, then <observable result>.
  - AC2: ...
- **Source:** [S2 §3.2] / ASSUMPTION A-02
- **Source ID:** <the source's own number, e.g. F-01 or UC-03; omit when the source has none>

## 4 Non-functional requirements

<!-- One row per category a source or the user mentions; other categories go to 8 Open questions.
Our IDs run NFR-01, NFR-02, ... in order. Source ID is the same field as for F-nn: the source's own
number (e.g. its NFR-05) goes there, so it is mapped, never silently renumbered. -->

| ID | Category | Requirement | Target | Source | Source ID |
|---|---|---|---|---|---|
| NFR-01 | <category a source names> | <statement> | <measurable target or "to be confirmed"> | [citation] | <the source's number, e.g. NFR-05; omit (—) when it has none> |

## 5 Entities and business rules

### 5.1 Entities

| Entity | Key fields | Notes |
|---|---|---|
| <entity> | <field names only> | <owner, retention, sensitivity> |

### 5.2 Business rules

| ID | Rule | Source |
|---|---|---|
| BR-01 | <condition and outcome> | [S2 p.7] |

## 6 Use cases

### UC-01 <name>

- **Actor:** <actor>
- **Precondition:** <state before>
- **Main flow:**
  1. <step>
  2. <step>
- **Result:** <state after>
- **Requirements:** F-01, F-02

## 7 External interfaces and integrations

| System | Direction | Data exchanged | Protocol / format | Source |
|---|---|---|---|---|
| <system> | In / Out / Both | <data> | <REST, file, SSO, ... or "to be confirmed"> | [citation] |

## 8 Open questions

| # | Question | Rests on | Affects | Owner |
|---|---|---|---|---|
| OQ-01 | Confirm ASSUMPTION A-01: <statement> | A-01 | F-03, F-07, NFR-02 | <role> |
| OQ-02 | <question> | Gap G2 | F-05 | <role> |
| OQ-03 | Is <category> needed (no source mentions it)? | Not in any source | — | <role> |

## Traceability

| Requirement | Source | Source ID |
|---|---|---|
| F-01 | [S2 §3.2] | F-01 |
| NFR-01 | [S1 p.4] | NFR-05 |
| NFR-02 | ASSUMPTION A-03 | — |

Next step: Lanewright Sprint Planner turns this into a weekly sprint plan.
