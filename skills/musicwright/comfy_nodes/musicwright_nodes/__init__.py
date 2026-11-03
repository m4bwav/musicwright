"""musicwright nodes: time-range repaint mask for 1D audio latents (ACE-Step 1.5).

KSampler blends with a latent's noise_mask each step (comfy/samplers.py KSamplerX0Inpaint):
1 = regenerate, 0 = keep the source. comfy.utils.reshape_mask takes a [B,1,T] mask for
1D latents and repeats it across channels, so this node only builds that tensor.
"""
import torch


class AudioLatentRepaintMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "samples": ("LATENT",),
            "start_s": ("FLOAT", {"default": 10.0, "min": 0.0, "max": 1000.0, "step": 0.01}),
            "end_s": ("FLOAT", {"default": 20.0, "min": 0.0, "max": 1000.0, "step": 0.01}),
            "fade_s": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.01}),
            "frames_per_s": ("FLOAT", {"default": 25.0, "min": 1.0, "max": 1000.0, "step": 0.01}),
        }}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "build"
    CATEGORY = "latent/audio"

    def build(self, samples, start_s, end_s, fade_s, frames_per_s):
        lat = samples["samples"]
        if lat.ndim != 3:
            raise ValueError(f"expected a [B,C,T] audio latent, got shape {tuple(lat.shape)}")
        t = (torch.arange(lat.shape[-1], dtype=torch.float32) + 0.5) / frames_per_s
        if fade_s > 0:
            mask = torch.minimum(((t - start_s) / fade_s + 1).clamp(0, 1),
                                 ((end_s - t) / fade_s + 1).clamp(0, 1))
        else:
            mask = ((t >= start_s) & (t < end_s)).float()
        out = samples.copy()
        out["noise_mask"] = mask.reshape(1, 1, -1)
        return (out,)


NODE_CLASS_MAPPINGS = {"AudioLatentRepaintMask": AudioLatentRepaintMask}
NODE_DISPLAY_NAME_MAPPINGS = {"AudioLatentRepaintMask": "Audio Latent Repaint Mask"}

try:
    from .acestep15.nodes import NODE_CLASS_MAPPINGS as _X, NODE_DISPLAY_NAME_MAPPINGS as _XN
    NODE_CLASS_MAPPINGS.update(_X)
    NODE_DISPLAY_NAME_MAPPINGS.update(_XN)
except ImportError as e:  # ComfyUI without ACE-Step 1.5 support: repaint still loads
    print(f"[musicwright_nodes] ACE-Step 1.5 extract nodes not loaded: {e}")
