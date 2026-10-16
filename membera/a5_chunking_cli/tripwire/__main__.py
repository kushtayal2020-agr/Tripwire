"""Command line: python -m tripwire "<text or file path>"   (reads stdin if no argument)"""
import os
import sys

from .scan import scan

arg = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
text = open(arg, encoding="utf-8").read() if os.path.isfile(arg) else arg
r = scan(text)
print(f"verdict={r.verdict} score={r.score:.2f} reasons={','.join(r.reasons) or '-'}")
sys.exit(1 if r.is_injection else 0)
