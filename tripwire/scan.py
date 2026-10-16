"""Public API: scan(text) -> ScanResult."""
from dataclasses import dataclass, field
from . import heuristics, classifier

THRESHOLD = 0.85


@dataclass
class ScanResult:
    verdict: str            # "injection" or "safe"
    score: float
    reasons: list = field(default_factory=list)

    @property
    def is_injection(self) -> bool:
        return self.verdict == "injection"


def scan(text: str, use_classifier: bool = True) -> ScanResult:
    hits = heuristics.check(text)
    if hits:
        return ScanResult("injection", 1.0, hits)
    if use_classifier and classifier.available():
        s = classifier.score(text)
        if s >= THRESHOLD:
            return ScanResult("injection", s, ["classifier"])
        return ScanResult("safe", s, [])
    return ScanResult("safe", 0.0, [])
