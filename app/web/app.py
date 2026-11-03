"""Streamlit 前端 Demo。

启动（推荐在项目根目录执行）：
    cd D:\python_demo\乡音守护者
    streamlit run app\web\app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# 把项目根目录加入 sys.path，避免直接 streamlit run 绝对路径时
# 报 "No module named 'app.core'; 'app' is not a package"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import json
import shutil
from datetime import datetime

import streamlit as st

from app.core.config import settings

st.set_page_config(
    page_title="乡音守护者",
    page_icon="🗣️",
    layout="wide",
)

# 路径准备
CORPUS_DIR = settings.data_dir / "corpus"
TRANSCRIPT_DIR = settings.data_dir / "transcripts"
CORPUS_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

st.title("🗣️ 乡音守护者")
st.caption("基于多模态大模型的方言保护与智能对话系统 · 首期试点：赣语萍乡话")

tab_collect, tab_asr, tab_chat, tab_about = st.tabs(
    ["🎙️ 采集", "👂 识别 ASR", "💬 对话", "ℹ️ 关于"]
)

# ============ Tab 1：采集 ============
with tab_collect:
    st.subheader("方言语料采集")
    st.caption("田野采录 / 众包录入：上传一段萍乡话音频，登记发音人信息，自动入语料库。")

    with st.form("collect_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            audio_file = st.file_uploader(
                "上传音频（wav / mp3 / m4a）",
                type=["wav", "mp3", "m4a", "flac"],
            )
            speaker_age = st.selectbox("发音人代际", ["老年(60+)", "中年(30-59)", "青年(15-29)"])
            speaker_gender = st.radio("性别", ["男", "女"], horizontal=True)
        with col2:
            speaker_id = st.text_input("发音人编号（如 PX-001）", value="PX-001")
            transcript = st.text_area(
                "转写文本（可选，先留空后续标注）",
                placeholder="把这段音频说的话用普通话/萍乡话记下来……",
            )
            scene = st.selectbox("场景", ["日常对话", "朗读句子", "歌谣童谣", "俗语采集", "其他"])

        submitted = st.form_submit_button("💾 保存到语料库", type="primary")

    if submitted:
        if audio_file is None:
            st.warning("请先选择一段音频文件。")
        else:
            # 1) 保存音频到 data/corpus/
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = Path(audio_file.name).suffix.lower()
            audio_name = f"{speaker_id}_{ts}{ext}"
            audio_path = CORPUS_DIR / audio_name
            with open(audio_path, "wb") as f:
                shutil.copyfileobj(audio_file, f)

            # 2) 追加一条 JSONL 标注到 data/transcripts/
            record = {
                "id": f"{speaker_id}_{ts}",
                "audio": str(audio_path.relative_to(settings.data_dir)),
                "speaker_id": speaker_id,
                "speaker_age": speaker_age,
                "speaker_gender": speaker_gender,
                "scene": scene,
                "transcript": transcript.strip(),
                "duration_sec": None,  # TODO 阶段 1 用 librosa 读时长
                "is_annotated": bool(transcript.strip()),
                "created_at": ts,
            }
            jsonl_path = TRANSCRIPT_DIR / "pingxiang_corpus.jsonl"
            with open(jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

            st.success(f"✅ 已保存：{audio_name}")
            st.json(record)

    # 展示当前语料库统计
    st.divider()
    st.markdown("### 语料库现状")
    jsonl_path = TRANSCRIPT_DIR / "pingxiang_corpus.jsonl"
    if jsonl_path.exists():
        # 用 utf-8-sig 读，自动兼容 Windows 写文件时可能带的 BOM
        raw = jsonl_path.read_text(encoding="utf-8-sig").strip()
        lines = raw.splitlines()
        records = [json.loads(x) for x in lines if x.strip()]
        c1, c2, c3 = st.columns(3)
        c1.metric("已录入条数", len(records))
        annotated = sum(1 for r in records if r["is_annotated"])
        c2.metric("已标注", annotated)
        c3.metric("待标注", len(records) - annotated)
        with st.expander("查看最近 5 条"):
            for r in records[-5:]:
                st.write(f"- `{r['id']}` [{r['speaker_age']}/{r['speaker_gender']}] "
                         f"{r['transcript'] or '（未标注）'}")
    else:
        st.info("还没有语料，上传第一条音频试试。")

# ============ Tab 2：ASR（占位）============
with tab_asr:
    st.subheader("方言语音识别 ASR")
    st.warning("阶段 1 接入 faster-whisper + 萍乡话 LoRA 微调后开放。")
    st.code("""# 目标接口（下一步实现）
from modules.asr import transcribe
text = transcribe("data/corpus/PX-001_20261103_xxx.wav")
""", language="python")

# ============ Tab 3：对话 ============
with tab_chat:
    st.subheader("乡音陪聊（DeepSeek 驱动）")
    st.caption("用萍乡话或普通话提问，模型会给出方言说法 + 文化解释。")

    model_choice = st.selectbox(
        "模型",
        ["qwen-plus", "qwen-turbo", "deepseek-v3（需百炼控制台开通）", "deepseek-r1（需百炼控制台开通）"],
        help="qwen-plus 现在可用；deepseek 需在阿里云百炼控制台单独开通付费",
    )
    # 映射回真实模型名
    model_map = {
        "qwen-plus": "qwen-plus",
        "qwen-turbo": "qwen-turbo",
        "deepseek-v3（需百炼控制台开通）": "deepseek-v3",
        "deepseek-r1（需百炼控制台开通）": "deepseek-r1",
    }
    model_choice = model_map[model_choice]

    # 初始化对话历史
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 展示历史
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 输入框
    user_input = st.chat_input("比如：萍乡话「戳卵」是什么意思？")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            try:
                from modules.llm import chat as llm_chat
                with st.spinner("DeepSeek 思考中…"):
                    reply = llm_chat(
                        [{"role": m["role"], "content": m["content"]}
                         for m in st.session_state.chat_history],
                        model=model_choice,
                    )
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"调用失败：{e}")

    if st.button("🗑️ 清空对话"):
        st.session_state.chat_history = []
        st.rerun()

# ============ Tab 4：关于 ============
with tab_about:
    st.subheader("关于本项目")
    st.markdown(
        """
- **项目**：乡音守护者 —— 基于多模态大模型的方言保护与智能对话系统
- **试点方言**：赣语（萍乡话）
- **目标**：方言「采集 → 识别 → 合成 → 对话」全链路
- **毕设周期**：2026.11 – 2027.05
- **指标**：ASR CER ≤ 15% / TTS MOS ≥ 4.0 / 对话延迟 < 2s
        """
    )
