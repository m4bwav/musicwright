# Licences, ownership and disclosure (checked 2026-10-17; not legal advice)

## Who owns AI music

- US Copyright Office (Part 2, 2025-01-29): purely AI-generated material is not protectable;
  prompts alone are not authorship; human selection, arrangement and changes can be. The Supreme
  Court declined Thaler v. Perlmutter on 2026-03-02.
- So "you own the output" in a model licence (ACE-Step, Stability, Suno paid) is a contract term
  with the vendor, not a copyright the user can enforce. Human-written lyrics, human edits and
  arrangement are where protectable authorship lives. Keep the ledger: it documents the human part.

## Model terms at a glance

| Model | Commercial use of outputs | Conditions |
|---|---|---|
| ACE-Step 1.5 (MIT) | yes | README warns about stylistic similarity; check originality, disclose AI use |
| MiniMax Music 3 | yes under USD 20M revenue | show "MiniMax-Music3" in the product UI; disclose AI content |
| YuE2 | individuals yes, companies need a licence | CC BY-NC 4.0 weights with a creator permission |
| Stable Audio 3 | yes under USD 1M revenue | Stability Community Licence; Enterprise above |
| MusicGen | no | CC BY-NC 4.0 |
| Lyria | per Gemini API terms | SynthID watermark stays in the audio |
| ElevenLabs | paid plans | not film, TV or studio games without Enterprise |
| Suno | paid tiers, within the download cap | remixes non-commercial; free tier personal only |

## Platform rules

- **Steam**: the Content Survey covers AI content that ships with the game and is consumed by
  players, sound included. Pre-generated music: describe it.
- **YouTube**: disclose realistic AI content, including AI music that is the focus of a video,
  with "AI use" in Studio.
- **Spotify**: supports DDEX AI credits; removes tracks that imitate another artist's voice
  without permission; filters spam and mass uploads.
- **Deezer**: tags AI tracks; demonetises fraud-linked streams.
- **Distributors**: DistroKid accepts with disclosure; CD Baby rejects fully AI works; TuneCore
  takes licensed-model output (re-check each help centre at release).
- **EU AI Act Art. 50**: disclosure duties from 2026-08-02; machine-readable marking of synthetic
  audio provisionally from 2026-12-02.

## Disclosure lines (fill in and store in music.json `disclosure`)

- Game store: "Music was generated with <model> (<licence>) from prompts written by <studio>,
  then selected, edited and mixed by <studio>."
- Video description: "Music: AI-generated with <model>, edited by <name>."
- MiniMax Music 3 in a product: include the text "MiniMax-Music3" where users see credits.
