# 乡音守护者

> 基于多模态大模型的方言保护与智能对话系统
>
> 南昌交通学院 · 人工智能学院 · 智能科学与技术专业 · 毕业设计（2026.11 – 2027.05）

让方言从「被存档」走向「被使用」：建成方言 **采集 → 识别 → 合成 → 对话** 全链路 AI 平台，首期试点 **赣语（萍乡话）**。

---

## 一、项目背景

- 方言加速流失：教育部语保工程数据显示，超 80.8% 汉语方言点存在青少年传承断层。
- 老年数字鸿沟：只会说方言的老人听不懂普通话 AI 助手，被智能服务挡在门外。
- 现有方言 AI 多停留在「单点识别」，缺少能听、会说、能聊的完整闭环。

**核心问题**：能否构建「采集—识别—合成—对话」全链路方言 AI 平台，让方言从「被存档」走向「被使用」？

## 二、技术指标（立项目标，非已实现）

| 模块 | 目标指标 |
|---|---|
| 方言语音识别 ASR | 试点方言字错误率 CER ≤ 15%（准确率 ≥ 85%），支持普通话夹方言 |
| 方言语音合成 TTS | 合成自然度 MOS ≥ 4.0，保留萍乡话腔调 |
| 方言大模型对话 | 纯方言提问 + 文化知识问答，响应延迟 < 2s |
| 方言语料库 | 首期自采 + 众包 ≥ 200 小时标注语料（老中青三代） |
| 文化知识图谱 | ≥ 5000 条（俗语、歌谣、典故、非遗） |
| 端侧部署 | 核心识别能力可在手机端离线运行（量化/剪枝） |

## 三、技术栈

- **Python 3.11**
- **ASR**：faster-whisper / openai-whisper + LoRA(PEFT) 迁移微调
- **TTS**：Coqui TTS 或 Piper（端侧友好），注入方言发音词典
- **LLM**：Qwen2.5-7B/14B-Instruct + LoRA 指令微调
- **RAG**：LangChain + ChromaDB + 文化知识图谱（JSON / Neo4j）
- **后端**：FastAPI（REST + WebSocket，音频流式）
- **前端**：第一阶段 Streamlit 快速 Demo；第二阶段 Vue3 + Element Plus
- **端侧**：ONNX 量化导出
- **数据**：方言拼音转写、发音词典 CSV、SQLite/PostgreSQL

## 四、目录结构

```
乡音守护者/
├── app/                    # FastAPI 后端 + Streamlit 前端
├── modules/                # 各 AI 模块（asr/tts/llm/rag/kg/dataset）
├── configs/                # 各模块 yaml 配置
├── data/                   # 语料、发音词典、知识图谱（不入 git）
├── models/                 # 预训练权重（不入 git）
├── scripts/                # 训练 / 构建 / 导出脚本
├── docs/                   # 架构、里程碑、评测方案
├── tests/                  # 单元测试
├── requirements.txt
├── .env.example
└── README.md
```

## 五、快速开始

### 1. 环境准备

```powershell
# 已存在全局 venv（D:\python_demo\.venv），也可为本项目单独建
cd D:\python_demo\乡音守护者
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 配置环境变量

```powershell
copy .env.example .env
# 编辑 .env，填入模型路径 / API key / 数据库连接
```

### 3. 启动后端（FastAPI）

```powershell
uvicorn app.main:app --reload --port 8000
# 打开 http://127.0.0.1:8000/docs  查看接口
```

### 4. 启动前端 Demo（Streamlit）

```powershell
streamlit run app\web\app.py
# 自动打开 http://localhost:8501
```

### 5. 跑模块最小 demo

```powershell
python -m modules.asr      # ASR 占位 demo
python -m modules.tts     # TTS 占位 demo
python -m modules.llm      # LLM 占位 demo
python -m modules.rag      # RAG 占位 demo
```

## 六、阶段规划（详见 docs/milestone.md）

| 阶段 | 时间 | 目标 | 里程碑 |
|---|---|---|---|
| 0 | 2026.11 | 项目骨架 + Hello World | 目录可跑 |
| 1 | 2026.11–12 | 开题 + 萍乡话语料采录 | 语料 ≥ 50h |
| 2 | 2027.01–02 | ASR/TTS 基线 + 半监督标注 | ASR CER ≤ 25% |
| 3 | 2027.03–04 | LLM LoRA + RAG + 端侧 | 全链路 Demo |
| 4 | 2027.05 | 评测 + 论文 + 答辩 | 论文成稿 |

## 七、应用场景

1. **方言博物馆 · 数字讲解**：语音导览 + 俗语互动 + 方言地图
2. **社区/医院 · 适老导诊陪聊**：挂号指引 + 应急呼叫 + 陪老人聊天
3. **适老家庭 · AI 乡音陪聊**：方言问答 + 亲情语音 + 日常提醒
4. **学校/非遗 · 传承教学**：方言课伴学 + 歌谣童谣互动

## 八、下一步要装的模型清单

> 详见 `docs/milestone.md` 末尾「模型下载清单」。

- ASR：`faster-whisper large-v3`（约 3GB，先跑基线）
- LLM：`Qwen/Qwen2.5-7B-Instruct`（HuggingFace / ModelScope）
- TTS：先 Piper 中文预训练 voices，后续换 Coqui 微调
- Embedding：`BAAI/bge-small-zh-v1.5`（RAG 用）
