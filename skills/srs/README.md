# Lanewright SRS

Free agent skill. Turns the evidence file from Lanewright Intake into a Software Requirements
Specification: `docs/requirements/srs.md` plus a Word copy, `srs.docx`.

- IEEE 29148-style outline: introduction and scope, actors, constraints, assumptions, functional
  requirements (`F-01`..), non-functional requirements (`NFR-01`..), data and business rules,
  use cases, integrations, open questions and a traceability table.
- Every requirement has a priority (Must/Should/Could), testable acceptance criteria and a source
  citation or a labelled `ASSUMPTION`. Assumptions are never promoted to requirements silently.
- For a change to an existing system it writes a change-request SRS: per change, the current
  behaviour, the requested change, the impact on screens, data and API, and acceptance criteria.
- No intake yet? It offers to run one, or does a short one inline.
- Writes in the language of your documents. The Word copy comes from a small bundled Python script
  (standard library only).

Try: "Run Lanewright SRS".

Part of four free skills: **raw input → Intake → SRS → Sprint Planner → Backlog Check (human
approval) → run the sprints** with [Lanewright](https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or the free
[scrum-kit](https://github.com/huzairsaputra/scrum-kit).

MIT licensed. Copyright (c) 2026 Huzair Saputra.
