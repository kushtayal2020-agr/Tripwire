"""Run: python -m eval.run_eval [--markdown]
Compares keyword-only vs heuristics (vs heuristics+classifier if `transformers` is installed).
--markdown also writes eval/RESULTS.md. Failures are listed so teammates can improve the rules."""
import csv
import re
import sys
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
    return det, fpr, len(atk), len(ben)


lines = ["| System | Subset | Attacks | Benign | Detection rate | False-positive rate |",
         "|---|---|---|---|---|---|"]
for name, fn in systems.items():
    for lang, label in (("all", "All"), ("en", "English"), ("hi", "Hindi/Hinglish")):
        subset = rows if lang == "all" else [r for r in rows if r["lang"] == lang]
        d, f, na, nb = metrics(fn, subset)
        lines.append(f"| {name} | {label} | {na} | {nb} | {d:.0%} | {f:.0%} |")
table = "\n".join(lines)
print(table)

best_name = list(systems)[-1]
best = systems[best_name]
missed = [r["text"] for r in rows if r["label"] == "1" and not best(r["text"])]
false_pos = [r["text"] for r in rows if r["label"] == "0" and best(r["text"])]
print(f"\nMissed attacks ({best_name}): {len(missed)}")
for t in missed:
    print("  -", t)
print(f"False positives ({best_name}): {len(false_pos)}")
for t in false_pos:
    print("  -", t)

if "--markdown" in sys.argv:
    with open("eval/RESULTS.md", "w", encoding="utf-8") as f:
        f.write(f"# Evaluation results\n\n{len(rows)} test strings (`eval/testset.csv`).\n\n{table}\n\n")
        f.write(f"## Missed attacks ({best_name})\n" + "".join(f"- {t}\n" for t in missed) or "")
        f.write(f"\n## False positives ({best_name})\n" + "".join(f"- {t}\n" for t in false_pos))
    print("\nWrote eval/RESULTS.md")
