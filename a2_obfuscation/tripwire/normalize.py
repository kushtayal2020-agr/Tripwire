"""Undo common obfuscation tricks so rules can still match (leetspeak, homoglyphs, zero-width chars)."""
import re
import unicodedata

ZERO_WIDTH = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\U000e0000-\U000e007f]")
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
# Cyrillic / Greek look-alikes -> Latin
HOMOGLYPHS = str.maketrans({"а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "і": "i", "у": "y", "х": "x",
                            "ο": "o", "α": "a", "ε": "e", "ι": "i"})
TOKEN = re.compile(r"[A-Za-z0-9@$]+")


def _fix_token(m: re.Match) -> str:
    tok = m.group(0)
    has_letter = any(c.isalpha() for c in tok)
    has_leet = any(c in "013457@$" for c in tok)
    # only touch words that mix letters with digits/symbols, e.g. "1gnore", "prev1ous"
    if len(tok) >= 4 and has_letter and has_leet:
        return tok.translate(LEET)
    return tok


def normalize(text: str) -> str:
    text = ZERO_WIDTH.sub("", text)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(HOMOGLYPHS)
    return TOKEN.sub(_fix_token, text)
