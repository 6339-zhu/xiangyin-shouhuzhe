"""文化知识图谱模块（阶段 3 启用）。

条目类型：俗语 / 歌谣 / 典故 / 非遗。
"""
from __future__ import annotations

import json
from pathlib import Path

from app.core.config import settings

KG_PATH = settings.data_dir / "kg" / "pingxiang_knowledge_seed.json"


def load_entries() -> list[dict]:
    """加载种子知识条目。"""
    if not KG_PATH.exists():
        return []
    with open(KG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("entries", [])


if __name__ == "__main__":
    entries = load_entries()
    print(f"[KG] 已加载 {len(entries)} 条萍乡文化种子知识。")
    for e in entries[:3]:
        print(f" - [{e.get('category')}] {e.get('title')}")
