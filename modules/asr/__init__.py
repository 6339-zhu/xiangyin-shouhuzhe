"""方言语音识别 ASR 模块（阶段 1 启用）。

阶段 0 仅提供占位 demo，证明模块可独立运行。
"""
from __future__ import annotations


def transcribe(audio_path: str) -> str:
    """对一段方言音频做识别。

    阶段 1 接入：faster-whisper + 萍乡话 LoRA 微调。
    """
    raise NotImplementedError("阶段 1 接入 faster-whisper 后实现")


if __name__ == "__main__":
    print("[ASR 占位] 模块可导入，真实识别在阶段 1 接入 faster-whisper。")
    print("下一步：pip install faster-whisper && 下载 large-v3 权重")
