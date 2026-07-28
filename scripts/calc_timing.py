#!/usr/bin/env python3
"""
calc_timing.py — 根据文本自动计算 SRT 时间戳

支持中英文混合，按自媒体语速（略快于正常语速）计算每句时长。
输出标准 SRT 格式。

用法:
  python calc_timing.py <input.txt> [--cps 4.5] [--wps 3.0] [--gap 0.5] [--pause 0.2]

参数:
  --cps    中文语速（字/秒），默认 4.5（正常 ~3.5，自媒体略快）
  --wps    英文语速（词/秒），默认 3.0
  --gap    段落间间隔（秒），默认 0.5
  --pause  标点停顿（秒），默认 0.2
"""

import re
import sys
import argparse


def is_chinese_char(c: str) -> bool:
    """判断是否为中文字符"""
    return '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf'


def is_english_char(c: str) -> bool:
    """判断是否为英文字母"""
    return c.isascii() and c.isalpha()


def classify_text(text: str) -> list[dict]:
    """
    将文本按句子拆分，分类每个字符。
    返回: [{"char": c, "type": "cn"|"en"|"digit"|"punct"|"space"|"other"}]
    """
    result = []
    for c in text:
        if is_chinese_char(c):
            result.append({"char": c, "type": "cn"})
        elif is_english_char(c):
            result.append({"char": c, "type": "en"})
        elif c.isdigit():
            result.append({"char": c, "type": "digit"})
        elif c in '，。！？；：、,.:;!?…—\n':
            result.append({"char": c, "type": "punct"})
        elif c in ' \t\r':
            result.append({"char": c, "type": "space"})
        else:
            result.append({"char": c, "type": "other"})
    return result


def split_sentences(text: str) -> list[str]:
    """按标点拆分句子，保留标点在句尾"""
    # 按句末标点拆分
    sentences = re.split(r'(?<=[。！？!?\n])', text)
    # 再按逗号/分号拆分为更小的呼吸单元
    result = []
    for s in sentences:
        if not s.strip():
            continue
        subs = re.split(r'(?<=[，,；;：:])', s)
        result.extend([x for x in subs if x.strip()])
    return result


def calc_sentence_duration(
    text: str, cps: float = 4.5, wps: float = 3.0, pause: float = 0.2
) -> float:
    """
    计算单句时长。
    中文字按 cps 算，英文词按 wps 算，数字按中文速度。
    """
    classified = classify_text(text)
    cn_count = sum(1 for c in classified if c["type"] == "cn")
    digit_count = sum(1 for c in classified if c["type"] == "digit")

    # 英文词数：按空格和标点分词
    en_text = "".join(
        c["char"]
        for c in classified
        if c["type"] in ("en", "space", "digit")
    )
    en_words = len([w for w in re.split(r'\s+', en_text) if w.strip()])
    # 避免重复计算数字
    en_words -= digit_count  # rough correction

    punct_count = sum(1 for c in classified if c["type"] == "punct")

    duration = (
        (cn_count + digit_count) / cps
        + max(0, en_words) / wps
        + punct_count * pause
    )
    return max(0.3, duration)  # 最短 0.3 秒


def text_to_srt(
    text: str,
    cps: float = 4.5,
    wps: float = 3.0,
    gap: float = 0.5,
    pause: float = 0.2,
) -> str:
    """
    将文本转换为 SRT 格式。
    先按段落（空行）拆分，再按句子拆分。
    """
    paragraphs = re.split(r'\n\s*\n', text.strip())
    sentences = []
    for para in paragraphs:
        para_sentences = split_sentences(para)
        sentences.extend(para_sentences)
        # 段落间加间隔标记
        if para_sentences:
            sentences.append(None)  # None = 段落间隔

    # 移除末尾多余的间隔
    while sentences and sentences[-1] is None:
        sentences.pop()

    srt_lines = []
    idx = 1
    current_time = 0.0

    for sent in sentences:
        if sent is None:
            current_time += gap
            continue

        duration = calc_sentence_duration(sent, cps, wps, pause)
        start = current_time
        end = current_time + duration

        # SRT 时间格式: HH:MM:SS,mmm
        start_str = f"{int(start//3600):02d}:{int((start%3600)//60):02d}:{start%60:06.3f}".replace(".", ",")
        end_str = f"{int(end//3600):02d}:{int((end%3600)//60):02d}:{end%60:06.3f}".replace(".", ",")

        srt_lines.append(str(idx))
        srt_lines.append(f"{start_str} --> {end_str}")
        srt_lines.append(sent.strip())
        srt_lines.append("")
        idx += 1

        current_time = end

    return "\n".join(srt_lines)


def main():
    parser = argparse.ArgumentParser(
        description="根据文本自动计算 SRT 时间戳"
    )
    parser.add_argument("input", help="输入文本文件路径")
    parser.add_argument(
        "--cps", type=float, default=4.5, help="中文语速（字/秒），默认 4.5"
    )
    parser.add_argument(
        "--wps", type=float, default=3.0, help="英文语速（词/秒），默认 3.0"
    )
    parser.add_argument(
        "--gap", type=float, default=0.5, help="段落间间隔（秒），默认 0.5"
    )
    parser.add_argument(
        "--pause", type=float, default=0.2, help="标点停顿（秒），默认 0.2"
    )
    parser.add_argument(
        "-o", "--output", help="输出 SRT 文件路径（默认打印到 stdout）"
    )

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    srt = text_to_srt(text, args.cps, args.wps, args.gap, args.pause)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(srt)
        total_time = 0.0
        for line in srt.split("\n"):
            if "-->" in line:
                end_part = line.split("-->")[1].strip()
                parts = end_part.replace(",", ".").split(":")
                total_time = (
                    int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
                )
        print(f"SRT written to {args.output}")
        print(f"Total duration: {total_time:.1f}s ({total_time/60:.1f}min)")
    else:
        print(srt)


if __name__ == "__main__":
    main()
