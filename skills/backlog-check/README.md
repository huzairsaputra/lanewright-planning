# Lanewright Backlog Check

Free agent skill. The human gate between planning and running a sprint: it checks each sprint
backlog file for readiness and records who approved it, before any agent touches the repository.

- Works on backlogs from Lanewright Sprint Planner or written by hand, in the format
  [Lanewright](https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams) or
  the free [scrum-kit](https://github.com/huzairsaputra/scrum-kit) reads, including `.proposed.md`
  files.
- A bundled Python script (standard library only) checks the table header, leftover template
  placeholders, item IDs and their sprint number, duplicate IDs across sprints, empty cells, story
  points, regions and owners against `.claude/kit.json`, short or vague acceptance criteria, and
  traceability to the SRS.
- The agent then reviews what a script cannot: testable criteria, item size, dependency order,
  owner fit and Must requirements left without an item.
- Writes `docs/sprints/backlog-check-{nn}.md` with a verdict (READY, READY WITH WARNINGS, NOT
  READY), the findings with suggested fixes, total story points and a sign-off block.
- Asks you to approve. Only your explicit yes fills the block, with the name and role you give;
  errors need an explicit, recorded override. It never edits a backlog on its own.

Try: "Run Lanewright Backlog Check on sprint 1".

Part of a free pipeline: **Intake → SRS → Sprint Planner → Backlog Check (human approval)**, then
run the approved sprints with Lanewright or scrum-kit. It does not replace them.

MIT licensed. Copyright (c) 2026 Huzair Saputra.
