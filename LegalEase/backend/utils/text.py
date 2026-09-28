import html
import re

REPLACEMENTS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2022": "-",
    "\u00a0": " ",
}

def sanitize_text(text: str) -> str:
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "", text)

def text_to_html(text: str) -> str:
    safe = html.escape(text)
    blocks = []
    for line in safe.splitlines():
        line = line.strip()
        if not line:
            blocks.append("<div class='spacer'></div>")
        elif line.startswith("#"):
            heading = line.lstrip("# ").strip()
            blocks.append(f"<h3>{heading}</h3>")
        elif line.isupper() and len(line) <= 100:
            blocks.append(f"<h3>{line}</h3>")
        else:
            blocks.append(f"<p>{line}</p>")
    return "\n".join(blocks)
