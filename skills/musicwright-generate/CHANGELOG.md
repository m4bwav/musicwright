# Changelog: musicwright-generate

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261106-5 · 2026-11-06 · SFT pack: wider blind test; recommended for calm and combat, still not the default
- because: R-20261106-7
- files: SKILL.md (model table), ../musicwright/references/recipes.json (acestep-xl-sft-pack)

The owner's rule was to change the default only if the pack won across captions with acceptable endings. It won calm and combat, not town, and takes on both routes stopped early.

### C-20261106-4 · 2026-11-06 · Cover: what a score cannot say about keeping the tune
- because: everscout ai-music distillation of Müller, Fundamentals of Music Processing (sec. 7.3, 8.2)
- files: references/acestep.md (cover notes)
- Ear stays the test: chroma scores read harmony and carry no per-pair threshold, and pitch tracking is weak on dense mixes.

### C-20261106-3 · 2026-11-06 · Lyrics: opposing view on matched lengths
- because: R-20261106-6
- files: references/acestep.md (Lyrics field), references/minimax3.md (Lyrics)
- Records Pattison's disagreement with the upstream note and drops "read aloud".

### C-20261106-2 · 2026-11-06 · SFT pack recipe; YuE2 cover verdict
- because: listener answers ask-sft-pair and ask-yue2cover, R-20261106-2
- files: SKILL.md (job table), RESEARCH.md, ../musicwright/references/recipes.json, ../musicwright/scripts/mw.py

Adds `acestep-xl-sft-pack` as an option, not the default, and names the YuE2 cover as the route for keeping a tune.

### C-20261106-1 · 2026-11-06 · YuE2 melody cover in mw.py gen
- because: user request, R-20261105-2
- files: references/acestep.md

The YuE2 cover route now runs through `mw.py gen`; no listener verdict yet.

### C-20261105-9 · 2026-11-05 · Official prompting notes for YuE2, Stable Audio 3 and ACE-Step vocals
- because: R-20261105-4
- files: references/models.md, references/acestep.md

Official prompting notes for YuE2, Stable Audio 3 and ACE-Step vocals, from round-two reading; see the RESEARCH entry for how strong each source is.

### C-20261105-3 · 2026-11-05 · YuE2 memory figure corrected
- because: R-20261105-3
- files: references/models.md (Full songs)

The row still gave the stated 24 GB after a measurement here.

### C-20261105-2 · 2026-11-05 · YuE2 melody route, Stable Audio 3 caption shape
- because: R-20261105-2
- files: references/acestep.md (Audio as input), references/models.md (Stable Audio 3 captions)

Points at a route that keeps a melody and gives the template's caption order; neither has been run or heard here.

### C-20261105-1 · 2026-11-05 · ACE-Step community reports
- because: R-20261105-1
- files: references/acestep.md (Caption, Lyrics, Parameters, Audio as input), references/acestep-rest.md (Start and check), references/licences.md (Model terms)

Adds what users and the maintainer report on captions, chords, endings, keyscale and cover, marked as reports and untried here, plus an unanswered rights question.

### C-20261104-1 · 2026-11-04 · Second-round listening: extract leak, recipe notes
- because: user request (listening page ask-round2, four answers; decisions 2026-11-04-listening-round2)
- files: SKILL.md route table; references acestep.md, acestep-rest.md; hub references/recipes.json

Extract drums are no longer described as clean: one spot near the end leaked. The recipe source notes record the Stable Audio 3 miss, the YuE2 keep and the preferred MiniMax seed. One listener, one source each.

### C-20261103-9 · 2026-11-03 · Sound tests point at the askwright page
- because: user request; T-20261103-1 (0/3: the hub-only rule was missed when this skill handled the request)
- files: SKILL.md
- One line sends listening tests to an askwright page when `mw.py doctor` reports the script.

### C-20261103-1 · 2026-11-03 · Listener verdicts: ComfyUI first for source tasks, two new recipes
- because: user request (listening page hw-checks-listening, seven answers)
- files: SKILL.md route table; references acestep-rest.md, acestep.md, minimax3.md, models.md

Cover without `--strength` now uses semantic hints, which won a blind pair. ComfyUI repaint and extract lead their routes. Stable Audio 3 Medium and YuE2 become recipes through `mw.py gen`. Each ruling rests on one listener and one source, and the docs say so.

### C-20261102-1 · 2026-11-02 · pulse --threshold adaptive for building leads
- because: user request (book distill: Lerch, Audio Content Analysis)
- files: SKILL.md Step 5

Step 5 tells a quiet-then-building lead to use `pulse --threshold adaptive`; the global threshold misses its quiet hits (Lerch, *An Introduction to Audio Content Analysis* 2nd ed., sec. 9.3.2).

### C-20261023-3 · 2026-10-23 · Density section tags marked as not shown to help; TUNING-GAP over 30 cents
- because: L-002, decisions 2026-10-23-listening-checks
- files: SKILL.md (Step 2, sections carry density), references/acestep-rest.md (Working from existing audio)
- In one blind pair the density tags did no better than mood words and neither take reached the tutti asked for; the bullet now says so. The lego tuning check fires over 30 cents.

### C-20261101-2 · 2026-11-01 · Copy check for every released cue
- because: user request (book learnings, Hands-On Generative AI with Transformers and Diffusion Models ch. 9; everscout ai-video beat)
- files: SKILL.md (Step 3 cheat-sheet)
- A cheat-sheet row: listen for a known tune before releasing any cue, not only after a reference or cover, since scarce-data music models can reproduce training tracks. Unverified.

### C-20261101-1 · 2026-11-01 · Temperature ladder, melody-copy check, control map
- because: user request (book learnings from Foster, Generative Deep Learning 2e, ch. 11)
- files: SKILL.md (Step 3 cheat-sheet), references/acestep.md (Control map)
- Two cheat-sheet rows (hold the seed and step LM temperature 0.7, 0.85, 1.0 before a new seed; compare transcribed contours and n-grams when a reference or cover was used) and a three-level control map that says to change only the wrong level.

### C-20261023-2 · 2026-10-23 · Tuning gap of an added part
- because: decisions 2026-10-23-books-track11 (N5)
- files: references/acestep-rest.md (Adding a part)
- After a lego render, `mw.py analyze SRC PART` gives the part's tuning gap from the source.

### C-20261023-1 · 2026-10-23 · Sections that say who plays, the listener's tired-of list, a stop rule
- because: R-20261023-1 (musicwright-compose), T-20261023-1
- files: SKILL.md (Step 2; Step 3), references/acestep.md (Lyrics field), references/minimax3.md (lyrics), evals/evals.json (action-2)
- Section tags carry density and the caption names near and far parts; the locked-seed loop compares matched copies and stops after three or four one-knob changes. Density tags are from the books and not yet compared with mood-only tags by a listener.

### C-20261018-1 · 2026-10-18 · Adding a part: DCW off, the server version, the lego recipe, pulse and answer
- because: R-20261017-6, L-001, user request (the listener's verdicts on the stage-2 mixes)
- files: SKILL.md (Step 5: add a part to a kept take), references/acestep-rest.md (Start and check; Working from existing audio), RESEARCH.md (R-20261017-6, Current understanding, Open questions), LEARNINGS.md (L-001); hub references/recipes.json (acestep-rest-lego)
- A new step routes a part added to a kept take through pulse, lego on the base checkpoint, duck --stem and mix; the REST reference names the server version that fixes DCW, how to start it per model and the measured VRAM.

### C-20261017-2 · 2026-10-17 · Source tasks (lego, complete, extract, cover, repaint) documented as run by mw.py
- because: R-20261017-4, R-20261017-5, user request
- files: references/acestep-rest.md (Working from existing audio), references/models.md (ACE-Step row), RESEARCH.md (Current understanding, Open questions)
- The REST reference now names the part list, the base checkpoints and their sizes, the upload and the planner-off rule; the tasks table replaced the "not yet run here" one.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
