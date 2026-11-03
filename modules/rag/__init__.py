"""RAG 文化知识检索模块（阶段 3 启用）。"""
from __future__ import annotations


def retrieve(query: str, top_k: int = 4) -> list[dict]:
    """检索与萍乡方言文化相关的条目。

    阶段 3 接入：ChromaDB + bge-small-zh + 知识图谱种子。
    """
    raise NotImplementedError("阶段 3 接入后实现")


if __name__ == "__main__":
    print("[RAG 占位] 模块可导入，真实检索在阶段 3 接入 ChromaDB。")
