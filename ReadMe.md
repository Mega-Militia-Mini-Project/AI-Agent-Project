# AI Agent Project

A sophisticated multi-agent AI orchestration system built with FastAPI and LangChain. This project provides intelligent conversational capabilities through single-agent and multi-agent modes, enabling dynamic AI interactions with support for multiple LLM providers.

## 📋 Project Overview

This project implements an advanced AI agent system that can:
- **Single Agent Mode**: Direct interaction with specified AI models with optional web search
- **Multi-Agent Sequential Mode**: Specialized agents work in sequence (Research → Analysis → Synthesis)
- **Multi-Agent Debate Mode**: Multiple perspectives (Optimist, Skeptic, Neutral) debate topics and reach consensus
- **Multiple LLM Support**: Seamless integration with Groq, OpenAI, and Google Gemini
- **Web Search Integration**: Real-time data collection via Tavily Search

## 🏗️ Architecture

### Core Components

#### `backend.py` - FastAPI Application
- **Purpose**: REST API server for AI agent interactions
- **Key Features**:
  - `/chat` endpoint that accepts queries and returns AI-generated responses
  - Pydantic request model validation
  - Support for 6+ LLM models
  - Dynamic routing between single-agent and multi-agent systems
  - Configurable agent modes (sequential/debate)
  
- **Supported Models**:
  - `llama3-70b-8192` (Groq)
  - `groq/compound-mini` (Groq)
  - `llama-3.3-70b-versatile` (Groq)
  - `gemini-2.0-flash` (Google Gemini)
  - `gemini-2.5-pro` (Google Gemini)
  - `openai/gpt-oss-120b` (OpenAI)

#### `multi_agent.py` - Multi-Agent Orchestration
Contains the `MultiAgentOrchestrator` class with specialized agents:

**Specialized Agents:**
1. **Research Agent** - Raw data collection
   - Extracts facts, statistics, and concrete information
   - Lists sources and URLs from web searches
   - Presents data in bullet points without interpretation
   
2. **Analyzer Agent** - Critical analysis
   - Identifies patterns and trends
   - Compares and contrasts data points
   - Evaluates credibility and biases
   - Generates deeper insights
   
3. **Writer Agent** - Synthesis and communication
   - Synthesizes research and analysis into coherent answers
   - Formats responses with proper structure
   - Provides actionable takeaways with citations
   
4. **Debate Agents** (in debate mode):
   - **Optimist** 🌟: Focuses on opportunities and positive aspects
   - **Skeptic** ⚠️: Focuses on risks and limitations
   - **Neutral** 📊: Objective evidence-based analysis
   - **Mediator** ⚖️: Synthesizes perspectives and builds consensus

**Processing Modes:**
- **Sequential Mode** (`process_query`): Research → Analyze → Write pipeline
- **Debate Mode** (`debate_mode`): Multiple perspectives debated, then mediated to consensus

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- API keys for desired LLM providers (Groq, OpenAI, Google Gemini)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AI-Agent-Project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

### Running the Server

Start the FastAPI server:
```bash
python backend.py
```

The server will run on `http://127.0.0.1:9999`

## 📡 API Endpoints

### POST `/chat`

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

**Request Parameters:**
- `model_name` (string, required): Name of the LLM model to use
- `model_provider` (string, required): Provider - "Groq", "OpenAI", or "Gemini"
- `system_prompt` (string, required): System prompt for the agent
- `messages` (list, required): List of user messages (query is first element)
- `allow_search` (boolean, required): Enable web search via Tavily
- `use_multi_agent` (boolean, optional): Enable multi-agent mode (default: false)
- `agent_mode` (string, optional): "sequential" or "debate" (default: "sequential")

**Response (Single Agent):**
```json
{
  "final_response": "The AI agent's response..."
}
```

**Response (Multi-Agent):**
```json
{
  "final_response": "The synthesized response...",
  "research_data": "Raw data collected...",
  "analysis": "Critical analysis...",
  "steps": [...]
}
```

## 📝 Example Usage

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

### Multi-Agent Sequential Mode
```python
response = requests.post(
    "http://127.0.0.1:9999/chat",
    json={
        "model_name": "llama3-70b-8192",
        "model_provider": "Groq",
        "system_prompt": "You are an expert.",
        "messages": ["Explain quantum computing"],
        "allow_search": True,
        "use_multi_agent": True,
        "agent_mode": "sequential"
    }
)
```

### Multi-Agent Debate Mode
```python
response = requests.post(
    "http://127.0.0.1:9999/chat",
    json={
        "model_name": "gemini-2.0-flash",
        "model_provider": "Gemini",
        "system_prompt": "You are analytical.",
        "messages": ["Should we invest in renewable energy?"],
        "allow_search": True,
        "use_multi_agent": True,
        "agent_mode": "debate"
    }
)
```

## 📚 Dependencies

| Package | Purpose |
|---------|---------|
| **FastAPI** | Web framework for building APIs |
| **Uvicorn** | ASGI server for FastAPI |
| **Pydantic** | Data validation and serialization |
| **LangChain** | Framework for building LLM applications |
| **LangChain-Groq** | Integration with Groq API |
| **LangChain-OpenAI** | Integration with OpenAI API |
| **LangChain-Google** | Integration with Google Generative AI |
| **LangChain-Tavily** | Web search integration |
| **LangGraph** | Graph-based agent orchestration |
| **Streamlit** | Optional UI framework |
| **python-dotenv** | Environment variable management |

## 🔄 Agent Processing Pipeline

### Sequential Mode
```
User Query
    ↓
Research Agent (collects raw data)
    ↓
Analyzer Agent (analyzes patterns)
    ↓
Writer Agent (synthesizes response)
    ↓
Final Response
```

### Debate Mode
```
User Query
    ↓
├─ Optimist Agent (positive perspective)
├─ Skeptic Agent (critical perspective)
└─ Neutral Agent (objective perspective)
    ↓
Mediator Agent (synthesizes consensus)
    ↓
Final Response
```

## 🎯 Key Features

- ✅ **Multiple LLM Support**: Seamless integration with Groq, OpenAI, and Google Gemini
- ✅ **Specialized Agent Roles**: Research, Analysis, Writing, and Debate agents
- ✅ **Web Search Integration**: Real-time information gathering via Tavily
- ✅ **Debate Mode**: Multiple perspectives with automated consensus building
- ✅ **REST API**: Simple HTTP interface for easy integration
- ✅ **Configurable Prompts**: Custom system prompts for different use cases
- ✅ **Error Handling**: Model validation and allowed models checking

## 🛠️ Development

### Project Structure
```
AI-Agent-Project/
├── backend.py              # FastAPI application
├── multi_agent.py          # Multi-agent orchestration logic
├── requirements.txt        # Python dependencies
└── ReadMe.md              # This file
```

### Adding New Models

To add a new LLM model:
1. Add the model name to `ALLOWED_MODEL_NAMES` in `backend.py`
2. Ensure the provider is supported in `_get_llm()` method

### Adding New Agents

To create new specialized agents in `multi_agent.py`:
1. Create a new agent method following the pattern of existing agents
2. Define its role and system prompt
3. Integrate it into the processing pipeline

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:9999/docs`
- **ReDoc**: `http://127.0.0.1:9999/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is provided as-is for educational and development purposes.

## 📬 Support

For questions or issues, please refer to the project documentation or contact the development team.