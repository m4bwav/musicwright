---
kind: note
status: active
date: 2026-10-18
title: Prompt for the next musicwright session (owed work from HANDOFF)
tags: handoff,prompt
---

# Next session prompt

Paste this into a fresh session in the musicwright repository.

---

Continue musicwright (this repository, public m4bwav/musicwright). Read AGENTS.md, then ai-docs/INDEX.md and ai-docs/HANDOFF.md, and check each skill's `evergreen.json` for due dates. Work the Owed items in HANDOFF.md, newest section first; refresh any evergreen unit that is due. Stop at anything that needs the owner or a listener, and say so.

For each change: research before recall, log the reason in the skill's CHANGELOG.md, run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py`, and work through a pull request you merge yourself once CI is green. Before you finish, update HANDOFF.md and the log, and print the same start command for this file.
