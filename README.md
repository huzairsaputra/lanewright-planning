# Lanewright Planning

Three free agent skills that take a project from loose material to a sprint plan your agents can
run. Each works on its own; together they form a pipeline:

```
raw input ─▶ Lanewright Intake ─▶ Lanewright SRS ─▶ Lanewright Sprint Planner ─▶ run the sprints
(docs, folder,   docs/requirements/    docs/requirements/     docs/sprints/weekly-sprint-plan.md   Lanewright or
 Drive, chat,    intake.md             srs.md + srs.docx      + .docx, sprint-{nn}-backlog.md       scrum-kit
 one line)
```

| Skill | Input | Output |
|---|---|---|
| [Lanewright Intake](skills/intake/) | PDF, DOCX, Markdown, text, images, chat exports, a local folder, a Google Drive folder, pasted text or one line | `docs/requirements/intake.md`: sources, cited facts by kind, gaps, interview, assumptions, project kind |
| [Lanewright SRS](skills/srs/) | `intake.md` | `srs.md` + `srs.docx`: IEEE 29148-style SRS or change-request SRS with traceability |
| [Lanewright Sprint Planner](skills/sprint-planner/) | `srs.md` | `weekly-sprint-plan.md` + `.docx` and one backlog file per sprint |

Principles shared by all three: no fact without a source citation, unknowns written as
`ASSUMPTION`, at most two short interview rounds with proposed defaults, documents in the user's
language, nothing overwritten without asking, and no personal data copied into the output.

## Running the sprints

The backlog files match what these workflow tools read from `.claude/kit.json`:

- [Lanewright](https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams)
  (paid): role-based multi-agent Scrum with per-branch file ownership, gate evidence and
  approval-gated merges. "Run Lanewright sprint 1".
- [scrum-kit](https://github.com/huzairsaputra/scrum-kit) (free, Claude Code plugin):
  `/scrum-kit:sprint 1`.

## Install

From Agensi (free): search for Lanewright Intake, Lanewright SRS and Lanewright Sprint Planner.

From this repository (Python 3.8+):

```
py -I build.py --install            # builds dist/*.zip and installs each skill into ~/.claude/skills
py -I build.py --install <dir>      # another skills directory
py -I build.py --uninstall          # removes only what --install wrote
```

Use `python3` or `python` instead of `py` outside Windows.

## Repository layout

| Path | What it holds |
|---|---|
| `skills/<skill>/` | `SKILL.md`, `templates/`, `README.md`, `LICENSE` of one skill |
| `shared/scripts/` | `docx_text.py` (DOCX → text, used by Intake) and `md_to_docx.py` (Markdown → DOCX, used by SRS and Sprint Planner); standard library only, each has `--self-test` |
| `build.py` | Checks each skill and builds `dist/<name>-<version>.zip`, copying in the scripts it uses |
| `tests/` | Unit tests for the scripts and the build |

## Development

```
py -I -m unittest discover -s tests -v
py -I shared/scripts/docx_text.py --self-test
py -I shared/scripts/md_to_docx.py --self-test
py -I build.py
```

## Platforms

Windows, macOS and Linux. The skills are plain instructions plus two Python standard-library
scripts; CI runs the tests and builds on all three operating systems. The skills were tried end to
end in Claude Code; other agents that can read files and run Python should work but are not tested
yet.

## Roadmap

- **Audio and video input** (recorded meetings, voice notes) through STT-Platform, a speech-to-text
  service in development. It will use your own STT-Platform account; subscribers send recordings
  without limits, and free accounts see their remaining quota before anything is sent. Until then,
  Intake asks for a transcript.

## License

MIT. Copyright (c) 2026 Huzair Saputra.
