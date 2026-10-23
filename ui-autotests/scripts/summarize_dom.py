"""Краткая сводка сохранённых элементов без служебных токенов форм."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1] / "reports" / "inspection"
for path in root.glob("*.json"):
    print(path.stem)
    for e in json.loads(path.read_text(encoding="utf-8")):
        if e["type"] == "hidden" or (not e["text"] and not e["id"]):
            continue
        print(e["tag"], e["id"], e["type"], ascii(e["text"][:250]), ascii(e["html"][:350]))
