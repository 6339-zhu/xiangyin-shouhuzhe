# 研究计划与里程碑（2026.11 – 2027.05）

## 时间线

| 阶段 | 时间 | 主要任务 | 里程碑（计划值） |
|---|---|---|---|
| 0 | 2026.11 | 项目骨架、开题、环境搭建 | 目录可跑通 |
| 1 | 2026.11–12 | 文献调研 + 萍乡话田野采录 + 发音词典构建 | 语料 ≥ 50h |
| 2 | 2027.01–02 | ASR/TTS 基线实验 + 半监督标注管线 + 语料质检扩采 | ASR CER ≤ 25% |
| 3 | 2027.03–04 | 方言指令微调 + RAG 知识库 + 端侧轻量化 | 全链路 Demo |
| 4 | 2027.05 | 端到端评测 + 论文撰写 + 毕业答辩 | 论文成稿 |

## 可行性保障

1. **数据**：家乡萍乡话，母语者可深度参与采录、标注、评测。
2. **算力**：开源模型 + 云端训练（3050 8G 起步，必要时租云）。
3. **执行**：单人毕设体量，配合导师分阶段指导。

---

## 模型下载清单（按阶段启用）

> 在 `models/` 目录下放置，不要提交 git。

### 阶段 1 · ASR 基线

```powershell
# 方案 A：faster-whisper（推荐，速度快）
pip install faster-whisper
# 代码里指定 large-v3 会自动下载到 ~/.cache/huggingface
# 首次推理时会下载约 3GB 权重

# 方案 B：openai-whisper
pip install openai-whisper
python -c "import whisper; whisper.load_model('large-v3')"
```

### 阶段 2 · TTS 基线

```powershell
# Piper（端侧友好，CPU 可跑）
pip install piper-tts
# 下载中文语音模型：
# zh_CN-huayan-medium.onnx  +  .onnx.json
# 参考 https://github.com/rhasspy/piper
```

### 阶段 3 · RAG 基线

```powershell
pip install langchain langchain-community chromadb sentence-transformers
# Embedding 模型（首次自动下载）：
# BAAI/bge-small-zh-v1.5  (~100MB)
```

### 阶段 4 · LLM 微调

```powershell
pip install transformers peft accelerate datasets bitsandbytes
# 基座模型（从 ModelScope 下载更快，国内推荐）：
#   pip install modelscope
#   modelscope download --model Qwen/Qwen2.5-7B-Instruct
# LoRA 微调脚本：scripts/train_llm_lora.py
```

### 阶段 6 · 端侧导出

```powershell
pip install onnx onnxruntime
python scripts/export_onnx.py
```
