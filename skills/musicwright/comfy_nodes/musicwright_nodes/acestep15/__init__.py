"""ACE-Step 1.5 extract for ComfyUI, vendored from ComfyUI_RyanOnTheInside (MIT, see LICENSE).

Only the 1.5 guiders, the model and tokenizer patches (applied lazily on first use) and two
nodes; the full pack's other nodes and heavy requirements are left out (research 06).
"""
import logging

logger = logging.getLogger("musicwright.acestep15")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
    logger.addHandler(h)
logger.propagate = False
