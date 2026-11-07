<!--
Layout of docs/sprints/weekly-sprint-plan.md. Keep the sections in this order. Translate headings,
labels, table headers and the Next step line into the document language; for Indonesian use
exactly the terms in the table below. Delete these comments, but keep the pagebreak comment lines: md_to_docx.py turns
each into a page break before a sprint.

| English | Indonesian |
|---|---|
| Weekly Sprint Plan | Rencana Sprint Mingguan |
| Item / Value | Ruas / Isi |
| 1 Introduction | 1 Pendahuluan |
| 2 Scrum framework | 2 Kerangka Kerja Scrum |
| Event / Schedule / Duration / Participants / Output | Acara / Jadwal / Durasi / Peserta / Keluaran |
| 3 Team and capacity | 3 Komposisi Tim dan Kapasitas |
| Role / People / Repository / Capacity per sprint / Notes | Peran / Personel / Repositori / Kapasitas per Sprint / Catatan |
| 4 Definition of Ready and Definition of Done | 4 Definition of Ready dan Definition of Done |
| Work type / Done criteria | Jenis Pekerjaan / Kriteria Selesai |
| 5 Sprint map | 5 Peta Sprint |
| Sprint / Period / Days / Sprint Goal | Sprint / Periode / Hari / Sprint Goal |
| 6 Sprint details | 6 Rencana Detail per Sprint |
| Day | Hari |
| No / Backlog item / Owner / SP / Done criteria | No / Item Sprint Backlog / PIC / SP / Kriteria Selesai |
| Total commitment: N SP — P people, capacity C SP. | Total komitmen: N story point — P personel, kapasitas C SP. |
| Sprint Backlog | Sprint Backlog |
| Risks and dependencies | Risiko dan Ketergantungan |
| Increment to demo | Increment yang Didemokan |
| 7 Project risks | 7 Manajemen Risiko Proyek |
| Risk / Level / Mitigation | Risiko / Tingkat / Mitigasi |
| 8 Metrics and reporting | 8 Metrik dan Pelaporan |
| Metric / Definition / Target | Metrik / Definisi / Target |
| Appendix A. Scrum event templates | Lampiran A. Templat Acara Scrum |
| Field / Content | Ruas / Isi |
| Planner assumptions / to confirm / date to confirm | Asumsi perencanaan / perlu dikonfirmasi / tanggal perlu dikonfirmasi |
| Open decisions for the product owner | Keputusan terbuka untuk product owner |
| Sprint report recipient | Penerima laporan sprint |
| Next step: Lanewright Backlog Check verifies each sprint backlog and records your approval; then run the sprints with ... or the free scrum-kit ... | Langkah berikutnya: Lanewright Backlog Check memeriksa setiap backlog sprint dan mencatat persetujuan Anda; lalu jalankan sprint dengan ... atau scrum-kit gratis ... |
-->

# Weekly Sprint Plan — <project name>

| Item | Value |
|---|---|
| Title | Weekly Sprint Plan — <project name> |
| Version | 1.0 |
| Method | Scrum, one-week sprints (Monday–Sunday) |
| Data source | docs/requirements/srs.md (<date or version>) |
| Product scope | <one line from SRS 1.2> |
| Status | Draft for product owner approval |

## 1 Introduction

### 1.1 Purpose

<What this plan is for: turning the SRS into weekly sprints the team commits to.>

### 1.2 Scope

<Requirements covered (F-01–F-nn, NFR-.., CR-..), what is left out and why.>

### 1.3 Basis

<The SRS and its version; assumptions taken from the SRS.>

Planner assumptions (defaults taken without an answer):

- PA-01 <statement> — to confirm with <role>

<!-- Only when the repository's rules ask for another language than the sources: -->

- PA-02 Documents follow the language of the sources (<language>), not <language> as the repository
  rules ask — to confirm with <role>

<!-- Only when the project's rules say implementers write no tests and QA tests in the next sprint. -->

Open decisions for the product owner:

- <The project's rules let QA test only in the sprint after the implementation; the Definition of
  Done needs passing tests within the sprint, and the last sprint would end untested.> Options:
  (a) add a week; (b) accept the items without tests for now; (c) QA tests in the same sprint after
  the paired implementation item merges. Planned until decided: (c), each QA item after the item it
  tests, with `Tests: <item ID>` in its text.

### 1.4 Date assumptions

- Project start: <Monday date> (day 1). End: <date> (day N).
- Sprints run Monday to Sunday; working days are Monday to Friday.
- Holidays and leave: <list; national holidays nobody confirmed are marked "to confirm" (PA-nn), and a
  date you are unsure of reads "date to confirm">.

## 2 Scrum framework

### 2.1 Roles

- **Product owner:** <role; default: the client contact>; owns the backlog and accepts increments.
- **Scrum master / orchestrator:** <role; default: the team lead>; runs events, removes blockers,
  guards capacity.
- **Developers:** <team codes, e.g. BE-1, FE-1, OPS>.
- **Sprint report recipient:** <role; default: the product owner>; receives the report after each
  Sprint Review.

### 2.2 Artefacts

- **Product backlog:** the SRS requirements split into items (this plan).
- **Sprint backlog:** `<backlog path>`, one file per sprint.
- **Increment:** a deployed, demonstrable result at the end of each sprint.

### 2.3 Events

| Event | Schedule | Duration | Participants | Output |
|---|---|---|---|---|
| Sprint Planning | Day 1 of each sprint (Monday), 09:00 | 1 hour | Whole team, product owner | Sprint goal and sprint backlog |
| Daily Scrum | Every working day, <time; default 09:00 local> | 15 minutes | Developers | Plan for the day, blockers |
| Backlog Refinement | Day 4 of each sprint (Thursday), 14:00 | 1 hour | Product owner, developers | Next sprint's items ready |
| Sprint Review | Last working day of the sprint, <time; default 14:00> | 1 hour | Whole team, stakeholders | Accepted increment, feedback, sprint report to <recipient> |
| Sprint Retrospective | Last working day of the sprint, <time; default 15:00, after the review> | 45 minutes | Whole team | Up to three improvement actions |

### 2.4 Team working rules

- One item in progress per person; finish before starting the next.
- Every change goes through a merge request with green CI and a review.
- Blockers are raised at the Daily Scrum or immediately when they stop work.
- The sprint goal does not change during the sprint; new work goes to the backlog.

## 3 Team and capacity

| Role | People / Repository | Capacity per sprint | Notes |
|---|---|---|---|
| BE-1 | 1 / <repository or area> | 10 SP | ... |
| FE-1 | 1 / ... | 10 SP | ... |
| OPS | 1 / ... | 10 SP | ... |
| **Total** | <P> | <C> SP | 10 SP per person per full week; 6 SP for a week of 4 working days or fewer; part-time pro rata (half time → 5 SP); about 10% of each sprint's team capacity kept free |

<!-- Only when capacity changes between sprints. -->

| Period | People | Total capacity | Consequence |
|---|---|---|---|
| Sprint 3 (<dates>) | 2 | 16 SP | <holiday on ...; items moved to sprint 4> |

## 4 Definition of Ready and Definition of Done

### 4.1 Definition of Ready

- The item traces to an SRS requirement or is a named foundation item.
- Acceptance criteria are testable and agreed with the product owner.
- Estimated at 10 SP or less; dependencies are done or planned earlier.
- The owner role is assigned and has capacity in the sprint.

### 4.2 Definition of Done

| Work type | Done criteria |
|---|---|
| Backend / API | Acceptance criteria met; tests pass; lint clean; API documented; reviewed and merged |
| Frontend / mobile | Acceptance criteria met on target devices; matches the agreed screens; reviewed and merged |
| Database | Migration and rollback tested; seed data where needed; reviewed and merged |
| DevOps / CI | Pipeline green; deployment documented; secrets kept out of the repository |
| QA | Test cases written and run; defects logged; regression run on the increment |
| Documentation | Updated in the repository and reviewed |

## 5 Sprint map

| Sprint | Period | Days | Sprint Goal |
|---|---|---|---|
| 1 | 17 – 23 August 2026 | 1–7 | <one demonstrable outcome> |
| 2 | 24 – 30 August 2026 | 8–14 | ... |

| Milestone | Sprint |
|---|---|
| <first demo, UAT, go-live, handover> | <n> |

## 6 Sprint details

<!-- pagebreak -->

### 6.1 Sprint 1 — 17 – 23 August 2026 (Day 1–7)

Sprint Goal: <one demonstrable outcome>.

#### Sprint Backlog

| No | Backlog item | Owner | SP | Done criteria |
|---|---|---|---|---|
| OPS-S01-01 | <item> | OPS | 3 | <criteria; source requirement> |
| BE-1-S01-01 | ... | BE-1 | 5 | ... |

<!-- The Owner column holds the team code. -->

Total commitment: <N> SP — <P> people, capacity <C> SP.

#### Risks and dependencies

- <risk or dependency> — <mitigation>
- BE-1-S01-02 needs OPS-S01-01 (day 1–2) — <mitigation>

#### Increment to demo

<What the product owner will see working at the review.>

<!-- Repeat the pagebreak line and a 6.n subsection for every sprint. -->

## 7 Project risks

| Risk | Level | Mitigation |
|---|---|---|
| <open SRS question blocks a feature> | High / Medium / Low | <decision date, owner> |
| <integration partner not ready> | ... | ... |
| <capacity loss from leave or holidays> | ... | ... |

## 8 Metrics and reporting

| Metric | Definition | Target |
|---|---|---|
| Sprint goal achieved | Sprints whose goal was accepted at review | Every sprint |
| Commitment reliability | Done SP ÷ committed SP per sprint | ≥ 80% |
| Velocity | Done SP per sprint | Stable within ±20% |
| Escaped defects | Defects found after an item was accepted | Falling sprint to sprint |
| Cycle time | Days from item start to merge | ≤ 3 working days |

Reporting: <who receives the sprint report, when, in what form>.

## Appendix A. Scrum event templates

### A.1 Daily Scrum

- Date:
- Done since the last Daily Scrum:
- Plan until the next Daily Scrum:
- Blockers and who removes them:

### A.2 Sprint Review

- Sprint and goal:
- Items done and accepted:
- Items not done (and where they go):
- Stakeholder feedback and new backlog items:

### A.3 Sprint Retrospective

- What went well:
- What to improve:
- Actions (owner, due sprint), at most three:

### A.4 Backlog card

| Field | Content |
|---|---|
| ID | <team code>-S{nn}-<seq> |
| Title | ... |
| Owner | <team code> |
| SP | 2–10 |
| Acceptance criteria | ... |
| Dependencies | <IDs> |
| Links | <SRS requirement IDs, designs, merge request> |

Next step: Lanewright Backlog Check verifies each sprint backlog and records your approval; then run the sprints with Lanewright (https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or the free scrum-kit (https://github.com/huzairsaputra/scrum-kit).
