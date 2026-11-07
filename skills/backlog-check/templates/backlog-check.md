<!--
Layout of docs/sprints/backlog-check-{nn}.md, one per sprint. Document language = the backlog's
language (its item titles and criteria). For Indonesian use exactly the terms in the table below;
any other language translates every heading, label, verdict and fixed line. Item IDs, file names,
hashes and rule names (header, placeholder, placeholder-official, id, empty-cell, sp, sp-scale,
region, owner, criteria-short, criteria-vague, broad-citation, deps, trace, coverage, total-sp,
format, columns, sha256, or a short name for a judgment finding) stay as they are. Roles, not
names, except the approver the user names. Delete these comments.

| English | Indonesian |
|---|---|
| Sprint {nn} Backlog Check | Pemeriksaan Backlog Sprint {nn} |
| Item / Value | Ruas / Isi |
| Format / Checked / Method / Status | Format / Diperiksa / Metode / Status |
| pending human approval / approved | menunggu persetujuan manusia / disetujui |
| Checked files | Berkas yang diperiksa |
| File / SHA-256 | Berkas / SHA-256 |
| not computed (no working Python) | tidak dihitung (Python tidak tersedia) |
| Verdict | Putusan |
| File / Verdict / Errors / Warnings | Berkas / Putusan / Galat / Peringatan |
| READY | SIAP |
| READY WITH WARNINGS | SIAP DENGAN CATATAN |
| NOT READY | BELUM SIAP |
| Findings | Temuan |
| # / Item / Rule / Severity / Finding / Suggested fix | # / Item / Aturan / Tingkat / Temuan / Usulan perbaikan |
| No findings. | Tidak ada temuan. |
| Story points | Story point |
| Sprint / Items / Total SP | Sprint / Item / Total SP |
| SRS coverage | Cakupan SRS |
| Weakly covered | Tercakup lemah |
| Sign-off | Persetujuan |
| Approved by / Role / Date / Overrides | Disetujui oleh / Peran / Tanggal / Pengecualian |
| DoD not applicable (approved) / none | Butir DoD tidak berlaku (disetujui) / tidak ada |
| DoD items proposed as not applicable (not approved until listed in the sign-off) / None | Butir DoD yang diusulkan tidak berlaku (belum disetujui sebelum dicantumkan di persetujuan) / Tidak ada |
| Next step: after approval, run the sprint with ... or the free scrum-kit ... | Langkah berikutnya: setelah disetujui, jalankan sprint dengan ... atau scrum-kit gratis ... |
-->

# Sprint {nn} Backlog Check

| Item | Value |
|---|---|
| Format | Lanewright / scrum-kit |
| Checked | <YYYY-MM-DD> |
| Method | scripts/backlog_check.py and judgment review / rules applied by hand (no working Python) |
| Status | pending human approval / approved |

## Checked files

<!-- One row per "INFO | <file> | - | sha256 | <hex>" line of the script, copied unchanged. No
working Python: "not computed (no working Python)". -->

| File | SHA-256 |
|---|---|
| `docs/sprints/sprint-{nn}-backlog.md` | <64 hex characters> |
| `docs/sprints/sprint-{nn}-backlog.proposed.md` | <only when the twin was checked> |

## Verdict

<!-- One row per checked file, from the script's VERDICT lines plus your judgment findings for that
file. A .proposed.md twin is judged on its own; approval covers the official file only. -->

| File | Verdict | Errors | Warnings |
|---|---|---|---|
| `docs/sprints/sprint-{nn}-backlog.md` | READY / READY WITH WARNINGS / NOT READY | <n> | <n> |

<!-- One line: the main reason for each verdict. -->

## Findings

<!-- One table for all checked files. Script findings first (INFO lines other than coverage and
total-sp may be left out; sha256 lines go to Checked files), then judgment findings. With more
than one file, name the file in the Finding cell. No findings: write "No findings." instead of the
table. -->

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

Weakly covered: <IDs cited only by items with more than 3 requirement IDs>. <!-- Only when the
script prints the weakly covered coverage line. -->

## Sign-off

<!-- The planner's proposals from section "Definition of Done: items that may not apply" of
docs/sprints/weekly-sprint-plan.md, item and reason; "None" when it lists none or there is no plan. -->

DoD items proposed as not applicable (not approved until listed in the sign-off):

- Negative authorization test — the notes have no login (SRS A-03)

<!-- Leave the five fields empty and the Status "pending human approval" until the user
explicitly approves, also when nobody can answer. Overrides: finding numbers and the user's reason,
e.g. "#1 accepted: the item is split on day 1". DoD not applicable (approved): only the DoD items
the user names, separated by "; ", or "none"; filled only together with the other fields, never
by you alone. An older report without this field counts as none approved. -->

Approved by: ____   Role: ____   Date: ____   Overrides: ____
DoD not applicable (approved): ____

Next step: after approval, run the sprint with Lanewright (https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or the free scrum-kit (https://github.com/huzairsaputra/scrum-kit): `Run Lanewright sprint {nn}` / `/scrum-kit:sprint {nn}`.
