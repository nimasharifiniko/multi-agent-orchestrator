# 🤖 Autonomous Multi-Agent Orchestration System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![LLM](https://img.shields.io/badge/LLM-Ollama%20%2F%20Qwen2.5--Coder-orange.svg)](https://ollama.ai/)
[![Architecture](https://img.shields.io/badge/Architecture-State--Driven%20Multi--Agent-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

An end-to-end, state-driven multi-agent orchestration system that automatically researches, drafts, evaluates, and iteratively revises technical reports using local Large Language Models (LLMs).

Developed by **[Nima Sharifi Niko](https://github.com/nimasharifiniko)**.

---

## 💡 Overview & Business Value

In traditional AI workflows, single-prompt execution often fails to deliver publication-grade technical documents. This system solves that problem by implementing a **peer-review feedback loop** between specialized autonomous agents:

1. **Researcher Agent**: Gathers context and structures key factual findings.
2. **Writer Agent**: Transforms raw findings into a cohesive, structured markdown draft.
3. **Reviewer Agent**: Evaluates draft quality against actionable metrics (scoring 1–10).
4. **Orchestrator Core**: Manages shared workflow state, enforces quality thresholds, and routes feedback back to the Writer for iterative revisions when necessary.

---

## 🏗️ System Architecture

```text
                               ┌─────────────────────────┐
                               │   User Input (Topic)    │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │    Central State Core   │
                               │     (WorkflowState)     │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │    Researcher Agent     │
                               └────────────┬────────────┘
                                            │ Extracted Findings
                                            ▼
                               ┌─────────────────────────┐
                        ┌─────►│      Writer Agent       │
                        │      └────────────┬────────────┘
                        │                   │ Draft Report
                        │ Feedback          ▼
                        │ Loop ┌─────────────────────────┐
                        │      │     Reviewer Agent      │
                        │      └────────────┬────────────┘
                        │                   │ Quality Evaluation
                        │                   ▼
                        │          ┌─────────────────┐
                        └──────────┤ Quality >= Pass?│
                        (Needs     └────────┬────────┘
                        Revision)           │ Yes (Approved)
                                            ▼
                               ┌─────────────────────────┐
                               │    Final Report Output  │
                               └─────────────────────────┘
✨ Key Features
State-Driven Orchestration: Centralized WorkflowState tracking agent execution, cycle counts, and outputs.
Autonomous Feedback Loop: Automatic re-drafting mechanism triggered whenever the Reviewer score falls below the customizable quality threshold.
Bounded Iteration Guard: Prevents infinite execution loops by setting strict iteration bounds (MAX_ITERATIONS).
Structured Data Validation: Enforced strict input/output schemas using Pydantic data models.
100% Local & Free Execution: Powered by Ollama (qwen2.5-coder:7b) for privacy and zero API costs.
Interactive Purple Dashboard: Custom Streamlit UI featuring live pipeline visualization, parameter tuning, and Markdown export.
🛠️ Tech Stack
Language: Python 3.10+
AI Engine / LLM: Ollama (qwen2.5-coder:7b) via OpenAI-compatible API
Data Modeling: Pydantic v2
Dashboard / UI: Streamlit (Custom CSS styling)
Environment Management: python-dotenv
Terminal Diagnostics: Rich CLI logging
📁 Project Structure
text

multi-agent-orchestrator/
│
├── src/
│   ├── __init__.py
│   ├── models.py          # Pydantic data models & state schema
│   ├── llm_client.py      # Centralized OpenAI-compatible LLM wrapper
│   ├── researcher.py      # Research extraction agent
│   ├── writer.py          # Drafting & revision agent
│   ├── reviewer.py        # Quality evaluation agent
│   └── orchestrator.py    # Main workflow state engine & loop controller
│
├── tests/
│   ├── test_workflow.py   # Multi-topic pipeline test suite
│   └── test_feedback_loop.py # Loop verification test
│
├── app.py                 # CLI entry point
├── streamlit_app.py       # Interactive Streamlit UI dashboard
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # Documentation
🚀 Quick Start Guide
1. Prerequisites
Installed Python 3.10+
Installed & running Ollama (https://ollama.ai)
Pull the recommended model:

Bash

ollama pull qwen2.5-coder:7b
2. Installation
Clone repository:

Bash

git clone https://github.com/nimasharifiniko/multi-agent-orchestrator.git
cd multi-agent-orchestrator
Create and activate virtual environment:

Bash

# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1
Install dependencies:

Bash

pip install -r requirements.txt
3. Environment Setup
Create .env file from template:

Bash

LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=qwen2.5-coder:7b
💻 How to Run
Option A: Interactive Streamlit Dashboard (Recommended)
Bash

streamlit run streamlit_app.py
Open http://localhost:8501 in your browser.

Option B: Terminal CLI Mode
Bash

python app.py
Option C: Run Test Suite
Bash

python -m tests.test_workflow
👨‍💻 Author
Nima Sharifi Niko

GitHub: @nimasharifiniko
Role: Python Developer · AI Engineer
📜 License
Distributed under the MIT License. See LICENSE for more information.