from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "00_inbox" / "urls" / "inbox.csv"
TOPICS = ROOT / "config" / "topics.json"


def load_topics() -> list[dict]:
    return json.loads(TOPICS.read_text(encoding="utf-8-sig"))["topics"]


def classify(title: str, url: str, notes: str, topics: list[dict]) -> str:
    text = f"{title} {url} {notes}".lower()
    scores: dict[str, int] = {}
    for topic in topics:
        scores[topic["id"]] = sum(1 for keyword in topic["keywords"] if keyword.lower() in text)
    best_topic, best_score = max(scores.items(), key=lambda item: item[1])
    return best_topic if best_score > 0 else "unclassified"


def main() -> None:
    topics = load_topics()
    rows = []
    with INBOX.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            if not row.get("topic"):
                row["topic"] = classify(row.get("title", ""), row.get("url", ""), row.get("notes", ""), topics)
            rows.append(row)

    with INBOX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Classified {len(rows)} inbox rows.")


if __name__ == "__main__":
    main()

