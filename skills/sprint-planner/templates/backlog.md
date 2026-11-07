# Backlog file formats

One file per sprint. `{nn}` is the two-digit sprint number in the file name and the title. Use the
format for what `.claude/kit.json` has. Keep the table header, section headings and line labels
exactly as shown: the workflow tool parses them. One row per item; acceptance criteria in one cell,
separated by `; ` (or `<br>`). Never put a `|` inside a cell.

The ID uses the team code (`BE-1-S01-01`). The two mapped columns:

| kit.json has | Format | Backlog path | `Region / module` | `Owner` |
|---|---|---|---|---|
| `docs`, `regions` | Lanewright | `docs.backlog` | the region key, or the module for a `per_module: true` region | that region's `role` |
| `dokumen`, `wilayah` | scrum-kit | `dokumen.backlog` | `Wilayah / modul`: the key, or the module for `per_modul: true` | `PIC`: that region's `agen` |
| no file | no kit.json: Lanewright format | `docs/sprints/sprint-{nn}-backlog.md` | the area: `api`, `web`, `ops` | the team code |

## Lanewright format (also: no kit.json: Lanewright format)

```
# Sprint {nn} backlog

Sprint goal: <one demonstrable outcome>

Period: <start> – <end>

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| BE-1-S01-01 | <item title> | <region key or module; no kit.json: api, web or ops> | <region's role, e.g. module-dev; no kit.json: BE-1> | 3 | <F-03 AC1: ...; AC2: ...> |

## Out of scope this sprint

- <item or requirement deliberately left for a later sprint, with the sprint>

## Dependencies and risks

- <dependency or risk> — <mitigation>
```

## scrum-kit format

The file is always in Indonesian; the item titles and criteria follow the document language.

```
# Backlog Sprint {nn}

Sprint Goal: <satu kalimat hasil yang bisa didemokan>

Periode: <mulai> – <selesai>

| ID | Item | Wilayah / modul | PIC | SP | Kriteria penerimaan |
|---|---|---|---|---|---|
| BE-1-S01-01 | <judul item> | <kunci wilayah, atau nama modul untuk wilayah per_modul> | <agen wilayah itu, mis. module-dev> | 3 | <F-03 AC1: ...; AC2: ...> |

## Di luar cakupan sprint ini

- <item atau kebutuhan yang sengaja ditunda, dengan sprintnya>

## Ketergantungan dan risiko

- <ketergantungan atau risiko> — <mitigasi>
```

## Rules for both

- ID: `<team code>-S{nn}-<seq>`, two-digit `<seq>` counted per team code within the sprint; letters,
  digits and hyphens only.
- A dependency on another owner's contract, schema or setup item in the same sprint is marked
  "day 1–2" in the Dependencies section.
- Period dates in the document language's usual form (`17 – 23 August 2026`, `17 – 23 Agustus 2026`).
- The SP column holds a number only (2–10).
- A file that already exists and has item rows is never overwritten: write
  `sprint-{nn}-backlog.proposed.md` beside it.
