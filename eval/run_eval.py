"""Run: python -m eval.run_eval   (adds a classifier column if `transformers` is installed)"""
import csv
import re
from tripwire import classifier
from tripwire.scan import scan

rows = list(csv.DictReader(open("eval/testset.csv", encoding="utf-8")))
KEYWORD = re.compile(r"ignore (all )?(previous|prior) instructions", re.I)

systems = {
    "keyword-only": lambda t: bool(KEYWORD.search(t)),
    "heuristics": lambda t: scan(t, use_classifier=False).is_injection,
}
if classifier.available():
    systems["heuristics+classifier"] = lambda t: scan(t).is_injection


def metrics(fn, subset):
    atk = [r for r in subset if r["label"] == "1"]
    ben = [r for r in subset if r["label"] == "0"]
    det = sum(fn(r["text"]) for r in atk) / max(len(atk), 1)
    fpr = sum(fn(r["text"]) for r in ben) / max(len(ben), 1)
    return det, fpr


print(f"{'system':<24}{'subset':<8}{'detection':>10}{'false-pos':>11}")
for name, fn in systems.items():
    for lang in ("all", "en", "hi"):
        subset = rows if lang == "all" else [r for r in rows if r["lang"] == lang]
        d, f = metrics(fn, subset)
        print(f"{name:<24}{lang:<8}{d:>9.0%}{f:>11.0%}")
