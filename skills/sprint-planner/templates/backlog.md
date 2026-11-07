# Backlog file formats

One file per sprint. `{nn}` is the two-digit sprint number in the file name and the title. Use the
form for the tool detected from `.claude/kit.json`. Keep the table header, section headings and
line labels exactly as shown: the workflow tool parses them. One row per item; acceptance criteria
in one cell, separated by `; ` (or `<br>`). Never put a `|` inside a cell.

## Lanewright (kit.json has `docs` and `regions`; path `docs.backlog`)

Also used when there is no kit.json: region = a sensible area name (for example `api`, `web`,
`schema`, `ci`), owner = the team role code.

```
# Sprint {nn} backlog

Sprint goal: <one demonstrable outcome>

Period: <start> – <end>

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| BE-1-S01-01 | <item title> | <a key of regions, or a module name for a per_module region> | <that region's role, e.g. module-dev> | 3 | <F-03 AC1: ...; AC2: ...> |

## Out of scope this sprint

- <item or requirement deliberately left for a later sprint, with the sprint>

## Dependencies and risks

- <dependency or risk> — <mitigation>
```

## scrum-kit (kit.json has `dokumen` and `wilayah`; path `dokumen.backlog`)

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

- ID: `<AREA>-S{nn}-<seq>`, two-digit `<seq>` counted per area within the sprint; letters, digits
  and hyphens only.
- Period dates in the document language's usual form (`17 – 23 August 2026`, `17 – 23 Agustus 2026`).
- The SP column holds a number only (2–10).
- A file that already exists and has item rows is never overwritten: write
  `sprint-{nn}-backlog.proposed.md` beside it.
