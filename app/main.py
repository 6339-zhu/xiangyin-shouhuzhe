"""FastAPI 入口。

启动：
    uvicorn app.main:app --reload --port 8000
文档：
    http://127.0.0.1:8000/docs
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import logger

app = FastAPI(
    title=settings.app_name,
    description="基于多模态大模型的方言保护与智能对话系统",
    version="0.1.0-stage0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="")


@app.on_event("startup")
async def on_startup():
    logger.info(f"{settings.app_name} 启动完成，环境={settings.app_env}")
    logger.info(f"项目根目录：{settings.project_root}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
