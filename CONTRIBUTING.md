# Contributing

1. Fork or branch, and keep changes focused.
2. Add an attack or benign example to `eval/testset.csv` for any rule you change.
3. Run `python -m pytest` and `python -m eval.run_eval` before opening a pull request.
4. Use clear commit messages, for example `add Marathi override patterns`.

Found an attack Tripwire misses? Open an issue with the text (redact any real secrets).
