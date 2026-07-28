#!/usr/bin/env python3
"""Static preflight for text-bearing video asset projects.

Checks common licensing and layout risks before rendering. This script is
conservative: it cannot prove a font license or visual correctness.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TEXT_EXTENSIONS = {".html", ".css", ".js", ".ts", ".tsx", ".jsx"}
FONT_EXTENSIONS = {".ttf", ".otf", ".woff", ".woff2"}


def collect_files(root: Path, extensions: set[str]) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in extensions]


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight a video asset project")
    parser.add_argument("project", type=Path, help="project directory")
    args = parser.parse_args()

    root = args.project.resolve()
    if not root.is_dir():
        print(f"BLOCK: project directory does not exist: {root}")
        return 2

    source_files = collect_files(root, TEXT_EXTENSIONS)
    font_files = collect_files(root, FONT_EXTENSIONS)
    combined = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in source_files)
    font_names = " ".join(p.name.lower() for p in font_files)

    blocks: list[str] = []
    warnings: list[str] = []

    has_puhuiti_file = any(token in font_names for token in ("puhui", "pu-hui", "普惠"))
    has_puhuiti_css = bool(re.search(r"Alibaba\s+PuHuiTi|阿里巴巴普惠体", combined, re.I))
    has_chinese = bool(re.search(r"[\u3400-\u9fff]", combined))

    if has_chinese and not (has_puhuiti_file and has_puhuiti_css):
        blocks.append(
            "Chinese text detected but a local Alibaba PuHuiTi file and matching CSS declaration "
            "were not both found. Warn the user and do not render text-bearing finals."
        )

    if re.search(r"font-family\s*:[^;]*(Microsoft YaHei|SimHei|Arial)", combined, re.I):
        warnings.append("Unapproved/system font fallback detected; do not assume commercial permission.")

    patterns = {
        "translate(-50%) centering": r"translate(?:X|Y)?\(\s*-50%",
        "GSAP xPercent/yPercent": r"\b[xy]Percent\s*:",
        "non-deterministic Math.random": r"Math\.random\s*\(",
        "Windows absolute path": r"[A-Za-z]:[\\/]Users[\\/]",
        "file URI": r"file://",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, combined, re.I):
            warnings.append(f"{label} detected; inspect before rendering.")

    if not source_files:
        warnings.append("No HTML/CSS/JS/TS source files found.")
    if has_chinese and not font_files:
        blocks.append("Chinese text detected but no local font files were found.")

    print(f"PROJECT={root}")
    print(f"SOURCE_FILES={len(source_files)}")
    print(f"FONT_FILES={len(font_files)}")
    for item in blocks:
        print(f"BLOCK: {item}")
    for item in warnings:
        print(f"WARN: {item}")

    if blocks:
        print(f"RESULT=BLOCKED ({len(blocks)} block, {len(warnings)} warning)")
        return 2
    print(f"RESULT=PASS ({len(warnings)} warning)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
