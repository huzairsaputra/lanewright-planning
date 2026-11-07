<!--
SRS outline for a change to an existing system. Translate every heading, label and table header
into the document language. Keep the IDs (CR-01, NFR-01, BR-01, A-01) and the word ASSUMPTION
exactly as shown. Delete these comments. Source citations come from the intake file.
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

### CR-01 <short name>

- **Current behaviour:** <what happens today> [S3 image 2]
- **Requested change:** The system shall <new behaviour>.
- **Impact:**
  - Screens: <screens changed or added>
  - Data: <fields, tables, migrations, existing records to convert>
  - API: <endpoints changed, added, deprecated; consumers affected>
- **Priority:** Must / Should / Could
- **Acceptance criteria:**
  - AC1: Given <state>, when <action>, then <observable result>.
  - AC2: Existing <behaviour that must not change> still works.
- **Source:** [S1 p.2] / ASSUMPTION A-02

## 4 Non-functional impact

| ID | Category | Requirement | Target | Source |
|---|---|---|---|---|
| NFR-01 | <security, privacy, performance, availability, accessibility, maintainability> | <statement> | <target or "to be confirmed"> | [citation] |

## 5 Data and business rules

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

| # | Question | Affects | Owner | Origin |
|---|---|---|---|---|
| OQ-01 | ... | CR-02 | <role> | Gap G1 |

## Traceability

| Requirement | Source |
|---|---|
| CR-01 | [S1 p.2] |

Next step: Lanewright Sprint Planner turns this into a weekly sprint plan.
