from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS_ROOT = ROOT / "01_topics"
OUTPUT = ROOT / "03_outputs" / "weekly_digest"
UNCLASSIFIED = ROOT / "00_inbox" / "unclassified_raw_notes"


def raw_note_links(raw_dir: Path) -> list[str]:
    if not raw_dir.exists():
        return []
    notes = [path for path in sorted(raw_dir.glob("*.md")) if path.name.lower() != "readme.md"]
    return [f"- [[{note.relative_to(ROOT).as_posix()[:-3]}]]" for note in notes[-10:]]


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    out_path = OUTPUT / f"{today}.md"
    lines = [f"# Weekly Digest: {today}", "", "## New Raw Notes", ""]
    for topic_dir in sorted(TOPICS_ROOT.iterdir()):
        if not topic_dir.is_dir():
            continue
        lines.append(f"### {topic_dir.name}")
        lines.append("")
        links = raw_note_links(topic_dir / "raw_notes")
        lines.extend(links or ["- No raw notes yet."])
        lines.append("")
    unclassified_links = raw_note_links(UNCLASSIFIED)
    if unclassified_links:
        lines.append("### unclassified")
        lines.append("")
        lines.extend(unclassified_links)
        lines.append("")
    lines.extend(["## Review Notes", "", "- ", "", "## Promote to Wiki", "", "- "])
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created {out_path}")


if __name__ == "__main__":
    main()
