"""Load the knowledge base: kb/KB-NN-*.md -> {"KB-NN": {"title", "text"}}."""
import re
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent / "kb"


def load() -> dict:
    articles = {}
    for path in sorted(KB_DIR.glob("KB-*.md")):
        text = path.read_text()
        m = re.match(r"# (KB-\d\d) (.+)", text)
        articles[m.group(1)] = {"title": m.group(2).strip(), "text": text}
    return articles


def as_prompt(articles: dict) -> str:
    return "\n\n".join(a["text"].strip() for a in articles.values())
