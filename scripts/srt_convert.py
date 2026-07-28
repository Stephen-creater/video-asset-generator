#!/usr/bin/env python3
"""
srt_convert.py — 各种字幕格式转 SRT

支持: VTT (WebVTT), ASS/SSA, 纯文本时间戳
输出: 标准 SRT 格式

用法:
  python srt_convert.py <input> [-o output.srt]
"""

import re
import sys
import argparse


def detect_format(text: str) -> str:
    """自动检测字幕格式"""
    if text.strip().startswith("WEBVTT"):
        return "vtt"
    if "[Events]" in text and "Format:" in text:
        return "ass"
    # 纯时间戳行检测
    lines = text.strip().split("\n")
    timestamp_lines = [l for l in lines if re.match(r'^\[?\d{1,2}:', l)]
    if len(timestamp_lines) > 0:
        return "plain"
    return "unknown"


def vtt_to_srt(text: str) -> str:
    """WebVTT → SRT"""
    lines = text.strip().split("\n")
    # Skip WEBVTT header
    start = 0
    for i, line in enumerate(lines):
        if "-->" in line:
            start = i - 1 if i > 0 else 0
            break

    srt_lines = []
    idx = 1
    i = start
    while i < len(lines):
        line = lines[i].strip()
        if "-->" in line:
            # Convert VTT timestamp to SRT (replace . with ,)
            ts = line.replace(".", ",")
            srt_lines.append(str(idx))
            srt_lines.append(ts)
            # Collect text
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip() and "-->" not in lines[i]:
                text_lines.append(lines[i].strip())
                i += 1
            srt_lines.append(" ".join(text_lines))
            srt_lines.append("")
            idx += 1
        else:
            i += 1
    return "\n".join(srt_lines)


def ass_to_srt(text: str) -> str:
    """ASS/SSA → SRT (仅提取 Dialogue 行)"""
    srt_lines = []
    idx = 1
    for line in text.split("\n"):
        if not line.startswith("Dialogue:"):
            continue
        # Dialogue: layer, start, end, style, name, marginL, marginR, marginV, effect, text
        parts = line.split(",", 9)
        if len(parts) < 10:
            continue
        start = parts[1].strip()
        end = parts[2].strip()
        content = parts[9].strip()
        # Remove ASS tags like {\i1}, {\b0}, etc.
        content = re.sub(r'\{[^}]*\}', '', content)
        # Remove \N newlines
        content = content.replace("\\N", " ")

        # Convert ASS time (H:MM:SS.cc) to SRT (HH:MM:SS,mmm)
        start = start.replace(".", ",")
        end = end.replace(".", ",")
        # Pad centiseconds to milliseconds
        if "," in start and len(start.split(",")[1]) == 2:
            start += "0"
        if "," in end and len(end.split(",")[1]) == 2:
            end += "0"

        srt_lines.append(str(idx))
        srt_lines.append(f"{start} --> {end}")
        srt_lines.append(content)
        srt_lines.append("")
        idx += 1
    return "\n".join(srt_lines)


def plain_to_srt(text: str) -> str:
    """纯文本时间戳 → SRT
    支持格式:
      [00:01.000] 文本内容
      00:01.000 文本内容
      00:01.000 - 00:05.000 文本内容
    """
    srt_lines = []
    idx = 1
    lines = text.strip().split("\n")

    for i, line in enumerate(lines):
        # Match [timestamp] or timestamp at start
        m = re.match(
            r'^\[?(\d{1,2}:\d{2}[.:]\d{2,3})\]?\s*[-–]\s*\[?(\d{1,2}:\d{2}[.:]\d{2,3})\]?\s*(.*)',
            line,
        )
        if m:
            start = m.group(1).replace(".", ",")
            end = m.group(2).replace(".", ",")
            content = m.group(3).strip()
        else:
            m = re.match(
                r'^\[?(\d{1,2}:\d{2}[.:]\d{2,3})\]?\s*(.*)', line
            )
            if not m:
                continue
            start = m.group(1).replace(".", ",")
            content = m.group(2).strip()
            # Estimate end from next line or add 3s
            next_match = None
            for j in range(i + 1, min(i + 5, len(lines))):
                nm = re.match(
                    r'^\[?(\d{1,2}:\d{2}[.:]\d{2,3})\]?', lines[j]
                )
                if nm:
                    next_match = nm
                    break
            if next_match:
                end = next_match.group(1).replace(".", ",")
            else:
                # Add 3 seconds
                parts = start.replace(",", ".").split(":")
                secs = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2]) + 3
                h = int(secs // 3600)
                m = int((secs % 3600) // 60)
                s = secs % 60
                end = f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

        if not content:
            continue

        srt_lines.append(str(idx))
        srt_lines.append(f"{start} --> {end}")
        srt_lines.append(content)
        srt_lines.append("")
        idx += 1

    return "\n".join(srt_lines)


def main():
    parser = argparse.ArgumentParser(description="字幕格式转 SRT")
    parser.add_argument("input", help="输入字幕文件路径")
    parser.add_argument("-o", "--output", help="输出 SRT 文件路径（默认 stdout）")
    parser.add_argument(
        "-f",
        "--format",
        choices=["vtt", "ass", "plain", "auto"],
        default="auto",
        help="输入格式（默认自动检测）",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    fmt = args.format if args.format != "auto" else detect_format(text)

    converters = {"vtt": vtt_to_srt, "ass": ass_to_srt, "plain": plain_to_srt}

    if fmt not in converters:
        print(f"Error: Unable to detect or unsupported format: {fmt}", file=sys.stderr)
        sys.exit(1)

    srt = converters[fmt](text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(srt)
        print(f"Converted {fmt.upper()} → SRT: {args.output}")
    else:
        print(srt)


if __name__ == "__main__":
    main()
