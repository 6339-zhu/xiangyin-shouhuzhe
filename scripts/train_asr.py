"""ASR 微调脚本占位（阶段 1-2 启用）。

用法：
    python scripts/train_asr.py --config configs/asr.yaml --data data/transcripts
"""
from __future__ import annotations

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/asr.yaml")
    parser.add_argument("--data", default="data/transcripts")
    args = parser.parse_args()
    print(f"[train_asr 占位] config={args.config} data={args.data}")
    print("阶段 1-2 实现：faster-whisper + PEFT/LoRA 微调")


if __name__ == "__main__":
    main()
