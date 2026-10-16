"""CLI used by the skill: python scripts/scan.py "<text or file path>" """
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from tripwire.scan import scan  # noqa: E402

arg = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
text = open(arg, encoding="utf-8").read() if os.path.isfile(arg) else arg
r = scan(text)
print(f"verdict={r.verdict} score={r.score:.2f} reasons={','.join(r.reasons) or '-'}")
sys.exit(1 if r.is_injection else 0)
