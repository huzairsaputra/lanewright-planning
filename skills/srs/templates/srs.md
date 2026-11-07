<!--
SRS outline for a new application (IEEE 29148 style). Translate every heading, label and table
header into the document language. Keep the IDs (F-01, NFR-01, BR-01, UC-01, A-01) and the word
ASSUMPTION exactly as shown. Delete these comments. Source citations come from the intake file.
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

<!-- One block per requirement. Group under 3.x sub-headings by feature area when there are more
than about ten. -->

### F-01 <short name>

- **Requirement:** The system shall <one behaviour>.
- **Actor:** <actor>
- **Priority:** Must / Should / Could
- **Acceptance criteria:**
  - AC1: Given <state>, when <action>, then <observable result>.
  - AC2: ...
- **Source:** [S2 §3.2] / ASSUMPTION A-02

## 4 Non-functional requirements

| ID | Category | Requirement | Target | Source |
|---|---|---|---|---|
| NFR-01 | Security | <statement> | <measurable target or "to be confirmed"> | [citation] |
| NFR-02 | Privacy | ... | ... | ... |
| NFR-03 | Performance | ... | ... | ... |
| NFR-04 | Availability | ... | ... | ... |
| NFR-05 | Accessibility | ... | ... | ... |
| NFR-06 | Maintainability | ... | ... | ... |

## 5 Data

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

| # | Question | Affects | Owner | Origin |
|---|---|---|---|---|
| OQ-01 | <question> | F-03, NFR-02 | <role> | Gap G2 / ASSUMPTION A-01 |

## Traceability

| Requirement | Source |
|---|---|
| F-01 | [S2 §3.2] |
| NFR-01 | ASSUMPTION A-03 |

Next step: Lanewright Sprint Planner turns this into a weekly sprint plan.
