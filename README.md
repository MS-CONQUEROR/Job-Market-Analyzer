# 🤖 Job Market Analyzer
### An Agentic AI System powered by LangGraph + LangChain

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3--70B-orange.svg)

---

## 📌 Problem Statement

Fresh graduates and developers don't know which skills are actually in demand RIGHT NOW. They spend months learning the wrong things and miss opportunities. This AI agent solves that by autonomously researching the live job market and generating a personalized skill gap report.

---

## 🚀 What It Does

- Ask about job market trends → Get real-time insights
- Mention your skills → Get personalized skill gap report

---

## 🏗️ Architecture


User Input
     ↓
LangGraph ReAct Agent
     ↓
Agent Node (LLM thinks & decides)
     ↓ tool_calls
Tool Node (Tavily searches live web)
     ↓ results
Agent Node (LLM analyzes & answers)
     ↓
Keyword Detection
     ↓
Normal Answer OR Structured SkillGap Report


---

## ✨ Features

- 🔍 Real-time web search using Tavily
- 🧠 ReAct Pattern — Think → Search → Observe → Answer
- 📊 Structured Skill Gap Report (3-column output)
- 💬 Multi-turn conversation with full context memory
- 🎯 Smart routing — searches only when needed
- 🖥️ Clean Streamlit web interface

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| LangGraph | Agent workflow & orchestration |
| LangChain | LLM & tool integration |
| Groq (LLaMA 3.3 70B) | Ultra-fast LLM inference |
| Tavily | Real-time web search |
| Pydantic | Structured output validation |
| Streamlit | Web UI |
| Python | Core language |

---

## 🧠 Key LangGraph Concepts Used

- **StateGraph** — manages agent workflow and state
- **ReAct Pattern** — autonomous reasoning and acting
- **Conditional Edges** — smart routing between nodes
- **Loop Edges** — agent loops until satisfied
- **add_messages Reducer** — maintains conversation history
- **Structured Output** — Pydantic-based skill gap report

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/MS-CONQUEROR/Job-Market-Analyzer.git
cd Job-Market-Analyzer

# Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in root directory:

```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your free API keys:
- Groq: https://console.groq.com
- Tavily: https://tavily.com

---

## ▶️ Run Locally

```bash
streamlit run main.py
```

Open browser at `http://localhost:8501`

---

## 📊 Output Example


You: I know Python, LangChain, LangGraph

📊 SKILL GAP REPORT
═══════════════════════════════════════════
🎯 Market Demand    💪 Your Skills    ❌ Missing Skills
• Agentic AI        • Python          • MLOps
• RAG Pipelines     • LangChain       • FastAPI
• MLOps             • LangGraph       • Docker
• FastAPI                             • Cloud (AWS/GCP)
• Docker
═══════════════════════════════════════════


---

## 🗺️ Roadmap

- [x] ReAct agent with real-time web search
- [x] Structured skill gap report
- [x] Multi-turn conversation memory
- [x] Streamlit UI

---

## 👨‍💻 Author

**MS** | 3rd Year IT @SNIST
Aspiring Agentic AI Engineer

---

## 📄 License

MIT License — feel free to use and modify!
