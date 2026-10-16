"""Normalize common text obfuscations before applying detection rules."""
import re
import unicodedata

ZERO_WIDTH = re.compile(
    "[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\U000e0000-\U000e007f]"
)
LEET = str.maketrans(
    {"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"}
)
HOMOGLYPHS = str.maketrans(
    {
        "а": "a",
        "е": "e",
        "о": "o",
        "р": "p",
        "с": "c",
        "і": "i",
        "у": "y",
        "х": "x",
        "ο": "o",
        "α": "a",
        "ε": "e",
        "ι": "i",
    }
)
TOKEN = re.compile(r"[A-Za-z0-9@$]+")


def _fix_token(match: re.Match) -> str:
    token = match.group(0)
    has_letter = any(char.isalpha() for char in token)
    has_leet = any(char in "013457@$" for char in token)
    if len(token) >= 4 and has_letter and has_leet:
        return token.translate(LEET)
    return token


def normalize(text: str) -> str:
    """Remove invisible characters and normalize common homoglyph/leet substitutions."""
    text = ZERO_WIDTH.sub("", text)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(HOMOGLYPHS)
    return TOKEN.sub(_fix_token, text)
