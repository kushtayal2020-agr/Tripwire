"""Layer 1: fast rule-based checks (English, Hinglish, Hindi, hidden content)."""
import re

from .normalize import normalize

F = re.IGNORECASE | re.DOTALL

PATTERNS = [
    # English
    ("en_ignore_instructions", r"\b(ignore|disregard|forget|override)\b.{0,30}\b(previous|prior|above|earlier|all|any)\b.{0,30}\b(instructions?|prompts?|rules|directions?)\b"),
    ("en_role_hijack", r"\b(you are now (an?|the|in|dan)\b|from now on you are|act as if you have no restrictions)"),
    ("en_reveal_prompt", r"\b(reveal|print|show|repeat|leak)\b.{0,25}\b(system prompt|hidden instructions|your instructions)\b"),
    ("en_secrecy", r"\b(do not|don't|without)\b.{0,15}\b(tell|inform|notify|alert)\b.{0,15}\bthe user\b"),
    ("en_new_instructions", r"\b(new|updated) (instructions?|task)\s*:"),
    # Hinglish (romanised Hindi)
    ("hinglish_ignore_a", r"\b(ignore|bhul\s*jao|bhool\s*jao|andekha|nazarandaz)\b.{0,40}\b(instructions?|nirdesh|aadesh|commands?)\b"),
    ("hinglish_ignore_b", r"\b(instructions?|nirdesh|aadesh|commands?)\b.{0,40}\b(ignore|bhul\s*jao|bhool\s*jao|andekha|nazarandaz)\b"),
    ("hinglish_secrecy", r"\buser\s+ko\s+(mat|na)\s+(batao|bataana|batana)\b"),
    # Hindi (Devanagari)
    ("hi_ignore_a", r"(अनदेखा|भूल\s*जाओ|इग्नोर).{0,40}(निर्देश|आदेश)"),
    ("hi_ignore_b", r"(निर्देश|आदेश).{0,40}(अनदेखा|भूल\s*जाओ|इग्नोर)"),
]
COMPILED = [(name, re.compile(p, F)) for name, p in PATTERNS]

# zero-width, bidi controls, and Unicode "tag" characters (used to smuggle text)
HIDDEN_UNICODE = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\U000e0000-\U000e007f]")
HIDDEN_HTML = re.compile(r"(display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0|opacity\s*:\s*0(?:\.0+)?\b|color\s*:\s*#?fff(?:fff)?\b)", re.I)
BASE64_BLOB = re.compile(r"[A-Za-z0-9+/]{80,}={0,2}")


def check(text: str) -> list[str]:
    """Return the list of rule names that matched (empty list = clean)."""
    hits = [name for name, rx in COMPILED if rx.search(text)]
    normalized = normalize(text)
    if normalized != text:
        hits.extend(
            f"obfuscated:{name}"
            for name, rx in COMPILED
            if rx.search(normalized) and name not in hits
        )
    if len(HIDDEN_UNICODE.findall(text)) >= 3:
        hits.append("hidden_unicode")
    if HIDDEN_HTML.search(text):
        hits.append("hidden_html")
    if BASE64_BLOB.search(text):
        hits.append("base64_blob")
    return hits
