# Train and use a style LoRA (ACE-Step 1.5)

Checked 2026-11-13 (R-20261113-2). Training measured on one run. The first blind verdict (2026-11-14, LEARNINGS L-003) found the slide adapter no better than its base model, so nothing here is a recipe.

## Data and captions

- Clips of at most about 120 s, each with `<clip>.caption.txt`, `<clip>.lyrics.txt` (`[Instrumental]`) and a dataset.json listing them.
- Every caption starts with a trigger word nobody else uses (`slidesteel`, `fretwood`), then generic style words. Put era and noise words (`1920s, vintage mono 78rpm recording, surface noise`) in the caption so the hiss binds to them, not to the trigger; leave them out at generation time.
- Never a performer's name in a caption or file name.
- Licence tag per set, kept beside the adapter: **sellable** (public-domain recordings, CC0, own recordings) or **personal-only** (anything else). A personal-only adapter never goes into a product that may be sold, and stores that ask get an AI disclosure either way. See [licences.md](licences.md).

## Train with Side-Step (two runs)

Side-Step ships in the ACE-Step 1.5 repository (`train.py`). It refuses paths outside its own root ("Path escapes safe root"): keep tensors in `preprocessed_tensors/<name>` and output in `lora_output/<name>` under the ACE-Step checkout. The dataset JSON may live anywhere. `--preprocess` only preprocesses; training is a second run.

```
python train.py --plain --yes fixed --checkpoint-dir ./checkpoints --model-variant turbo --preprocess --dataset-json /abs/dataset.json --tensor-output ./preprocessed_tensors/<name> --max-duration 125
python train.py --plain --yes fixed --checkpoint-dir ./checkpoints --model-variant turbo --dataset-dir ./preprocessed_tensors/<name> --output-dir ./lora_output/<name> --adapter-type lokr --epochs 100 --save-every 10 --offload-encoder
```

- Measured on a 16 GB RTX 5060 Ti: about 8.9 GB VRAM in use during training, about 2 min per epoch over about 100 clips (so 100 epochs is about 3.3 h). Progress goes to TensorBoard (`lora_output/<name>/runs`), not the console.
- Checkpoints: `lora_output/<name>/checkpoints/epoch_N_loss_X/lokr_weights.safetensors` (LyCORIS LoKr, keys `lycoris_<decoder module>`; metadata names the algo and targets, by default q/k/v/o projections).

## Use it in ComfyUI (native nodes, no custom pack)

ComfyUI's LoRA loader already maps `lycoris_*` and `base_model.model.*` keys onto the ACE-Step 1.5 decoder, and its weight adapters include LoKr, so no key conversion is needed. What must match is the **model size**: an adapter trained on turbo (2B, hidden 2048) does not fit the XL files (hidden 2560) and loads nothing. An adapter trained on the XL SFT model fits `acestep_v1.5_xl_sft_bf16` in ComfyUI (360 modules matched, 2026-11-14) and runs on the acestep-xl-sft recipe.

1. Put the DiT it was trained on into `models/diffusion_models`. For turbo, the checkout's `checkpoints/acestep-v15-turbo/model.safetensors` has the same key layout as the ComfyUI repackaged files and loads in UNETLoader as is (copy it as e.g. `acestep_v1.5_turbo_bf16.safetensors`, 4.8 GB).
2. Check and install the adapter:
   `mw.py lora-check <lokr_weights.safetensors> --unet <models/diffusion_models/that file> --install <ComfyUI>/models/loras --name <trigger>_turbo_lokr_eN`
   It reports matched modules, keys ComfyUI will not map and shape mismatches (the wrong model size), and copies only when everything fits.
3. Generate with the LoRA chained after the UNETLoader (`LoraLoaderModelOnly`, repeat `--lora` to stack):
   `mw.py gen --recipe acestep-xl-sft --set "{\"unet\":\"acestep_v1.5_turbo_bf16.safetensors\"}" --steps 8 --cfg 1.0 --sampler euler --scheduler simple --lora <file>:1.0 --caption "<trigger>, <style words>" ...`
   Turbo is distilled: the ACE-Step docs recommend 8 steps; cfg 1.0 is the usual distilled setting and has not been judged here. Sweep strength (0.6, 0.8, 1.0) on fixed seeds and let the listener pick.
4. Or open [workflows/acestep15-turbo-lora.api.json](workflows/acestep15-turbo-lora.api.json) in ComfyUI (API format, the same graph) and change the LoRA name, strength and caption.
