"""Layer 2: open-weight prompt-injection classifier (runs locally, no API calls)."""
MODEL_ID = "protectai/deberta-v3-base-prompt-injection-v2"  # verify license on the model card

_pipe = None


def available() -> bool:
    try:
        import transformers  # noqa: F401
        return True
    except ImportError:
        return False


def _load():
    global _pipe
    if _pipe is None:
        from transformers import pipeline
        _pipe = pipeline("text-classification", model=MODEL_ID, truncation=True, max_length=512)
    return _pipe


def score(text: str) -> float:
    """Probability (0-1) that the text is a prompt injection."""
    out = _load()(text[:2000])[0]
    return out["score"] if out["label"].upper().startswith("INJ") else 1.0 - out["score"]
