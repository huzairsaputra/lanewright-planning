# Lanewright Sprint Planner

Free agent skill. Turns an SRS into a weekly Scrum plan your team and your stakeholders can both
use: `docs/sprints/weekly-sprint-plan.md` plus a Word copy, and one backlog file per sprint.

- Asks a few questions (start Monday, end date, team roles, capacity, holidays, milestones), each
  with a proposed default.
- Splits requirements into items of 2–10 story points, foundations first (repository, CI, schema,
  auth), then features in dependency order. Every item has an owner role and testable acceptance
  criteria from the SRS.
- Monday–Sunday sprints with day numbers across the project. No sprint is ever booked above its
  capacity; what does not fit moves later and is reported.
- The plan has the document info, Scrum events, team and capacity, Definition of Ready and Done,
  a sprint map, one page per sprint (goal, backlog, risks, demo), project risks, metrics and event
  templates.
- Backlog files are written in the exact format
  [Lanewright](https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or
  the free [scrum-kit](https://github.com/huzairsaputra/scrum-kit) reads (detected from
  `.claude/kit.json`), so you can run sprint 1 right away. Backlog files that already have items
  are never overwritten; a file holding only the template placeholder is.

Try: "Run Lanewright Sprint Planner".

Part of four free skills: **raw input → Intake → SRS → Sprint Planner → Backlog Check (human
approval) → run the sprints** with [Lanewright](https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or the free
[scrum-kit](https://github.com/huzairsaputra/scrum-kit).

Install (free, from Agensi): Lanewright Intake, Lanewright SRS, Lanewright Sprint Planner and
Lanewright Backlog Check.

MIT licensed. Copyright (c) 2026 Huzair Saputra.
