<!--
Layout of docs/sprints/backlog-check-{nn}.md, one per sprint. Document language = the backlog's
language (its item titles and criteria). For Indonesian use exactly the terms in the table below;
any other language translates every heading, label, verdict and fixed line. Item IDs and rule names
(header, placeholder, id, empty-cell, sp, sp-scale, region, owner, criteria-short, criteria-vague,
deps, trace, coverage, total-sp, format, columns, or a short name for a judgment finding) stay as
they are. Roles, not names, except the approver the user names. Delete these comments.

| English | Indonesian |
|---|---|
| Sprint {nn} Backlog Check | Pemeriksaan Backlog Sprint {nn} |
| Item / Value | Ruas / Isi |
| Backlog file / Format / Checked / Method | Berkas backlog / Format / Diperiksa / Metode |
| Verdict | Putusan |
| READY | SIAP |
| READY WITH WARNINGS | SIAP DENGAN CATATAN |
| NOT READY | BELUM SIAP |
| Findings | Temuan |
| # / Item / Rule / Severity / Finding / Suggested fix | # / Item / Aturan / Tingkat / Temuan / Usulan perbaikan |
| No findings. | Tidak ada temuan. |
| Story points | Story point |
| Sprint / Items / Total SP | Sprint / Item / Total SP |
| SRS coverage | Cakupan SRS |
| Sign-off | Persetujuan |
| Approved by / Role / Date / Overrides | Disetujui oleh / Peran / Tanggal / Pengecualian |
| Next step: after approval, run the sprint with ... or the free scrum-kit ... | Langkah berikutnya: setelah disetujui, jalankan sprint dengan ... atau scrum-kit gratis ... |
-->

# Sprint {nn} Backlog Check

| Item | Value |
|---|---|
| Backlog file | `<path of the backlog file>` |
| Format | Lanewright / scrum-kit |
| Checked | <YYYY-MM-DD> |
| Method | scripts/backlog_check.py and judgment review / rules applied by hand (no working Python) |

## Verdict

**READY / READY WITH WARNINGS / NOT READY** — <errors> errors, <warnings> warnings.

<!-- One line: the main reason for the verdict. -->

## Findings

<!-- Script findings first (INFO lines other than coverage and total-sp may be left out), then
judgment findings. No findings: write "No findings." instead of the table. -->

| # | Item | Rule | Severity | Finding | Suggested fix |
|---|---|---|---|---|---|
| 1 | BE-1-S01-02 | sp | ERROR | SP 13 is outside 1-10 | Split into schema (5) and API (8) items |
| 2 | FE-1-S01-01 | criteria-vague | WARN | "works properly" has no observable result | "the list shows 20 rows per page and a next-page button" |
| 3 | - | dependency order | WARN | FE-1-S01-01 needs BE-1-S01-02, which ends later in the sprint | Mark the API contract day 1–2 or move the screen to sprint 2 |

## Story points

| Sprint | Items | Total SP |
|---|---|---|
| {nn} | <n> | <SP> |

SRS coverage: <"all n F/CR requirements are cited" or the IDs no item cites; Must requirements
without an item named first>. <!-- Only when an SRS was used. -->

## Sign-off

<!-- Leave the four fields empty until the user explicitly approves. Overrides: finding numbers and
the user's reason, e.g. "#1 accepted: the item is split on day 1". -->

Approved by: ____   Role: ____   Date: ____   Overrides: ____

Next step: after approval, run the sprint with Lanewright (https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or the free scrum-kit (https://github.com/huzairsaputra/scrum-kit): `Run Lanewright sprint {n}` / `/scrum-kit:sprint {n}`.
