# Member A (Detection): 6 commits

Prerequisite: Member C's commits (extended `eval/testset.csv` and the new `eval/run_eval.py`) must already be on GitHub. Run `git pull --rebase` first.

Copy each folder's CONTENTS into your repo root (note the `\*`), then commit and push, in this order:

| # | Folder | Commit message |
|---|---|---|
| 1 | a1_new_patterns | Add paraphrase, AI-addressed and Hindi/Hinglish role-hijack patterns |
| 2 | a2_obfuscation | Add normalizer for leetspeak, homoglyphs and zero-width characters |
| 3 | a3_false_positives | Reduce false positives in role-hijack, secrecy and Hinglish rules |
| 4 | a4_classifier | Make classifier configurable and fail-safe when model cannot load |
| 5 | a5_chunking_cli | Scan long documents in chunks and add python -m tripwire CLI |
| 6 | a6_tests | Add regression, normalizer and scan tests |

PowerShell example (commit 1):
    Copy-Item -Recurse -Force C:\path\to\membera\a1_new_patterns\* .
    git add .
    git status        # paths must look like tripwire/heuristics.py, never a1_new_patterns/...
    git commit -m "Add paraphrase, AI-addressed and Hindi/Hinglish role-hijack patterns"
    git pull --rebase
    git push

After commit 6: `python -m pytest` should show 30 passed. Then tell Member C to re-run
`python -m eval.run_eval --markdown` and update RESULTS.md and the README table.

## Do these yourself (more commits, and honest results)
1. The 100% / 0% numbers are on a test set the rules were tuned against, so they are optimistic.
   Write 15+ NEW attacks and benign sentences you have not seen (other phrasings, other Indian languages),
   add them to `eval/testset.csv`, and fix what fails. Commit each fix separately.
2. On a machine with internet: `pip install transformers torch`, then `python -m eval.run_eval`.
   A third row, heuristics+classifier, appears once the model downloads. Check its licence on the Hugging Face model card.
3. Tune `TRIPWIRE_THRESHOLD` (default 0.85) and report the trade-off.
