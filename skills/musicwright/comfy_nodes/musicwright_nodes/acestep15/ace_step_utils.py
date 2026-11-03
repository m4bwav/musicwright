# Vendored from ryanontheinside/ComfyUI_RyanOnTheInside nodes/acestep/ace_step_utils.py at 52daf66 (MIT, see LICENSE).
# Only extract_semantic_hints is kept; the silence-latent download is not needed by the cover guider.
import torch
import comfy.model_management
from . import logger


def extract_semantic_hints(model, source_latent, verbose=True):
    """
    Extract semantic hints from source audio latents for Cover/Extract tasks.

    This extracts the semantic structure of the audio (rhythm, melody, harmony)
    while abstracting away the timbre. Used by Cover and Extract guiders.

    Args:
        model: ComfyUI ModelPatcher wrapping the ACE-Step 1.5 model
        source_latent: Source audio latent in ComfyUI format [B, 64, T]
        verbose: Whether to print diagnostic information

    Returns:
        torch.Tensor: Semantic hints in ComfyUI format [B, 64, T]
    """
    logger.debug(f"[SEMANTIC_EXTRACT] input latent shape={source_latent.shape}, mean={source_latent.mean():.4f}, std={source_latent.std():.4f}")

    prefix = "[SEMANTIC_EXTRACT]"

    # Validate v1.5 shape: (batch, 64, length)
    if len(source_latent.shape) != 3 or source_latent.shape[1] != 64:
        raise ValueError(f"ACE-Step 1.5 requires latent shape (batch, 64, length), got {source_latent.shape}")

    # Get the diffusion model (AceStepConditionGenerationModel)
    diffusion_model = model.model.diffusion_model

    if not hasattr(diffusion_model, 'tokenizer') or not hasattr(diffusion_model, 'detokenizer'):
        raise RuntimeError(
            "Model does not have tokenizer/detokenizer. "
            "Make sure you're using an ACE-Step 1.5 model."
        )

    # Load model to GPU
    comfy.model_management.load_model_gpu(model)

    device = comfy.model_management.get_torch_device()
    dtype = model.model.get_dtype()

    # Move source tensor to model device/dtype
    # Source is in ComfyUI format: [B, D, T] = [B, 64, length]
    # Tokenizer expects: [B, T, D] = [B, length, 64]
    source_on_device = source_latent.to(device=device, dtype=dtype)
    source_transposed = source_on_device.movedim(-1, -2)  # [B, T, D]

    if verbose:
        logger.debug(f"{prefix} Extracting from source shape: {source_latent.shape}")
        logger.debug(f"{prefix}   source stats: mean={source_transposed.mean():.4f}, std={source_transposed.std():.4f}")

    # Verify weights are on GPU
    tokenizer_device = next(diffusion_model.tokenizer.parameters()).device
    if verbose:
        logger.debug(f"{prefix}   tokenizer on: {tokenizer_device}, target: {device}")

    # Step 1: Tokenize - get quantized embeddings at 5Hz
    with torch.no_grad():
        quantized, indices = diffusion_model.tokenizer.tokenize(source_transposed)

    if verbose:
        logger.debug(f"{prefix}   quantized shape: {quantized.shape}")
        logger.debug(f"{prefix}   quantized stats: mean={quantized.mean():.4f}, std={quantized.std():.4f}")

    # Step 2: Detokenize - upsample from 5Hz to 25Hz
    # Use quantized directly (not get_output_from_indices) to avoid redundant computation
    with torch.no_grad():
        lm_hints = diffusion_model.detokenizer(quantized)

    if verbose:
        logger.debug(f"{prefix}   lm_hints shape: {lm_hints.shape}")
        logger.debug(f"{prefix}   lm_hints stats: mean={lm_hints.mean():.4f}, std={lm_hints.std():.4f}")
        if lm_hints.std() < 0.01:
            logger.warning(f"{prefix}   Very low variance in semantic hints!")

    # Transpose back to ComfyUI format: [B, T, D] → [B, D, T]
    semantic_hints = lm_hints.movedim(-1, -2)

    logger.debug(f"[SEMANTIC_EXTRACT] output hints shape={semantic_hints.shape}, mean={semantic_hints.mean():.4f}, std={semantic_hints.std():.4f}")

    return semantic_hints
