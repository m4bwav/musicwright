# Hosted music services (checked 2026-10-17)

Paid calls need the user's go-ahead: say the price first. Prices and terms move; re-check the
linked pages before relying on them.

| Service | Route | Price | Terms that matter |
|---|---|---|---|
| Google Lyria 3.5 | Gemini API `lyria-3.5`; `response_format` for WAV | USD 0.08 a song | SynthID watermark on all output; artist voices and copyrighted lyrics blocked; no iterative editing |
| Lyria 3 Clip | `lyria-3-clip-preview`, always 30 s | USD 0.04 a clip | as above |
| Lyria RealTime | `lyria-realtime-exp` streaming session, 48 kHz PCM | not published | experimental, instrumental only; BPM 60-200, density, brightness, scale |
| ElevenLabs Music v2.5 | API `music_v2_5`, official skill and MCP | USD 0.15 a minute | commercial on paid plans, but film, TV and studio games need Enterprise; stems, inpainting |
| MiniMax Music (hosted) | API, official MCP | about USD 0.15 a song (secondary source) | API terms |
| Mureka | web, prepaid API | about USD 0.045-0.05 a song (secondary) | paid plans royalty-free |
| Suno v6 | web app only | Pro USD 8, Premier USD 24 a month | no public API: never automate it; downloads capped (Pro 20, Premier 60 a month); remixes non-commercial; Suno may fingerprint files; stream-ripping banned |
| Udio | web app | | downloads disabled since 2025-10-29; licensed platform not launched as of 2026-09 |

Pages: https://ai.google.dev/gemini-api/docs/music-generation, https://ai.google.dev/gemini-api/docs/pricing,
https://elevenlabs.io/pricing/api, https://elevenlabs.io/music, https://suno.com/pricing,
https://suno.com/legal/terms.

When a user brings a Suno or Udio track: treat it as audio to finish (musicwright-produce), check
which plan made it (free tier is personal use only), and keep the plan and date in the ledger.
