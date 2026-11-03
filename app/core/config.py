"""全局配置：从 .env 读取，统一注入其他模块。"""
from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # 通用
    app_name: str = "乡音守护者"
    app_env: str = "dev"
    log_level: str = "INFO"

    # 路径
    project_root: Path = Path(__file__).resolve().parents[2]
    models_dir: Path = project_root / "models"
    data_dir: Path = project_root / "data"

    # ASR
    asr_model_size: str = "large-v3"
    asr_language: str = "zh"
    asr_initial_prompt: str = "以下是萍乡话普通话夹杂的普通话转写文本。"

    # TTS
    tts_model_name: str = "piper"
    tts_voice: str = "zh_CN-huayan-medium"
    tts_device: str = "cpu"

    # LLM
    llm_provider: str = "dashscope"          # dashscope / local
    llm_model: str = "qwen-plus"               # qwen-plus / qwen-turbo / deepseek-v3 / deepseek-r1
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscope_api_key: str = ""
    llm_lora_weights: str = ""
    llm_device: str = "cuda"
    llm_max_new_tokens: int = 1024
    llm_temperature: float = 0.7

    # RAG
    rag_embed_model: str = "BAAI/bge-small-zh-v1.5"
    rag_vector_dir: str = "./data/chroma"
    rag_top_k: int = 4

    # DB
    db_url: str = "sqlite:///./data/xiangyin.db"


settings = Settings()
