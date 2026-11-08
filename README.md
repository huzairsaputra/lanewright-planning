<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/logo-dark.svg">
    <img alt="Lanewright Planning" src="brand/logo.svg" width="440">
  </picture>
</p>

<h1 align="center">Lanewright Planning</h1>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://github.com/huzairsaputra/lanewright-planning/releases"><img alt="Release" src="https://img.shields.io/github/v/release/huzairsaputra/lanewright-planning?color=green"></a>
  <a href="https://github.com/huzairsaputra/lanewright-planning/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/huzairsaputra/lanewright-planning/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="Windows, macOS, Linux" src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg">
</p>

Four free agent skills that take a project from loose material to an approved sprint backlog your
agents can run. Each works on its own; together they form a pipeline:

```
raw input → Intake → SRS → Sprint Planner → Backlog Check (human approval) → run the sprints

raw input        docs, folder, Drive, chat, one line
Intake           docs/requirements/intake.md
SRS              docs/requirements/srs.md + srs.docx
Sprint Planner   docs/sprints/weekly-sprint-plan.md + .docx, sprint-{nn}-backlog.md
Backlog Check    docs/sprints/backlog-check-{nn}.md: verdict, findings, your sign-off
run the sprints  Lanewright or scrum-kit
```

| Skill | Input | Output |
|---|---|---|
| [Lanewright Intake](skills/intake/) | PDF, DOCX, Markdown, text, images, chat exports, a local folder, a Google Drive folder, pasted text or one line | `docs/requirements/intake.md`: sources, cited facts by kind, gaps, interview, assumptions, project kind |
| [Lanewright SRS](skills/srs/) | `intake.md` | `srs.md` + `srs.docx`: IEEE 29148-style SRS or change-request SRS with traceability |
| [Lanewright Sprint Planner](skills/sprint-planner/) | `srs.md` | `weekly-sprint-plan.md` + `.docx` and one backlog file per sprint |
| [Lanewright Backlog Check](skills/backlog-check/) | sprint backlog files (Lanewright or scrum-kit format), optionally `kit.json` and `srs.md` | `backlog-check-{nn}.md`: SHA-256 of each checked file, READY / READY WITH WARNINGS / NOT READY per file, findings with fixes, total SP, a sign-off block only a human fills |

Principles shared by all four: no fact without a source citation, unknowns written as
`ASSUMPTION`, at most two short interview rounds with proposed defaults, documents in the language
of the sources, no existing content overwritten without asking, and no personal data copied into
the output.

## Why four skills, not one

The four jobs take different inputs and each ends in a file a person should read before the next
step starts, so they are separate skills that share one repository and one install command.

- **Start anywhere.** With an SRS already in hand, skip Intake and SRS. With a backlog written by
  hand or by another tool, run only Backlog Check. One large skill would force the whole chain on
  everyone.
- **A pause for review after every step.** Each output (`intake.md`, `srs.md`, the sprint plan,
  the check report) is a file you read and correct before the next skill reads it.
- **The check is independent of the author.** Backlog Check does not write plans, and only a human
  fills its sign-off block. A skill that wrote the plan and also approved it would be marking its
  own work.
- **Less to load, clearer triggers.** A skill's `SKILL.md` is loaded in full when it runs, and each
  description matches one kind of request ("write an SRS" is not "check this backlog").
- **Each skill carries only its own scripts.** Intake has `docx_text.py`; SRS and Sprint Planner
  have `md_to_docx.py`; Backlog Check has `backlog_check.py`.

The cost: a newcomer has to know the order. Each output ends with a one-line next step, and the
pipeline above shows the chain.

## Running the sprints

Backlog Check is the human gate in front of the workflow tools, not a replacement for them: it
reports and records your approval, and you then run the approved sprint. The backlog files match
what these tools read from `.claude/kit.json`:

- [Lanewright](https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams)
  (paid): role-based multi-agent Scrum with per-branch file ownership, gate evidence and
  approval-gated merges. "Run Lanewright sprint 1".
- [scrum-kit](https://github.com/huzairsaputra/scrum-kit) (free, Claude Code plugin):
  `/scrum-kit:sprint 1`.

## Install

Download the zip of a skill from the [Releases](https://github.com/huzairsaputra/lanewright-planning/releases)
page and unpack it into `~/.claude/skills`, or install from this repository (Python 3.8+):

```
py -I build.py --install            # builds the four dist/*.zip and installs each skill into ~/.claude/skills
py -I build.py --install <dir>      # another skills directory
py -I build.py --uninstall          # removes only what --install wrote
```

Use `python3` or `python` instead of `py` outside Windows.

## Example

[`examples/superapps/`](examples/superapps/) is a complete run from a single line, "Portal layanan
publik digital terpadu (Superapps)": the intake, the SRS (Markdown and Word), an eight-week sprint
plan (Markdown and Word) and eight sprint backlogs, in Indonesian because the brief is. Everything
the brief did not say is labelled as an assumption. The backlog check on those files reports
`READY WITH WARNINGS`: no errors, eight short acceptance criteria and ten items that cite more than
three requirements.

## Repository layout

| Path | What it holds |
|---|---|
| `examples/superapps/` | The example run above, with its `.claude/kit.json` |
| `skills/<skill>/` | `SKILL.md`, `templates/`, `README.md`, `LICENSE` of one skill |
| `shared/scripts/` | `docx_text.py` (DOCX → text, used by Intake), `md_to_docx.py` (Markdown → DOCX, used by SRS and Sprint Planner) and `backlog_check.py` (backlog readiness rules, used by Backlog Check); standard library only, each has `--self-test` |
| `brand/` | The Lanewright Planning logo: mark, horizontal logo (light and dark), and the 512 px icon (`icon-tile-green.svg`, `icon-512.png`) |
| `build.py` | Checks each skill and builds `dist/<name>-<version>.zip`, copying in the scripts it uses |
| `tests/` | Unit tests for the scripts and the build |

## Development

```
py -I -m unittest discover -s tests -v
py -I shared/scripts/docx_text.py --self-test
py -I shared/scripts/md_to_docx.py --self-test
py -I shared/scripts/backlog_check.py --self-test
py -I build.py
```

## Platforms

Windows, macOS and Linux. The skills are plain instructions plus three Python standard-library
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
