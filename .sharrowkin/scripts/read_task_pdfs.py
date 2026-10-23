"""Read the supplied task PDFs without modifying the original files."""
from pathlib import Path
import argparse
import sys

from pypdf import PdfReader

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--document", type=int, choices=[1, 2])
parser.add_argument("--start", type=int, default=1)
parser.add_argument("--end", type=int)
parser.add_argument("--layout", action="store_true")
args = parser.parse_args()
files = sorted(ROOT.glob("*.pdf"))
for index, path in enumerate(files, start=1):
    if args.document is not None and args.document != index:
        continue
    reader = PdfReader(path)
    print(f"\nDOCUMENT {index}: {path.name}; PAGES: {len(reader.pages)}")
    if args.document is None:
        for number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            print(f"PAGE {number}: {len(text)} characters; {text[:160]!r}")
        continue
    last_page = min(args.end or len(reader.pages), len(reader.pages))
    for number in range(args.start, last_page + 1):
        print(f"\n--- PAGE {number} ---\n")
        mode = "layout" if args.layout else "plain"
        print(reader.pages[number - 1].extract_text(extraction_mode=mode) or "[NO EXTRACTABLE TEXT]")
