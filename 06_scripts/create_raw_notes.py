from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "00_inbox" / "urls" / "inbox.csv"
TEMPLATE = ROOT / "04_templates" / "source_note_template.md"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-_\u3040-\u30ff\u3400-\u9fff]+", "-", text)
    text = text.strip("-")
    return text[:80] or "untitled"


def render(template: str, row: dict) -> str:
    values = {
        "title": row.get("title", "Untitled"),
        "url": row.get("url", ""),
        "source_type": row.get("source_type", ""),
        "topic": row.get("topic", "unclassified"),
        "status": row.get("status", "new"),
        "added_at": row.get("added_at", ""),
    }
    for key, value in values.items():
        template = template.replace("{" + key + "}", value)
    return template


def main() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    created = 0
    with INBOX.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            topic = row.get("topic") or "unclassified"
            if topic == "unclassified":
                out_dir = ROOT / "00_inbox" / "unclassified_raw_notes"
            else:
                out_dir = ROOT / "01_topics" / topic / "raw_notes"
            out_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{row.get('id', 'item')}-{slugify(row.get('title', 'untitled'))}.md"
            out_path = out_dir / filename
            if out_path.exists():
                continue
            out_path.write_text(render(template, row), encoding="utf-8")
            created += 1
    print(f"Created {created} raw notes.")


if __name__ == "__main__":
    main()
