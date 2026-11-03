"""方言大模型对话模块。

当前实现：通过 DashScope（阿里云百炼）OpenAI 兼容端点调用 DeepSeek。
后续阶段 4 切换为本地 Qwen2.5 + LoRA，保持同样的 chat() 接口。
"""
from __future__ import annotations

from openai import OpenAI

from app.core.config import settings
from app.core.logging import logger

# 系统提示词：乡音守护者人设（萍乡话方言助手）
SYSTEM_PROMPT = """你是「乡音守护者」，一位熟悉赣语萍乡话的方言文化助手。
回答规则：
1. 先用普通话解释清楚意思；
2. 再给一句萍乡话的说法；
3. 涉及俗语/典故/非遗时，补充来历和文化背景；
4. 如果用户用萍乡话提问，回应里保留萍乡话腔调和典型用词（如「恰饭」「克哪里」「冇」）；
5. 不知道就直说，不要编造。
"""

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.dashscope_api_key:
            raise RuntimeError("未配置 DASHSCOPE_API_KEY，请检查 .env")
        _client = OpenAI(
            api_key=settings.dashscope_api_key,
            base_url=settings.llm_base_url,
        )
    return _client


def chat(messages: list[dict], model: str | None = None) -> str:
    """调用大模型对话。

    Args:
        messages: [{"role":"user","content":"..."}, ...]
        model: 覆盖默认模型（默认 deepseek-v3）

    Returns:
        模型回复文本
    """
    client = _get_client()
    payload = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    logger.info(f"调用 LLM：model={model or settings.llm_model}, messages={len(payload)}")
    resp = client.chat.completions.create(
        model=model or settings.llm_model,
        messages=payload,
        max_tokens=settings.llm_max_new_tokens,
        temperature=settings.llm_temperature,
    )
    return resp.choices[0].message.content or ""


if __name__ == "__main__":
    # 直接跑：python -m modules.llm
    reply = chat([{"role": "user", "content": "萍乡话「恰饭」是什么意思？"}])
    print("=== DeepSeek 回复 ===")
    print(reply)
