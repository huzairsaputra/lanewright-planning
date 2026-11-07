# Lanewright Intake

Free agent skill. Give it whatever you have about a project (PDFs, Word files, screenshots, chat
exports, a folder, a Google Drive folder, pasted notes, or just one sentence) and it writes
`docs/requirements/intake.md`: one evidence file where every fact has a source citation.

- Facts grouped by kind: goals, actors, features, business rules, data, screens, integrations,
  constraints, non-functional needs, timeline, budget, stakeholders.
- Every fact cites its source (`[S2 p.7]`, `[S1 §3.2]`, `[interview Q3]`); nothing is invented.
- Lists what is missing, then asks at most two short rounds of questions, each with a proposed
  default. Anything still unknown is written down as an `ASSUMPTION`, never as a fact.
- Tells a new application from a change to an existing system.
- Writes in your language. Reads Word files with a small bundled Python script (standard library
  only); PDFs and images are read by the agent itself.

Try: "Run Lanewright Intake on the docs/input folder" or "Lanewright Intake: a citizen complaint
portal for our city".

Part of a free pipeline: **Intake → SRS → Sprint Planner**, then run the sprints with
[Lanewright](https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or
the free [scrum-kit](https://github.com/huzairsaputra/scrum-kit).

MIT licensed. Copyright (c) 2026 Huzair Saputra.
