# 🤖 GenQuery: A Multi-Agent Conversational AI System

---

## Overview

**GenQuery** is a multi-agent conversational AI system that coordinates specialized AI agents to collaboratively process user queries and generate accurate, well-structured, and context-aware responses. Unlike traditional single-agent chatbots, GenQuery distributes reasoning across multiple agents — each with a defined role — to improve factual accuracy, reduce hallucinations, and deliver transparent, explainable outputs.

The system supports three operating modes:

- **Single Agent Mode** — Direct LLM interaction with optional web search
- **Sequential Multi-Agent Mode** — Research → Analysis → Writing pipeline
- **Debate Multi-Agent Mode** — Optimist / Skeptic / Neutral agents debate, with a Mediator synthesizing a consensus

---

## Architecture

```
User Query
    ↓
Streamlit Frontend
    ↓
FastAPI /chat Endpoint
    ↓
┌──────────────────────────────────────────────────┐
│                                                  │
│  Single Agent    Sequential Multi-Agent    Debate Multi-Agent  │
│      ↓                   ↓                         ↓          │
│  [Optional          Research Agent           3-Agent Debate   │
│  Web Search]             ↓                  (Optimist,        │
│      ↓             Analyzer Agent           Skeptic,          │
│   Response               ↓                  Neutral)          │
│                     Writer Agent                 ↓            │
│                          ↓                  Mediator          │
│                     3 Outputs               4 Outputs         │
└──────────────────────────────────────────────────┘
                          ↓
                  UI Result Display
```

---

## Agent Roles & Responsibilities

| Agent | Mode | Primary Task | Output |
|---|---|---|---|
| **Research Agent** | Sequential | Collects raw factual data via web search | Bullet list of facts & sources |
| **Analyzer Agent** | Sequential | Evaluates patterns, contradictions, reliability | Insight-driven analysis |
| **Writer Agent** | Sequential | Synthesizes final structured response | Well-formatted answer |
| **Optimist** | Debate | Highlights positive outcomes and evidence | Supportive perspective |
| **Skeptic** | Debate | Lists risks, flaws, and uncertainties | Critical view |
| **Neutral Analyst** | Debate | Evaluates data without bias | Balanced facts |
| **Mediator** | Debate | Combines all viewpoints into consensus | Final refined output |

---

## Project Structure

```
AI-Agent-Project/
├── backend.py          # FastAPI REST API — routing, validation, endpoint logic
├── multi_agent.py      # MultiAgentOrchestrator — all agent logic and pipelines
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .gitignore
└── ReadMe.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | FastAPI + Python |
| **AI Framework** | LangChain, LangGraph |
| **LLM Providers** | Groq, OpenAI, Google Gemini |
| **Web Search** | Tavily Search API |
| **Env Management** | python-dotenv |
| **Hosting** | Localhost / Cloud-compatible |

---

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for at least one LLM provider (Groq, OpenAI, or Google Gemini)
- A Tavily API key (required for web search features)

### 1. Clone the Repository

```bash
git clone https://github.com/Mega-Militia-Mini-Project/AI-Agent-Project.git
cd AI-Agent-Project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> **Note:** A Gemini API key (as `GEMINI_API_KEY`) is also required if using Google Gemini models.

### 5. Run the Backend Server

```bash
python backend.py
```

The server starts at: **`http://127.0.0.1:9999`**

- Swagger UI: `http://127.0.0.1:9999/docs`
- ReDoc: `http://127.0.0.1:9999/redoc`

---

##  API Reference

### `POST /chat`

Send a query to the AI agent system.

**Request Body:**

```json
{
  "model_name": "llama3-70b-8192",
  "model_provider": "Groq",
  "system_prompt": "You are a helpful assistant.",
  "messages": ["What is climate change?"],
  "allow_search": true,
  "use_multi_agent": false,
  "agent_mode": "sequential"
}
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `model_name` | string | ✅ | Name of the LLM model |
| `model_provider` | string | ✅ | `"Groq"`, `"OpenAI"`, or `"Gemini"` |
| `system_prompt` | string | ✅ | System-level instruction for the agent |
| `messages` | list[string] | ✅ | User query (first element used) |
| `allow_search` | boolean | ✅ | Enable Tavily web search |
| `use_multi_agent` | boolean | ❌ | Enable multi-agent mode (default: `false`) |
| `agent_mode` | string | ❌ | `"sequential"` or `"debate"` (default: `"sequential"`) |

**Supported Models:**

| Model Name | Provider |
|---|---|
| `llama3-70b-8192` | Groq |
| `groq/compound-mini` | Groq |
| `llama-3.3-70b-versatile` | Groq |
| `gemini-2.0-flash` | Google Gemini |
| `gemini-2.5-pro` | Google Gemini |
| `openai/gpt-oss-120b` | OpenAI |

**Response — Single Agent:**

```json
{
  "final_response": "The AI agent's response..."
}
```

**Response — Multi-Agent Sequential:**

```json
{
  "final_response": "The synthesized response...",
  "research_data": "Raw data collected...",
  "analysis": "Critical analysis...",
  "steps": [...]
}
```

**Response — Multi-Agent Debate:**

```json
{
  "final_response": "Mediator's consensus...",
  "optimist_response": "...",
  "skeptic_response": "...",
  "neutral_response": "..."
}
```

---

##  Usage Examples

### Single Agent Mode

```python
import requests

response = requests.post(
    "http://127.0.0.1:9999/chat",
    json={
        "model_name": "llama3-70b-8192",
        "model_provider": "Groq",
        "system_prompt": "You are a helpful assistant.",
        "messages": ["What is machine learning?"],
        "allow_search": True,
        "use_multi_agent": False
    }
)
print(response.json())
```

### Sequential Multi-Agent Mode

```python
response = requests.post(
    "http://127.0.0.1:9999/chat",
    json={
        "model_name": "llama-3.3-70b-versatile",
        "model_provider": "Groq",
        "system_prompt": "You are an expert researcher.",
        "messages": ["Explain the current state of quantum computing."],
        "allow_search": True,
        "use_multi_agent": True,
        "agent_mode": "sequential"
    }
)
print(response.json())
```

### Debate Multi-Agent Mode

```python
response = requests.post(
    "http://127.0.0.1:9999/chat",
    json={
        "model_name": "gemini-2.0-flash",
        "model_provider": "Gemini",
        "system_prompt": "You are an analytical AI.",
        "messages": ["Should we invest in renewable energy?"],
        "allow_search": True,
        "use_multi_agent": True,
        "agent_mode": "debate"
    }
)
print(response.json())
```

---

## Performance Analysis

| Category | Single-Agent | Multi-Agent | Improvement |
|---|---|---|---|
| Factual Accuracy | Medium | High | Improved grounding |
| Output Structure | Simple text | Well-structured | Better readability |
| Transparency | None | Full reasoning trace | User trust improved |
| Adaptability | 1 model | 3 LLM providers | Smart switching |
| Perspectives | Single view | Multi-view consensus | Avoids bias |

---

## Functional Testing Results

| Test Scenario | Status |
|---|---|
| Query without search enabled | ✅ Pass |
| Query with search enabled | ✅ Pass |
| Invalid model selected | ✅ Pass |
| Debate mode — multi-view + mediator | ✅ Pass |
| High-latency request | ✅ Pass |
| Missing API key | ✅ Pass |

---

##  Future Scope

- Integration with additional AI providers (Claude, DeepSeek, LLaMA variants)
- Domain-specific debate personas (legal expert, medical analyst, financial advisor)
- Long-term memory for cross-session context retention
- Browser extension and mobile app deployment
- Enhanced tool support (calculators, code runners, document readers)
- Analytics dashboard for agent performance monitoring
- Enterprise API with authentication and rate limiting
- Reinforcement learning for agent coordination optimization

---

## 📄 License

This project is submitted as a B.Tech dissertation at RCOEM, Nagpur. It is provided for educational and academic purposes.

---

## 📬 Contact

For questions or contributions, please open an issue on the (https://github.com/Mega-Militia-Mini-Project/AI-Agent-Project).
