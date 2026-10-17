# Other music tools for agents (checked 2026-10-17)

What exists beside musicwright, when to point the user at it, and what not to depend on.
Full notes with sources: ai-docs/research/02-agent-tools-and-workflows.md. Stars and dates move;
re-check before recommending.

## Use when the user has the software

| Need | Tool | Note |
|---|---|---|
| Control Ableton Live | Producer Pal (GPL-3.0, MCP + REST) or ahujasid/ableton-mcp (MIT) | Install friction is the top complaint; read back after every write |
| Control REAPER | TwelveTake-Studios/reaper-mcp (MIT) | Stock REAPER, file bridge, one-call workflow tools |
| Notation, MuseScore | tskovlund/mcp-score (MIT) | MusicXML plus live MuseScore editing |
| Sample search | Splice connector (official, beta) | Royalty-free samples |
| Hosted generation, paid | ElevenLabs official skill and MCP (`music_v2_5`) | Self-serve plans exclude film, TV and studio games |
| Hear what it wrote (symbolic) | oaustegard/claude-skills `listening-to-music` (MIT) | Renders, spectrograms, engraved score, one change at a time |

## Borrow ideas, not code

- bitwize-music-studio/claude-ai-music-skills (CC0): album pipeline, 7-point audio QC, -14 LUFS mastering.
- Strudel MCPs and skills (mostly AGPL-3.0): live-coded patterns; Strudel itself is on Codeberg
  and its community is wary of AI. Read for ideas, copy nothing.
- os-tack/fcp-midi (MIT): compact bar.beat note syntax.

## Do not automate

- Suno: no public API; every "Suno API" is an unofficial wrapper against its terms. Describe the
  manual route only.
- Udio: downloads have been off since 2025-10-29.

## Positioning

People who make music push back hard on agents that author for them. Lead with sketching,
arranging, notation, rendering and checking; the user stays the author of anything they release.
