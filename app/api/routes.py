"""FastAPI 路由占位。

阶段 0 只暴露健康检查 + 各模块占位路由，真实接口在后续阶段接入。
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.core.logging import logger
from modules.llm import chat as llm_chat

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    model: str | None = None


@router.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "app": "乡音守护者",
        "message": "Hello, 乡音守护者！项目骨架已就绪。",
    }


@router.get("/api/v1/asr/status")
async def asr_status():
    """ASR 占位 —— 阶段 1 接入"""
    return {"module": "asr", "status": "placeholder", "todo": "faster-whisper 加载 + 萍乡话推理"}


@router.get("/api/v1/tts/status")
async def tts_status():
    """TTS 占位 —— 阶段 2 接入"""
    return {"module": "tts", "status": "placeholder", "todo": "Piper/Coqui 加载 + 方言发音词典"}


@router.get("/api/v1/llm/status")
async def llm_status():
    """LLM 占位 —— 阶段 4 接入"""
    return {"module": "llm", "status": "placeholder", "todo": "Qwen2.5-7B + LoRA 微调"}


@router.get("/api/v1/rag/status")
async def rag_status():
    """RAG 占位 —— 阶段 3 接入"""
    return {"module": "rag", "status": "placeholder", "todo": "ChromaDB + bge-small-zh"}


@router.get("/api/v1/kg/status")
async def kg_status():
    """文化知识图谱占位 —— 阶段 3 接入"""
    return {"module": "knowledge_graph", "status": "placeholder", "todo": "5000 条俗语/歌谣/非遗"}


@router.post("/api/v1/chat")
async def chat(req: ChatRequest):
    """方言对话接口（当前走 DashScope DeepSeek）。"""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message 不能为空")
    try:
        reply = llm_chat(
            [{"role": "user", "content": req.message}],
            model=req.model,
        )
        return {"reply": reply, "model": req.model or settings.llm_model}
    except Exception as e:
        logger.exception("LLM 调用失败")
        raise HTTPException(status_code=500, detail=f"LLM 调用失败：{e}")
