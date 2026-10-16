"""Layer 2: open-weight prompt-injection classifier (runs locally, no API calls).

Configure with environment variables:
  TRIPWIRE_MODEL   Hugging Face model id (default: protectai/deberta-v3-base-prompt-injection-v2)
  TRIPWIRE_DEVICE  -1 for CPU (default) or a GPU index
"""
import os

MODEL_ID = os.environ.get("TRIPWIRE_MODEL", "protectai/deberta-v3-base-prompt-injection-v2")  # verify license on model card
DEVICE = int(os.environ.get("TRIPWIRE_DEVICE", "-1"))

_pipe = None
_load_failed = False


def available() -> bool:
    """True if transformers is installed and the model has not failed to load."""
    if _load_failed:
        return False
    try:
        import transformers  # noqa: F401
        return True
    except ImportError:
        return False


def _load():
    global _pipe, _load_failed
    if _pipe is None:
        try:
            from transformers import pipeline
            _pipe = pipeline("text-classification", model=MODEL_ID, truncation=True,
                             max_length=512, device=DEVICE)
        except Exception as exc:  # no internet, model missing, out of memory...
            _load_failed = True
            print(f"[tripwire] classifier unavailable ({type(exc).__name__}); using rules only")
            return None
    return _pipe


def warmup() -> bool:
    """Load the model now (call once at start-up). Returns True if it is ready."""
    return _load() is not None


def score(text: str):
    """Probability (0-1) that the text is a prompt injection, or None if the classifier is unavailable."""
    pipe = _load()
    if pipe is None:
        return None
    out = pipe(text)[0]
    return out["score"] if out["label"].upper().startswith("INJ") else 1.0 - out["score"]
