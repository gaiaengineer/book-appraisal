#!/usr/bin/env python3
"""Extract plain text + structure from a manuscript (epub, docx, pdf, txt, md).

Stdlib-only for epub/docx/txt/md. PDF needs pdfminer.six (or `pdftotext` on PATH).

Usage:
    python3 extract_book.py <book_path> [--out <workdir>]

Writes into <workdir> (default: ./.appraisal_work/<book_stem>/):
    full.txt       normalised plain text, blank-line separated paragraphs
    manifest.json  word count, paragraph offsets, detected section headings
"""

import argparse
import html
import json
import os
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------- text utils

TAG_RE = re.compile(r"<[^>]+>")
BLOCK_END_RE = re.compile(r"</(p|div|h[1-6]|li|br|tr)\s*>|<br\s*/?>", re.I)
WS_RE = re.compile(r"[ \t ]+")


def html_to_text(markup: str) -> str:
    markup = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", markup)
    markup = BLOCK_END_RE.sub("\n\n", markup)
    text = TAG_RE.sub("", markup)
    return html.unescape(text)


def normalise(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("­", "")          # soft hyphen
    text = WS_RE.sub(" ", text)
    lines = [ln.strip() for ln in text.split("\n")]
    out, blank = [], False
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return "\n".join(out).strip()


# ---------------------------------------------------------------- extractors


def extract_epub(path: Path) -> str:
    """Read the OPF spine so chapters come out in reading order."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        try:
            container = ET.fromstring(z.read("META-INF/container.xml"))
            rootfile = container.find(".//{*}rootfile").get("full-path")
        except Exception:
            cands = [n for n in names if n.lower().endswith(".opf")]
            if not cands:
                raise SystemExit("epub: no OPF package document found")
            rootfile = cands[0]

        opf = ET.fromstring(z.read(rootfile))
        base = os.path.dirname(rootfile)
        idmap = {
            item.get("id"): item.get("href")
            for item in opf.iterfind(".//{*}manifest/{*}item")
        }
        spine = [
            idmap.get(ref.get("idref"))
            for ref in opf.iterfind(".//{*}spine/{*}itemref")
        ]
        hrefs = [h for h in spine if h]
        if not hrefs:
            hrefs = [n for n in names if n.lower().endswith((".xhtml", ".html", ".htm"))]

        parts = []
        for href in hrefs:
            member = os.path.normpath(os.path.join(base, href)).replace(os.sep, "/")
            if member not in names:
                member = next((n for n in names if n.endswith(os.path.basename(href))), None)
                if member is None:
                    continue
            raw = z.read(member).decode("utf-8", "replace")
            chunk = normalise(html_to_text(raw))
            if chunk:
                parts.append(chunk)
    return "\n\n".join(parts)


def extract_docx(path: Path) -> str:
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
    paras = []
    for p in doc.iter(f"{W}p"):
        runs = [t.text or "" for t in p.iter(f"{W}t")]
        line = "".join(runs).strip()
        style = p.find(f"{W}pPr/{W}pStyle")
        if line and style is not None and "Heading" in (style.get(f"{W}val") or ""):
            line = f"## {line}"
        if line:
            paras.append(line)
    return "\n\n".join(paras)


def extract_pdf(path: Path) -> str:
    try:
        from pdfminer.high_level import extract_text  # type: ignore
        return extract_text(str(path)) or ""
    except ImportError:
        pass
    import shutil
    import subprocess
    if shutil.which("pdftotext"):
        return subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            capture_output=True, text=True, check=True,
        ).stdout
    raise SystemExit(
        "PDF support needs pdfminer.six or poppler.\n"
        "  pip install pdfminer.six      # or: brew install poppler"
    )


def extract_txt(path: Path) -> str:
    return path.read_text("utf-8", errors="replace")


EXTRACTORS = {
    ".epub": extract_epub, ".docx": extract_docx, ".pdf": extract_pdf,
    ".txt": extract_txt, ".md": extract_txt, ".markdown": extract_txt,
}

# ---------------------------------------------------------------- structure

HEADING_RE = re.compile(
    r"^(##\s+.+|(?:chapter|part|book|prologue|epilogue|interlude)\b.{0,60}|"
    r"[IVXLC]{1,7}|\d{1,3})$",
    re.I,
)


def find_headings(paras, cum_words):
    out = []
    for i, p in enumerate(paras):
        if len(p) <= 70 and HEADING_RE.match(p.strip()):
            out.append({"paragraph": i, "word_offset": cum_words[i],
                        "text": p.strip().lstrip("# ")})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    src = Path(args.book).expanduser()
    if not src.exists():
        raise SystemExit(f"not found: {src}")
    ext = src.suffix.lower()
    if ext not in EXTRACTORS:
        raise SystemExit(f"unsupported format {ext!r}; supported: {', '.join(EXTRACTORS)}")

    text = normalise(EXTRACTORS[ext](src))
    paras = [p for p in text.split("\n\n") if p.strip()]
    words = [len(p.split()) for p in paras]
    total = sum(words)

    if total < 2000:
        sys.stderr.write(
            f"WARNING: only {total} words extracted. If this is a scanned PDF it "
            "needs OCR first (e.g. ocrmypdf) — do not appraise from this.\n"
        )

    cum, run = [], 0
    for w in words:
        cum.append(run)
        run += w

    out_dir = Path(args.out) if args.out else Path(".appraisal_work") / src.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "full.txt").write_text("\n\n".join(paras), "utf-8")

    manifest = {
        "source": str(src.resolve()),
        "format": ext.lstrip("."),
        "total_words": total,
        "paragraphs": len(paras),
        "paragraph_word_offsets": cum,
        "headings": find_headings(paras, cum)[:400],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), "utf-8")

    print(json.dumps({
        "workdir": str(out_dir), "total_words": total,
        "paragraphs": len(paras), "headings_found": len(manifest["headings"]),
    }, indent=2))


if __name__ == "__main__":
    main()
