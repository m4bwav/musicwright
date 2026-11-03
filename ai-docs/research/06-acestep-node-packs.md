# ACE-Step node packs for extract (2026-11-03)

Owed item 7 waited on picking a community node pack for ACE-Step extract inside ComfyUI. Mark asked for packs to be downloaded for research. Three were cloned (depth 1, not installed, nothing run) to `Ai/Music/node-pack-research/` on the owner's machine.

| Pack | Last commit | Licence | Extract | How it runs |
|---|---|---|---|---|
| ryanontheinside/ComfyUI_RyanOnTheInside (`nodes/acestep/`) | 2026-03-20 | MIT | yes: `ACEStep15NativeExtractGuider` ("Extract the {TRACK_NAME} track from the audio:"), also Lego, Cover, Edit | native ComfyUI model, a CFGGuider subclass; no ACE-Step library |
| ace-step/ACE-Step-ComfyUI (official) | 2026-03-01 | MIT | no (text2music, cover, repaint, audio codes) | HTTP client to the ACE-Step server, cloud or local; same as the REST route mw.py already has |
| hiroki-abe-58/ComfyUI-AceMusic | 2026-02-09 | Apache 2.0 | no | wraps the ACE-Step Python library (pip install from git), needs that venv |

## Ruling

Use the RyanOnTheInside extract guider. Do not install the whole pack into the shared ComfyUI: its requirements pull in pymunk, pygame, openunmix, opencv and scikit-image, and it registers hundreds of unrelated nodes. Instead copy the acestep guider code (MIT, keep the notice) into musicwright's own `comfy_nodes/`, next to AudioLatentRepaintMask, and wire `mw.py gen --task extract`.

Bonus for the cover item: the same pack has `ACEStep15SemanticExtractor` and a cover guider that feeds semantic hints from the source latent. That is the "cover with source audio codes" route still owed in item 7.

Extract runs on the base model only (models.md), so the recipe needs the base checkpoint, not XL sft.

Sources: the three repositories above; search lead from a r/StableDiffusion post (Feb 2026) listing extract and lego as wip, now implemented in the v15 guiders.
