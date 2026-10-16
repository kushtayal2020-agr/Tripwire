"""Public API: scan(text) -> ScanResult. Long documents are scanned in overlapping chunks."""
import os
from dataclasses import dataclass, field
from . import heuristics, classifier

THRESHOLD = float(os.environ.get("TRIPWIRE_THRESHOLD", "0.85"))
CHUNK_CHARS = 1500
OVERLAP = 200


@dataclass
class ScanResult:
    verdict: str            # "injection" or "safe"
    score: float
    reasons: list = field(default_factory=list)
    notes: list = field(default_factory=list)   # non-fatal info, e.g. "classifier_unavailable"

    @property
    def is_injection(self) -> bool:
        return self.verdict == "injection"


def chunks(text: str, size: int = CHUNK_CHARS, overlap: int = OVERLAP):
    """Split text into overlapping pieces so an attack hidden deep in a long page is still seen."""
    if len(text) <= size:
        return [text]
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step)]


def scan(text: str, use_classifier: bool = True) -> ScanResult:
    # rules are cheap, so run them on the whole document
    hits = heuristics.check(text)
    if hits:
        return ScanResult("injection", 1.0, hits)
    if not (use_classifier and classifier.available()):
        return ScanResult("safe", 0.0, [])
    best = 0.0
    for piece in chunks(text):
        s = classifier.score(piece)
        if s is None:
            return ScanResult("safe", 0.0, [], ["classifier_unavailable"])
        best = max(best, s)
        if best >= THRESHOLD:
            return ScanResult("injection", best, ["classifier"])
    return ScanResult("safe", best, [])
