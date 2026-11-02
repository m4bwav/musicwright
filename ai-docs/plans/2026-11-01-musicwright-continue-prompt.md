# Continue musicwright

Execute this in D:/m4bwa/Claude/Projects/Ai/musicwright.

1. Load state: AGENTS.md, ai-docs/INDEX.md, ai-docs/HANDOFF.md (state lives there), the tail of ai-docs/log.md, and the musicwright skills you touch. Check open askwright sets under D:/m4bwa/Claude/Projects/Ai/Music/*/ask with `ask.py status`; act on answers, never fill open questions with a guess.
2. Waits on Mark: any release beyond a tag, registry publishing, listening verdicts on new takes.
3. Order: first the newest HANDOFF section's "Owed" items (e.g. verify FluidSynth via `mw.py doctor` and a render), then the main "Owed" list in order.
4. Stop points: before any GPU job on a shared ComfyUI if it is busy; before anything Mark must hear.
5. Hand-over: work through PRs on main, merge your own once CI is green; run tests/check_skills.py, tests/test_mw.py, scripts/budget.py before each commit. Before finishing, update HANDOFF.md and the log, and print the same start command: `Execute D:/m4bwa/Claude/Projects/Ai/musicwright/ai-docs/plans/2026-11-01-musicwright-continue-prompt.md`.
