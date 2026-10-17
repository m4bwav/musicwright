# 02 - Agent tools and workflows for music (October 2026)

Research for the musicwright plugin: which skills, plugins, MCP servers and agent workflows people
use to make music with Claude Code, Claude Desktop, Cursor, Codex, Copilot, Gemini CLI and
ChatGPT, what works, and what to borrow.

- Researched: 2026-10-17. Stars and last-push dates come from the GitHub API on that day.
- Method: `gh search repos`, `gh search code --filename SKILL.md`, `gh api` for metadata, READMEs
  and issue lists; the skills.sh search API; the Hacker News Algolia API for threads and
  comments; web search for vendor news. Reddit was not read.
- Findings are numbered R-101 onward. Each gives its source and the date it was checked or
  published. "Verdict" in the table: **use** (recommend or depend on), **borrow** (read for
  ideas, don't depend on it), **watch** (early or changing), **skip**.

## Summary table

| Name | Type | URL | Stars | Last push | Licence | Verdict |
|---|---|---|---|---|---|---|
| Claude for Creative Work: Ableton connector | Official connector (docs only) | anthropic.com/news/claude-for-creative-work | n/a | 2026-04-28 launch | proprietary | watch |
| Claude for Creative Work: Splice connector | Official remote MCP (samples) | mcp.splice.com/mcp | n/a | 2026-04-28 launch | proprietary | use (optional) |
| Ableton Extensions SDK (beta) | Official JS/TS SDK | ableton.com (via attackmagazine.com) | n/a | 2026-06-02 beta | proprietary | watch |
| ahujasid/ableton-mcp | MCP (Ableton, Remote Script socket) | github.com/ahujasid/ableton-mcp | 3200 | 2026-09-22 | MIT | borrow |
| adamjmurray/producer-pal | MCP + REST + skills (Ableton, Max for Live) | github.com/adamjmurray/producer-pal | 331 | 2026-10-17 | GPL-3.0 | use (Ableton users) |
| uisato/ableton-mcp-extended | MCP (Ableton) | github.com/uisato/ableton-mcp-extended | 278 | 2026-05-07 | MIT | borrow |
| bschoepke/ableton-live-mcp | MCP (Ableton, Live Object Model) | github.com/bschoepke/ableton-live-mcp | 230 | 2026-10-06 | MIT | borrow |
| glincker/ableton-skills | 12 skills for Ableton producers | github.com/glincker/ableton-skills | 41 | 2026-09-23 | MIT | borrow |
| Korben00/ableton-producer-skills | Skills on Extensions SDK | github.com/Korben00/ableton-producer-skills | 20 | 2026-06-05 | MIT | borrow (gotchas) |
| TwelveTake-Studios/reaper-mcp | MCP (REAPER, 176-180 tools) | github.com/TwelveTake-Studios/reaper-mcp | 82 | 2026-10-17 | MIT | use (REAPER users) |
| bonfire-systems/reaper-mcp | MCP (REAPER, reapy, 60 tools) | github.com/bonfire-systems/reaper-mcp | 158 | 2026-10-07 | MIT | borrow |
| dschuler36/reaper-mcp-server | MCP (REAPER project reading) | github.com/dschuler36/reaper-mcp-server | 131 | 2026-10-16 | MIT | borrow |
| xDarkzx/Reaper-MCP | MCP (REAPER, 181 tools) | github.com/xDarkzx/Reaper-MCP | 100 | 2026-10-14 | Apache-2.0 | watch |
| shiehn/total-reaper-mcp | MCP (all of ReaScript) | github.com/shiehn/total-reaper-mcp | 87 | 2026-08-03 | MIT | borrow |
| MongLong0214/logic-pro-mcp | MCP (Logic Pro, Swift, fail-closed) | github.com/MongLong0214/logic-pro-mcp | 130 | 2026-10-17 | MIT | borrow |
| koltyj/logic-pro-mcp | MCP (Logic Pro) | github.com/koltyj/logic-pro-mcp | 122 | 2026-09-05 | MIT | watch |
| karl-andres/fl-studio-mcp | MCP (FL Studio) | github.com/karl-andres/fl-studio-mcp | 220 | 2026-09-30 | MIT | watch |
| WeModulate/bitwig-mcp-server | MCP (Bitwig) | github.com/WeModulate/bitwig-mcp-server | 75 | 2025-04-10 | MIT | skip (stale) |
| yokadeeds-dev/yoka-cubase-mcp | MCP (Cubase via Mackie Control) | github.com/yokadeeds-dev/yoka-cubase-mcp | 6 | 2026-10-16 | AGPL-3.0 | borrow (closed loop) |
| tskovlund/mcp-score | MCP + skill (MusicXML, MuseScore) | github.com/tskovlund/mcp-score | 29 | 2026-10-12 | MIT | use |
| HKUDS/CLI-Anything (musescore, audacity) | Agent CLIs + skills | github.com/HKUDS/CLI-Anything | 53869 | 2026-09-22 | Apache-2.0 | borrow |
| williamzujkowski/live-coding-music-mcp | MCP (Strudel via Playwright) | github.com/williamzujkowski/live-coding-music-mcp | 244 | 2026-10-12 | AGPL-3.0 | borrow (ideas only) |
| p-poss/dj-claude | Claude Code plugin + MCP (Strudel) | github.com/p-poss/dj-claude | 36 | 2026-06-02 | AGPL-3.0 | borrow (ideas only) |
| linxule/mcp-music-studio | Remote MCP + MCP Apps (ABC + Strudel) | github.com/linxule/mcp-music-studio | 74 | 2026-10-13 | AGPL-3.0 | borrow (ideas only) |
| bfollington/terma `strudel` skill | Skill | github.com/bfollington/terma | 52 | 2026-08-30 | CC-BY-SA-4.0 | borrow |
| renatoworks/strudel-claude | Skills (Strudel) | github.com/renatoworks/strudel-claude | 71 | 2026-02-03 | MIT | borrow |
| vanities/toaster-strudel | Skill set (Strudel, 10+ skills) | github.com/vanities/toaster-strudel | 8 | 2026-06-15 | GPL-3.0 | skip |
| oaustegard/claude-skills `listening-to-music` | Skill + scripts (render and measure) | github.com/oaustegard/claude-skills | 153 | 2026-10-15 | MIT | use / borrow heavily |
| abhishekjairath/sonic-pi-mcp | MCP (Sonic Pi via OSC) | github.com/abhishekjairath/sonic-pi-mcp | 19 | 2026-03-22 | MIT | watch |
| Synohara/supercollider-mcp | MCP (SuperCollider) | github.com/Synohara/supercollider-mcp | 10 | 2026-10-13 | MIT | watch |
| AJBogo9/supercollider-mcp | MCP (SC with NRT render) | github.com/AJBogo9/supercollider-mcp | 0 | 2026-10-05 | MIT | borrow (NRT idea) |
| os-tack/fcp-midi | MCP (semantic MIDI ops, pretty-midi) | github.com/os-tack/fcp-midi | 7 | 2026-07-06 | MIT | borrow (syntax) |
| tubone24/midi-mcp-server | MCP (text to MIDI file) | github.com/tubone24/midi-mcp-server | 55 | 2026-04-12 | MIT | skip |
| brightlikethelight/music21-mcp-server | MCP (music21 analysis) | github.com/brightlikethelight/music21-mcp-server | 28 | 2026-06-23 | MIT | skip |
| bitwize-music-studio/claude-ai-music-skills | Claude Code plugin (53 skills + MCP, Suno pipeline) | github.com/bitwize-music-studio/claude-ai-music-skills | 568 | 2026-10-15 | CC0-1.0 | borrow heavily |
| elevenlabs/skills `music` | Official skill | github.com/elevenlabs/skills | 493 | 2026-10-17 | MIT | use (paid route) |
| elevenlabs/elevenlabs-mcp | Official MCP (speech, SFX, music) | github.com/elevenlabs/elevenlabs-mcp | 1535 | 2026-08-20 | MIT | use (paid route) |
| MiniMax-AI/MiniMax-MCP | Official MCP (TTS, music) | github.com/MiniMax-AI/MiniMax-MCP | 1590 | 2026-08-20 | MIT | watch |
| ace-step/ace-step-skills | Official ACE-Step skills | github.com/ace-step/ace-step-skills | 94 | 2026-03-10 | none stated | borrow |
| ace-step/ACE-Step-1.5 | Open music model | github.com/ace-step/ACE-Step-1.5 | 13714 | 2026-10-11 | MIT | use (local default) |
| calesthio/generative-media-skills | Provider skills (ACE-Step, ElevenLabs, Lyria, MiniMax, Suno) + EVAL.md | github.com/calesthio/generative-media-skills | 205 | 2026-07-14 | MIT | borrow |
| AceDataCloud/SunoMCP | Third-party Suno API MCP | github.com/AceDataCloud/SunoMCP | 67 | 2026-10-12 | MIT | skip (unofficial) |
| sandraschi/suno-mcp | Suno via Playwright browser | github.com/sandraschi/suno-mcp | 1 | 2026-10-14 | MIT | skip (ToS risk) |
| ruvnet/ruflo `ruflo-music` | Plugin skills (master, stems, MIDI) | github.com/ruvnet/ruflo | 75898 | 2026-10-17 | MIT | borrow (LUFS report) |
| BilkentAudio/Wwise-MCP | MCP (Wwise via WAAPI) | github.com/BilkentAudio/Wwise-MCP | 76 | 2026-10-04 | Apache-2.0 | watch |
| varunneal/spotify-mcp | MCP (Spotify) | github.com/varunneal/spotify-mcp | 614 | 2026-03-11 | MIT | skip (out of scope) |
| marcelmarais/spotify-mcp-server | MCP (Spotify) | github.com/marcelmarais/spotify-mcp-server | 482 | 2026-10-16 | MIT | skip (out of scope) |
| zachswift615/audio-analysis-mcp and peers | MCP (audio analysis) | github.com/zachswift615/audio-analysis-mcp | 4 | 2025-12-11 | none | skip; build our own |

## Findings by category

### Official and vendor routes

- **R-101** Anthropic shipped nine "Claude for Creative Work" connectors on 2026-04-28,
  including Ableton and Splice. Anthropic describes the Ableton connector as grounding answers
  in official Live and Push documentation; Splice lets Claude search its royalty-free sample
  catalogue. The Ableton connector controls nothing in Live. Source:
  https://www.anthropic.com/news/claude-for-creative-work (launch date from
  https://godberrystudios.com/posts/claude-for-creative-work-9-connectors-tested-2026/), checked
  2026-10-17.
- **R-102** Splice's MCP is remote at `https://mcp.splice.com/mcp` (Streamable HTTP, OAuth).
  Tools named in coverage: describe_a_sound, create_stack, prompt_to_stack, share_stack,
  download_asset. Downloads depend on the user's Splice plan and credits, and the server is
  labelled beta. Source: https://sonicfield.org/ai-agents-enter-the-studio-the-mcp-turn-in-audio
  (2026-04-29), https://mcpservers.org/remote-mcp-servers/splice, checked 2026-10-17.
- **R-103** Ableton released the Extensions SDK as a public beta on 2026-06-02 (Live Suite
  12.4.5 beta): JS/TS on Node, reaching tracks, clips, MIDI, devices, tempo and automation.
  Limits in the first beta: no Max for Live integration, no event triggers. Korben00's skills
  record more friction (Developer Mode resets on restart, one reliable activation per Live
  session, no preset loading, not real time). Sources:
  https://www.attackmagazine.com/news/ableton-extensions-sdk-turns-live-suite-into-an-experimental-development-platform/,
  https://github.com/Korben00/ableton-producer-skills, checked 2026-10-17.
- **R-104** ElevenLabs publishes an official `music` skill in elevenlabs/skills (MIT, pushed
  2026-10-17). It uses model `music_v2_5` and documents compose, stream, composition plans,
  `compose_detailed` with inpainting, `video_to_music`, upload and finetunes. It needs
  `ELEVENLABS_API_KEY` and is paid per use. The official elevenlabs-mcp server (1535 stars) covers
  the same API. Source: https://github.com/elevenlabs/skills/blob/main/music/SKILL.md, checked
  2026-10-17.
- **R-105** anthropics/skills (181k stars) has no music, audio or MIDI skill. The nearest is
  `algorithmic-art` (p5.js visuals). anthropics/claude-plugins-official and github/awesome-copilot
  have no music entries either (tree grep for music|audio|midi|strudel, 2026-10-17). Music
  skills all come from the community and vendors.
- **R-106** ACE-Step ships official skills (ace-step/ace-step-skills: `acestep-docs`,
  `acestep-lyrics-transcription`, `acestep-simplemv`, a Remotion music-video skill). The model
  repo ace-step/ACE-Step-1.5 is MIT with 13.7k stars, pushed 2026-10-11. The author's earlier private
  ACE-Step skills (a REST client and a ComfyUI recipe) are prior art folded into musicwright. Source: https://github.com/ace-step/ace-step-skills, checked
  2026-10-17.

### Agent Skills and Claude Code plugins

- **R-107** bitwize-music-studio/claude-ai-music-skills (568 stars, CC0, pushed 2026-10-15) is
  the most complete music plugin found: 53 skills, a Python MCP server with 80+ tools, a
  Suno-centred album pipeline (concept, research with source checks, lyrics with prosody and
  pronunciation checks, Suno style prompts, stem import, mastering to -14 LUFS, promo video).
  It has quality gates (a 13-point lyric checklist and a 7-point audio QC: loudness, clipping,
  silence, phase, stereo width, frequency balance, dynamic range) and assigns a model tier per
  skill (opus for creative, sonnet for reasoning, haiku for mechanical work). Its CI runs 4,412
  tests on three OSes. The README warns that Pro plans hit rate limits. CC0 means its code can be
  reused. Source: https://github.com/bitwize-music-studio/claude-ai-music-skills, checked
  2026-10-17.
- **R-108** oaustegard's `listening-to-music` skill (v0.2.0, MIT) solves the core problem that
  Claude cannot hear. It renders Strudel or any Web Audio page in headless Chromium to WAV, then
  plots a CQT spectrogram with a pYIN melody line and chroma. It measures chord clashes from the
  note events, "rubs" in the audio, and Sethares roughness. It engraves the notes as a score PNG
  for Claude to read and uses a shared events JSON (layer, t0, t1, midi; times in bars). Its rule:
  change one thing, re-render, re-measure, keep a numbers table, record each version twice, and
  only trust a change bigger than the take-to-take spread. Measured results it publishes:
  monophonic transcription F1 87% on a soprano line and 0% on four-part texture; the OMR tool
  oemer scored 6%; Claude reading a clean engraving into ABC scored 100% (one case). Source:
  https://github.com/oaustegard/claude-skills/tree/main/listening-to-music, checked 2026-10-17.
- **R-109** Strudel skills are the most numerous type of music skill. On skills.sh the leader
  is bfollington/terma `strudel` with 135 installs. It writes patterns and shares them as encoded
  strudel.cc URLs, with no audio rendering. Others: renatoworks/strudel-claude (REPL control,
  DJ sets, lessons), vanities/toaster-strudel (10+ narrow skills: bass, groove, mixing,
  emotion), p-poss/dj-claude, ahgraber/skills, janjs/music-as-code. Source:
  https://skills.sh/api/search?q=strudel, checked 2026-10-17.
- **R-110** Suno skills have the highest real install counts: schwepps `suno-music-creator`
  1343, social-media-skills `suno` 478, bitwize `suno-engineer` 426, acedatacloud `suno-music`
  267. They write prompts and lyrics and leave generation to the user on suno.com. The "music"
  search also returns items with 140k-390k installs (heygen hyperframes, prime-skills
  runcomfy). Counts that size look inflated or automated. Don't treat them as demand signals.
  Source: https://skills.sh/api/search?q=suno and ?q=music, checked 2026-10-17.
- **R-111** MIDI skills have few installs: maystudios `audio-to-midi` 91 and `midi-synth` 68,
  tubone24 `midi-generation` 40, ruflo `music-midi` 23. HKUDS CLI-Anything's
  `cli-anything-musescore` has 477 installs. CLI-Anything ships agent CLIs with eval tasks
  (export_wav, project_roundtrip) for Audacity, MuseScore and rekordbox. Source:
  https://skills.sh/api/search?q=midi, https://github.com/HKUDS/CLI-Anything, checked 2026-10-17.
- **R-112** glincker/ableton-skills (12 skills, MIT) puts producer craft into skills and leaves
  the plumbing to an Ableton MCP. Examples: high-pass pads near 100 Hz, respect instrument ranges
  (Vln1 G3-G6), catch kick-bass masking near 80 Hz, trap at 140 BPM is half time. One repo
  targets Claude Code, Cursor, Codex and Gemini CLI. Korben00/ableton-producer-skills does the
  same on the Extensions SDK and has a `gotchas.md` that every other skill depends on. Sources:
  https://github.com/glincker/ableton-skills, https://github.com/Korben00/ableton-producer-skills,
  checked 2026-10-17.
- **R-113** calesthio/generative-media-skills (205 stars, MIT) has one provider skill per
  music API (ace-step, elevenlabs-music, google-lyria, minimax-music, suno-music), each with an
  `EVAL.md`, plus `music-supervision-scoring` and `music-video-production` craft skills. It is a
  good model for keeping provider details apart from craft. Source:
  https://github.com/calesthio/generative-media-skills, checked 2026-10-17.
- **R-114** ruflo's `ruflo-music` plugin has a `music-master` skill that reports
  `lufs_before` and `lufs_after` "so the user can see the actual loudness change, not just
  'done'", with a -14 LUFS default and a peak limiter. It is a small but good habit to copy.
  Source: https://github.com/ruvnet/ruflo/tree/main/plugins/ruflo-music, checked 2026-10-17.
- **R-115** Several DAW MCPs bundle their own skills: Producer Pal (`examples/skills/`:
  analyze-audio, export-audio, read-als, open-live-set, audio-generator), uisato
  (`ableton-songwriter`), jasper-zheng/ableton-sdk-mcp (`ableton-midi`, `ableton-mixing`,
  `ableton-safety`), and mcp-score (`score-generate`, installed with `mcp-score install-skill`).
  The pairing is becoming standard: an MCP server for access, a skill for judgement. Source: GitHub
  code search `--filename SKILL.md ableton`, 2026-10-17.

### DAW control MCP servers

- **R-116** Ableton has the most work. ahujasid/ableton-mcp (3200 stars, MIT) is the reference.
  A MIDI Remote Script inside Live opens a socket, and a Python MCP server installed via `uvx
  ableton-mcp` talks to it. It warns to run only one instance, because Claude Desktop and Cursor
  together fight over the socket. It ships anonymous telemetry, which can be disabled. Its most
  discussed issues are about installation: the control surface not appearing, Live 12 Remote
  Scripts folder changes, macOS crashes. One issue notes that the PyPI release (1.3.x) is ahead
  of `main`. Source: https://github.com/ahujasid/ableton-mcp and its issues, checked 2026-10-17.
- **R-117** Producer Pal (adamjmurray, GPL-3.0, v2.4.0 released 2026-10-02, 2.5.0-rc1 on
  2026-10-14) is a Max for Live device running an MCP server in Node for Max. It also exposes a
  REST API so scripts and coding agents can edit a Live Set with no AI at all, and it works with
  Claude, Gemini, ChatGPT, OpenRouter, Ollama and LM Studio. Its stated vision is "help people
  make music, not make music instead of them". It got an honourable mention in Anthropic's
  "Built with Claude" contest. Its August 2026 issues are a catalogue of silent failures:
  "reports success but leaves the pad unchanged", `quantizeGrid` silently no-ops, a batched update
  times out partway with no per-item failure, a cross-track duplicate replaces the source.
  Sources: https://github.com/adamjmurray/producer-pal, https://producer-pal.org, checked
  2026-10-17.
- **R-118** bschoepke/ableton-live-mcp (230 stars, Show HN 2026-05-03, 123 points, 79
  comments) uses the Live Object Model and was built with Codex. It added a semantic sample
  search by querying the SQLite database behind Live's "Find Similar Sounds". Its issues: strict
  MCP clients rejected three tools that lacked `inputSchema.type: "object"`, and a user asked for
  "a safe first session" for onboarding. Source: https://news.ycombinator.com/item?id=47999656,
  https://github.com/bschoepke/ableton-live-mcp, checked 2026-10-17.
- **R-119** REAPER has the most mature crop. TwelveTake-Studios/reaper-mcp v1.9.0 (MIT, listed
  in the MCP Registry as `com.twelvetake/reaper-mcp`) talks to REAPER through files using a stock
  Lua bridge script and a JSFX analyser, with no ports and no extra installs. It ships
  workflow-level tools (`setup_sidechain_compression`, `add_mastering_chain`,
  `add_parallel_compression`, `create_bus`, `get_project_summary`) as well as raw ones.
  bonfire-systems/reaper-mcp uses python-reapy's distant API, which must be enabled by a
  script. shiehn/total-reaper-mcp claims coverage of all of ReaScript. Sources:
  https://github.com/TwelveTake-Studios/reaper-mcp,
  https://github.com/bonfire-systems/reaper-mcp, checked 2026-10-17.
- **R-120** Logic Pro: MongLong0214/logic-pro-mcp (Swift, macOS 14+, v3.18.0, MIT, pushed
  2026-10-17) calls itself "stateful, fail-closed" with "live project readback". Its README says
  it was selected for Anthropic's Claude for Open Source programme. koltyj/logic-pro-mcp uses 8
  dispatcher tools plus 7 resources. Neither works on Windows, which is where we develop. Source:
  https://github.com/MongLong0214/logic-pro-mcp, checked 2026-10-17.
- **R-121** Other DAWs: karl-andres/fl-studio-mcp (220 stars) and calvinw/fl-studio-mcp (piano
  roll) for FL Studio; WeModulate/bitwig-mcp-server has had no push since 2025-04-10, and its
  newer peers have 0-3 stars; yoka-cubase-mcp drives Cubase over Mackie Control with
  closed-loop state checks; pyroqbit/ardour-mcp uses Ardour's OSC (port 3819). An HN commenter
  says Ardour itself "recently added MCP" for accessibility, which I could not confirm on
  ardour.org. sandraschi/vcv-rack-mcp writes VCV Rack patch JSON with no GUI automation. Sources:
  GitHub API 2026-10-17; HN comment in item 47999656.
- **R-122** Notation: tskovlund/mcp-score (MIT, alpha, Python 3.14+) has the assistant write a
  music21 script that exports MusicXML. With MuseScore 4.4.2+ open, it reads and edits the live
  score through a plugin WebSocket and renders PDF, PNG, MIDI and audio through the MuseScore
  CLI. CI tests three MuseScore versions. Dorico support is experimental. JordanSucher/musescore-mcp
  has not been pushed since 2025-04. wspringer/lilypond-mcp engraves LilyPond into PDF, SVG and
  PNG. Source: https://github.com/tskovlund/mcp-score, checked 2026-10-17.
- **R-123** Game audio middleware: BilkentAudio/Wwise-MCP (76 stars, Apache-2.0, built on WAAPI)
  says it is experimental and not for production projects. silver-rain-dev/sk-wwise-mcp is a
  modular suite. I found no FMOD Studio MCP; repos named "fmodel-mcp" are Unreal asset tools.
  Adaptive-music guidance exists only as skills (skills.sh `firzus/agent-skills/adaptive-audio`
  models music as a state machine with quantised transitions). Sources: GitHub search
  2026-10-17, https://www.skills.sh/firzus/agent-skills/adaptive-audio.

### Code-based music (live coding)

- **R-124** williamzujkowski/live-coding-music-mcp (244 stars, AGPL-3.0, npm, OIDC trusted
  publishing) drives strudel.cc through Playwright. v4.0.0 dropped 58 single-verb aliases for 28
  enum-parameterised tools (`playback({action})`, `transform({op})`, `analyze({include})`). It adds
  4 read-only resources for catalogues and a result envelope `{ok, errorCategory, isRetryable}` on
  every call. It does audio analysis (FFT, tempo, key) through Web Audio, has named multi-session
  support and MIDI import and export, and pins upstream `@strudel/*` versions. Source:
  https://github.com/williamzujkowski/live-coding-music-mcp, checked 2026-10-17.
- **R-125** p-poss/dj-claude (AGPL-3.0, npm `dj-claude`) is a Claude Code plugin with 20
  slash commands and an MCP server. Audio runs through `node-web-audio-api` with no browser, and
  the README admits that sounds "rougher" than a browser engine, with `--browser` as the fix. It
  has a headless mode (`--headless "lofi" --duration N`) and multi-agent jams over HTTP. Source:
  https://github.com/p-poss/dj-claude, checked 2026-10-17.
- **R-126** linxule/mcp-music-studio (AGPL-3.0) is a remote MCP with nothing to install. It
  draws and plays ABC-notation scores and Strudel patterns inside the chat through MCP Apps, puts
  a small piece in a share link (larger ones get a stored link that lasts 30 days), and has
  `get-music-guide` and `get-strudel-guide` reference tools. Source:
  https://github.com/linxule/mcp-music-studio, checked 2026-10-17.
- **R-127** Sonic Pi and SuperCollider have little coverage. abhishekjairath/sonic-pi-mcp (19
  stars) sends code over OSC. SuperCollider MCPs have 0-10 stars. AJBogo9's has non-real-time
  (NRT) rendering, the right route to an offline WAV. I found nothing for TidalCycles. Sonic Pi
  itself (12.2k stars) is active. Source: GitHub search 2026-10-17.
- **R-128** Strudel lives at codeberg.org/uzu/strudel (AGPL-3.0, 1262 stars, updated
  2026-10-16). Codeberg's terms now bar projects that are mostly LLM-generated (reported
  2026-07-29). The uzu community forum is sceptical of mainstream AI ("very much the opposite of
  live coding"). A NIME 2026 paper argues that AI inserting code opaquely conflicts with live
  coding's audience-visible process. So: don't host musicwright on Codeberg, don't send AI-written
  PRs upstream, and expect a cool reception in that scene. Sources:
  https://gigazine.net/news/20260729-codeberg-bans-ai-contributions/,
  https://uzu.lurk.org/t/llm-chat/6084, https://nime.org/proc/nime2026_171/, checked 2026-10-17.

### MIDI and symbolic formats

- **R-129** os-tack/fcp-midi (MIT) has the LLM send batches of compact text ops instead of
  MIDI events: `note Bass E2 at:1.1 dur:quarter vel:90`, `chord Pad Em at:1.1 dur:whole`,
  `crescendo @track:Lead vel:45-75 @range:3.1-6.4`, `tempo 174 at:11.1`. Positions are
  bar.beat. There are separate tools for query (`midi_query` map, piano roll, find) and session
  (checkpoint, undo, redo), and pretty-midi writes the file. Source:
  https://github.com/os-tack/fcp-midi, checked 2026-10-17.
- **R-130** Research view on formats: ABC gets the most LLM research of the text-based music
  formats, and LilyPond is mostly a rendering target (LILYBENCH preprint, arXiv 2606.08722).
  Studies count ABC as valid when music21 can parse it and render it to MIDI, which is a
  parseability check, not a quality check (arXiv 2407.21531). Plan for a parse-and-render
  validation step after every generation. Sources: https://arxiv.org/pdf/2606.08722,
  https://arxiv.org/pdf/2407.21531, checked 2026-10-17.
- **R-131** roomi-fields/osc-bridge maps OSC to MIDI/SysEx for 849 hardware synths and DAWs.
  feamster/digitakt-midi-mcp and morningstar-midi-mcp drive specific hardware. Hardware control
  works but is niche. Source: GitHub search 2026-10-17.

### AI generation services and models

- **R-132** Suno has no public self-serve API. In July 2026 it opened an invite-only developer
  API intake with no docs, prices or date. Every Suno MCP in use (AceDataCloud/SunoMCP 67 stars,
  CodeKeanu, sandraschi's Playwright browser driver) is unofficial and carries terms-of-service and
  reliability risk. Source:
  https://www.digitalmusicnews.com/2026/07/03/suno-is-opening-an-api-partner-program/, checked
  2026-10-17.
- **R-133** Udio disabled all downloads on 2025-10-29 after its UMG settlement (Warner settled
  2025-11-19). As of April 2026 coverage there is no confirmed return. Leave Udio out. Source:
  https://www.digitalmusicnews.com/2025/10/31/udio-downloads-disabled-umg-deal/, checked
  2026-10-17.
- **R-134** MiniMax Music 3 went open-weight on 2026-08-13 (Hugging Face, native ComfyUI
  support, songs up to about 5 minutes, 32 kHz stereo). Its community licence reportedly allows
  free commercial use under $20M annual revenue. Ports followed within weeks:
  minimaxmusic.cpp (GGML), a ComfyUI production toolkit (84 stars), MiniMax-Music3-Studio (105).
  Google Lyria 3 (30 s clips) and Lyria 3 Pro (up to 3 min) are available through the Gemini
  API and Vertex. Sources: https://kie.ai/de/blog/minimax-music-3-release,
  https://gemini.google/overview/music-generation/, GitHub search 2026-10-17. Licence text not
  read; check before recommending.
- **R-135** OpenAI has no first-party music model as of the sources found. It was reported in
  development in October 2025, and a Manifold market on confirmation by June 2026 resolved NO.
  ChatGPT and Codex users reach music through MCPs and skills like everyone else. Source:
  https://manifold.markets/MingCat/openai-confirm-work-on-a-generative, checked 2026-10-17.
- **R-136** The local, free route is the most active ecosystem: timoncool/ACE-Step-Studio (416
  stars, pushed 2026-10-17, one-click offline install), ComfyUI ACE-Step 1.5 workflows (Remix,
  Repaint), averagenative/audio-studio (ComfyUI + ACE-Step, stems, LoRAs). This fits the user's
  existing ComfyUI and ACE-Step setup and the author's preference for free tools with no attribution
  required. Source: GitHub search 2026-10-17.

### Listening services and analysis

- **R-137** Spotify's 2026-02-11 Development Mode changes (migration enforced 2026-03-09)
  require the app owner to have Premium, cap new apps at five users, removed endpoint families,
  dropped `external_ids` (ISRC) from track objects, and reportedly cut search limits to 10. The
  community Spotify MCPs (varunneal 614 stars, marcelmarais 482) are bound by those limits.
  claude.ai also offers a Spotify connector (search, playlists). Reference-track lookup is the
  only overlap with musicwright, so leave Spotify to those connectors. Source:
  https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide,
  checked 2026-10-17.
- **R-138** No audio-analysis MCP has traction (top: zachswift615/audio-analysis-mcp, 4 stars).
  uribrecher's adds Demucs stems and transcription; gwyntel's uses Gemma 4 locally. Analysis is
  done inside larger tools instead: oaustegard (R-108), bitwize QC (R-107),
  live-coding-music-mcp `analyze` (R-124), REAPER JSFX analyser (R-119). A bundled
  librosa + pyloudnorm (MIT, 783 stars) script is the gap musicwright can fill. Source: GitHub
  search 2026-10-17.

## What works and what does not (community reports)

- **R-139** Works: organising sessions. An HN commenter had Claude "organize, rename, colour,
  and prepare 100+ track songs for mixing" through an Ableton MCP and said it "works extremely
  well". The OP of the Ableton-MCP experiments post used it to pick and mash up two songs over
  two days, and agreed a person could learn the same by hand in that time. Source:
  https://news.ycombinator.com/item?id=46428922 (post 2025-12-30), read 2026-10-17.
- **R-140** Works: a producer's wish list from Show HN 47999656: (1) track layouts with empty
  clips, (2) MIDI sequences, (3) synth patches (Serum), (4) stem extraction, (5) workflow
  automation such as sidechaining, (6) semantic sample search. The author reported 1, 2 and 5
  working and later added 6. Stem splitting was not reachable from Live's API. Source:
  https://news.ycombinator.com/item?id=47999656 (2026-05-03), read 2026-10-17.
- **R-141** Poor: taste. The Show HN prompt log asked for "a real edm banger", and one reply
  was "I'm afraid Codex ignored that one". Several rounds went to fixes like "the element is a bit
  muddy", "the song is basically one volume", "doesn't seem like the new thing has any notes".
  The agent cannot hear, so each fix waits on a human listening. That is the argument for an
  automatic render-and-measure loop (R-108). Source: same thread.
- **R-142** Poor: silent failures and timeouts in DAW bridges. Writes report success but change
  nothing (R-117 issues; uisato issue "write_automation reports success but does not create clip
  envelope points", 2026-08-31). Batched updates time out with no per-item report. Guides advise
  smaller steps for timeouts. Every write needs a read-back. Sources:
  https://github.com/adamjmurray/producer-pal/issues,
  https://github.com/uisato/ableton-mcp-extended/issues, checked 2026-10-17.
- **R-143** Poor: install friction. The top issues on ahujasid are all setup (control surface not
  shown, Remote Scripts folder, macOS crash). A Cycling '74 forum user reported Max crashing on
  a `.amxd` loaded from a cloned repo. TwelveTake's file bridge using only stock REAPER is the
  counterexample. Sources: R-116, https://cycling74.com/forums/producer-pal-mcp-server-running-in-node-for-max-to-control-ableton-live,
  checked 2026-10-17.
- **R-144** Tip: tool docs matter. The Ableton-MCP experiments author saw "a jump in
  efficiency" after hand-editing tool docstrings with examples of when and how to call each tool.
  Another commenter said the fix for Ableton's undocumented `.als` format is to have Claude write
  a parser for the XML. Source: https://news.ycombinator.com/item?id=46428922.
- **R-145** Culture: there is strong pushback from musicians ("for me, the point of making music
  is making it myself"). The defences that landed were AI as a tool inside the DAW (alternative
  reverbs, finishing hobby tracks) and accessibility (voice control for visually impaired users).
  "If you've gone to the trouble of setting up Ableton MCP, you've already worked harder than Suno
  requires", answered by "Suno ... has nowhere near the affordances most musicians want" and the
  idea of sketching in a DAW, rendering, then using Suno to "upscale". Positioning to take from
  this: musicwright helps the user author; it doesn't author for them. Source: HN 47999656.
- **R-146** Single-prompt composing gives "unimpressive" music: mood and genre shifts work, and a
  melody over a beat sounds decent (one Substack author, anecdotal). Source:
  https://expandmapping.substack.com/p/composing-instrumental-music-with, checked 2026-10-17.
- **R-147** Cost: bitwize says its multi-agent album pipeline "works best on the Max
  subscription" and Pro "will hit rate limits during multi-track sessions". Keep musicwright's
  default path cheap: scripts do the measuring, the model only judges. Source: R-107.

## Name collision check (musicwright)

- **R-148** No collisions found on 2026-10-17. GitHub: no repo or user named musicwright (`gh
  search repos musicwright` returned nothing; `gh api users/musicwright` 404). Code search only
  hits old expired-domain lists, so musicwright.com was registered at some point. npm
  `musicwright` 404 with no search hits; PyPI `musicwright`, `music-wright` and `music_wright`
  404; crates.io and NuGet 404; skills.sh search 0 results; web search finds only unrelated
  "Musicwrights Publishers" (a Cape Town music publisher) and the 1946 Musicwriter typewriter.
  The name fits the author's *wright family (polywright, chartwright, cinewright). Check again just
  before the first publish.

## Patterns to borrow

1. **Render, measure, change one thing (R-108).** Every generated piece gets an offline WAV
   render, a spectrogram PNG Claude can look at, and a numbers table per version (LUFS, true
   peak, clash count, tempo, key). Record twice and report take-to-take spread before calling a
   change better. This is the main fix for R-141.
2. **Read back after every write, and fail closed (R-117, R-120, R-121, R-142).** A tool that
   changes a project returns the state it read afterwards, not "done". Batch operations return
   per-item results. Treat a mismatch as an error.
3. **Small, enum-shaped tool surface and a result envelope (R-124).** Few verbs with an
   `action`/`op` parameter, read-only references as resources or `--help`, and
   `{ok, errorCategory, isRetryable}` on every result. Every tool schema has
   `inputSchema.type: "object"` (R-118).
4. **CLI first, MCP optional (R-117, R-119).** Producer Pal's REST API and TwelveTake's file
   bridge mean the same backend works with no AI and from any agent. Ship `mw.py` (standard
   library where possible, like pw.py and fw.py) and have skills call it. An MCP wrapper can
   come later.
5. **Compact semantic note syntax plus one shared events JSON (R-129, R-108).** Positions as
   bar.beat, durations by name, batched ops, checkpoint and undo. One events format (layer, t0,
   t1, midi, vel) that converts to MIDI, MusicXML, ABC and Strudel, so every tool reads the same
   notes.
6. **The score as a second sense (R-108, R-122).** Engrave notes to PNG (music21 + verovio,
   MuseScore CLI or LilyPond) and have Claude read the voicings. Validate every generated ABC,
   MusicXML or MIDI by parsing and re-rendering it (R-130).
7. **Skills for judgement, tools for access (R-112, R-113, R-115).** Keep production craft
   (ranges, masking frequencies, genre tempos, loop rules) in skills and provider or DAW details
   in separate reference files, so a new DAW or API is one new file.
8. **Workflow-level tools over raw wrappers (R-119).** One call for "sidechain this",
   "mastering chain", "project summary". Fewer round trips, fewer timeouts.
9. **Quality gates with numbers (R-107, R-114).** Audio QC before handing anything over:
   integrated LUFS, true peak, clipping, leading and trailing silence, phase and mono
   compatibility, stereo width, spectral balance, dynamic range. Always print before and after.
   Targets per destination: about -14 LUFS for streaming (bitwize and ruflo default). Game
   targets differ by platform (R-149), so read them from a table rather than hard-coding them.
10. **Loops for games are a first-class output (R-123).** Sample-accurate loop points, a tail
    check (render two passes and measure the seam), stems per layer, and a state-machine
    description of transitions for FMOD, Wwise or Unity. Nobody covers this well, so it is room
    for musicwright to stand out.
11. **Determinism (R-108, existing acestep skill).** A seed on every generator and renderer, and
    the seed recorded in the manifest, so a take can be reproduced.
12. **Headless modes with a duration (R-125).** Every renderer takes `--seconds` and exits, so
    background runs and CI work.
13. **Share links for small pieces (R-109, R-126).** Strudel code fits in a strudel.cc URL;
    ABC fits in an abcjs link. A cheap preview with no file transfer.
14. **Model tiers per skill (R-107).** Mechanical skills (import, convert, QC) on a small
    model; composition and lyric judgement on the large one.
15. **Safe first session and install doctor (R-118, R-143).** A `mw.py doctor` that finds
    MuseScore, LilyPond, ffmpeg, FluidSynth and SoundFonts, ComfyUI and ACE-Step hosts, and a
    first task that cannot damage a project.
16. **No telemetry, one instance, no shared sockets (R-116).** Say so in the README.
17. **Licence hygiene.** Most Strudel tools are AGPL-3.0 and Producer Pal is GPL-3.0: read
    for ideas, copy no code. bitwize (CC0) and MIT repos (oaustegard, fcp-midi, TwelveTake,
    mcp-score) can be borrowed from with notices. Generated-music rights: prefer local open
    weights (ACE-Step MIT); keep Suno and Udio out of default paths (R-132, R-133).
18. **Positioning (R-117, R-145).** Say "the musician remains the author" in the README, and
    lead with sketching, arranging, notation, rendering and QC, not one-prompt songs.

## Volatile claims to re-check

| Claim | Where | Checked | Re-check by |
|---|---|---|---|
| Ableton connector is docs-only; Splice connector is beta with credits | anthropic.com/news/claude-for-creative-work; mcpservers.org/remote-mcp-servers/splice | 2026-10-17 | 2027-01 |
| Extensions SDK still beta, no M4L or event triggers | attackmagazine.com (link in R-103) | 2026-10-17 | 2026-12 |
| Producer Pal at 2.4.0 with 2.5.0-rc1 | github.com/adamjmurray/producer-pal/releases | 2026-10-17 | 2026-12 |
| ahujasid/ableton-mcp PyPI ahead of `main`, has telemetry | github.com/ahujasid/ableton-mcp | 2026-10-17 | 2027-01 |
| ElevenLabs music model id `music_v2_5` | github.com/elevenlabs/skills/blob/main/music/SKILL.md | 2026-10-17 | 2026-12 |
| Suno API invite-only, no docs | digitalmusicnews.com/2026/07/03/suno-is-opening-an-api-partner-program/ | 2026-10-17 | 2026-12 |
| Udio downloads disabled | digitalmusicnews.com/2025/10/31/udio-downloads-disabled-umg-deal/ | 2026-10-17 | 2027-01 |
| MiniMax Music 3 open weights; licence under $20M revenue (licence text unread) | kie.ai/de/blog/minimax-music-3-release; Hugging Face model card | 2026-10-17 | before recommending |
| Lyria 3 limits (30 s free, Pro 3 min) | gemini.google/overview/music-generation/ | 2026-10-17 | 2027-01 |
| No OpenAI music model | manifold.markets/MingCat/openai-confirm-work-on-a-generative | 2026-10-17 | 2026-12 |
| Spotify Dev Mode limits (Premium owner, 5 users, search limit 10) | developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide | 2026-10-17 | 2027-03 |
| Codeberg bans mostly-LLM projects | gigazine.net/news/20260729-codeberg-bans-ai-contributions/ | 2026-10-17 | 2027-03 |
| Ardour ships an MCP (unconfirmed HN claim) | news.ycombinator.com/item?id=47999656; ardour.org release notes | 2026-10-17 | 2026-11 |
| skills.sh installs (strudel 135, suno-music-creator 1343; 100k+ counts look inflated) | skills.sh/api/search?q=music | 2026-10-17 | each refresh |
| No FMOD Studio MCP exists | GitHub search "fmod mcp" | 2026-10-17 | each refresh |
| Wwise-MCP marked experimental | github.com/BilkentAudio/Wwise-MCP | 2026-10-17 | 2027-01 |
| Logic Pro MCP in Claude for Open Source programme (README claim) | github.com/MongLong0214/logic-pro-mcp | 2026-10-17 | 2027-01 |
| musicwright free on GitHub, npm, PyPI, crates, NuGet, skills.sh | R-148 | 2026-10-17 | before first publish |

- **R-149** Game loudness targets are not settled in the sources found. ASWG-R001 is cited as
  -24 LUFS by one source and -23 LUFS ±2 LU by another for console, with -18 LUFS for mobile in
  a third. Read the ASWG PDF before putting numbers in a skill. Sources:
  https://www.gamedeveloper.com/audio/standardizing-loudness-in-virtual-reality,
  https://audiomediainternational.com/mobile-loudness-an-adaptive-approach/, checked 2026-10-17.
