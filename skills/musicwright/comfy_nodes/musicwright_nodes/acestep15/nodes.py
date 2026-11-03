"""Two nodes for ACE-Step 1.5 extract, adapted from ComfyUI_RyanOnTheInside nodes.py (MIT, see LICENSE).

Names carry an MW prefix so they never clash with the full pack if both are installed.
Extract needs the base checkpoint (acestep_v1.5_xl_base_bf16), not sft or turbo.
"""
from . import patches
from .ace_step_guiders_v15 import ACEStep15NativeExtractGuider

TRACKS = ["vocals", "drums", "bass", "guitar", "keyboard", "strings",
          "percussion", "synth", "fx", "brass", "woodwinds", "backing_vocals"]


class MWAceStep15TaskTextEncode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "clip": ("CLIP",),
            "text": ("STRING", {"multiline": True, "default": ""}),
            "task_type": (["text2music", "repaint", "cover", "extract", "lego"],),
            "track_name": (["None"] + TRACKS, {"default": "None"}),
            "lyrics": ("STRING", {"multiline": True, "default": ""}),
            "bpm": ("INT", {"default": 120, "min": 10, "max": 300}),
            "duration": ("FLOAT", {"default": 60.0, "min": 1.0, "max": 2000.0, "step": 0.1}),
            "keyscale": ("STRING", {"default": "C major"}),
            "timesignature": (["2", "3", "4", "6"], {"default": "4"}),
            "language": ("STRING", {"default": "en"}),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffff}),
        }}

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "conditioning"

    def encode(self, clip, text, task_type, track_name, lyrics, bpm, duration, keyscale, timesignature, language, seed):
        patches.apply_acestep_patches()
        tokens = clip.tokenize(text, lyrics=lyrics, bpm=bpm, duration=duration, keyscale=keyscale,
                               timesignature=int(timesignature), language=language, seed=seed,
                               task_type=task_type, track_name=None if track_name == "None" else track_name,
                               cfg_scale=2.0, temperature=0.85, top_p=0.9, top_k=0, min_p=0.0)
        return (clip.encode_from_tokens_scheduled(tokens),)


class MWAceStep15ExtractGuider:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "model": ("MODEL",),
            "positive": ("CONDITIONING",),
            "negative": ("CONDITIONING",),
            "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 100.0, "step": 0.1}),
            "source_latents": ("LATENT",),
            "track_name": (TRACKS,),
        }}

    RETURN_TYPES = ("GUIDER",)
    FUNCTION = "get_guider"
    CATEGORY = "sampling/custom_sampling/guiders"

    def get_guider(self, model, positive, negative, cfg, source_latents, track_name):
        patches.apply_acestep_patches()
        src = source_latents["samples"]
        if src.ndim != 3 or src.shape[1] != 64:
            raise ValueError(f"ACE-Step 1.5 needs a (batch, 64, length) latent, got {tuple(src.shape)}")
        return (ACEStep15NativeExtractGuider(model, positive, negative, cfg, src, track_name),)


NODE_CLASS_MAPPINGS = {"MWAceStep15TaskTextEncode": MWAceStep15TaskTextEncode,
                       "MWAceStep15ExtractGuider": MWAceStep15ExtractGuider}
NODE_DISPLAY_NAME_MAPPINGS = {"MWAceStep15TaskTextEncode": "ACE-Step 1.5 Task Text Encode (musicwright)",
                              "MWAceStep15ExtractGuider": "ACE-Step 1.5 Extract Guider (musicwright)"}
