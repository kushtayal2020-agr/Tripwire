"""Public API: scan(text) -> ScanResult."""
import os
from dataclasses import dataclass, field
from . import heuristics, classifier

THRESHOLD = float(os.environ.get("TRIPWIRE_THRESHOLD", "0.85"))


@dataclass
class ScanResult:
    verdict: str            # "injection" or "safe"
    score: float
    reasons: list = field(default_factory=list)
    notes: list = field(default_factory=list)   # non-fatal info, e.g. "classifier_unavailable"

    @property
    def is_injection(self) -> bool:
        return self.verdict == "injection"


def scan(text: str, use_classifier: bool = True) -> ScanResult:
    hits = heuristics.check(text)
    if hits:
        return ScanResult("injection", 1.0, hits)
    if use_classifier and classifier.available():
        s = classifier.score(text[:2000])
        if s is None:
            return ScanResult("safe", 0.0, [], ["classifier_unavailable"])
        if s >= THRESHOLD:
            return ScanResult("injection", s, ["classifier"])
        return ScanResult("safe", s, [])
    return ScanResult("safe", 0.0, [])
