"""Command line interface for scanning text or files."""
import argparse
import json
import sys
from pathlib import Path

from .scan import scan


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan text or a file for prompt injection.")
    parser.add_argument("text_or_file", nargs="?", help="text to scan or path to a UTF-8 file (default: stdin)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--no-classifier", action="store_true", help="use heuristic rules only")
    args = parser.parse_args()

    text = args.text_or_file if args.text_or_file is not None else sys.stdin.read()
    if args.text_or_file is not None:
        path = Path(args.text_or_file)
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                parser.error(f"cannot read {path}: {exc}")

    result = scan(text, use_classifier=not args.no_classifier)
    if args.json:
        print(json.dumps({
            "verdict": result.verdict,
            "score": result.score,
            "reasons": result.reasons,
        }))
    else:
        print(f"verdict={result.verdict} score={result.score:.2f} reasons={','.join(result.reasons) or '-'}")
    return 1 if result.is_injection else 0


if __name__ == "__main__":
    sys.exit(main())
