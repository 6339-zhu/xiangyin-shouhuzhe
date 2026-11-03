"""方言语音合成 TTS 模块（阶段 2 启用）。"""
from __future__ import annotations


def synthesize(text: str, out_path: str) -> str:
    """把文字合成为方言语音。

    阶段 2 接入：Piper / Coqui + 萍乡话发音词典。
    """
    raise NotImplementedError("阶段 2 接入后实现")


if __name__ == "__main__":
    print("[TTS 占位] 模块可导入，真实合成在阶段 2 接入 Piper/Coqui。")
