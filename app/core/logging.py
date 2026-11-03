"""统一日志：loguru 封装。"""
from __future__ import annotations

import sys
from loguru import logger

from app.core.config import settings

logger.remove()
logger.add(
    sys.stdout,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level:<7}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)
logger.add(
    "logs/xiangyin_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="14 days",
    level=settings.log_level,
    encoding="utf-8",
)

__all__ = ["logger"]
