# AGENTS.md — Autonomous-Agent

## Project Purpose
This project implements a production-grade Autonomous AI Agent using Google Agent Development Kit (ADK).
It uses a LoopAgent architecture with a maximum of 3 iterations, equipped with Web Search, Weather,
and Database tools. It includes full error handling and Agent Observability via Cloud Trace.

---

## Tech Stack
- **Language:** Python 3.11+
- **Agent Framework:** Google ADK (Agent Development Kit)
- **Agent Type:** LoopAgent (max_iterations=3)
- **Tools:** Web Search Tool, Weather Tool, Database Tool
- **Observability:** Google Cloud Trace + ADK built-in tracing
- **Deployment:** Google Cloud Run

---

## Build Instructions

### Prerequisites
- Python 3.11+
- Google Cloud project with ADK, Cloud Trace, and Gemini API enabled
- Google Search API key (or SerpAPI key)
- OpenWeatherMap API key (or equivalent)
- PostgreSQL database for the Database Tool

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SEARCH_API_KEY=your_search_api_key
SEARCH_ENGINE_ID=your_search_engine_id
WEATHER_API_KEY=your_openweathermap_api_key
DATABASE_URL=postgresql://user:password@host:5432/agent_db
GOOGLE_CLOUD_PROJECT=your_gcp_project_id
```

### Run Locally
```bash
python main.py
```

### Run with Docker
```bash
docker build -t autonomous-agent .
docker run -p 8080:8080 autonomous-agent
```

---

## Coding Standards
- Follow PEP 8 style guide
- All tool functions must have complete docstrings describing inputs, outputs, and side effects
- Use type hints on all function signatures
- Each tool must handle its own exceptions and return structured error responses (never raise unhandled exceptions)
- Use `logging` module for all agent step logging
- Agent loop must respect `max_iterations=3` strictly
- All external API calls must have timeout settings and retry logic

---

## Project Structure
```
Autonomous-Agent/
├── main.py                 # Entry point; runs the LoopAgent
├── agent/
│   ├── loop_agent.py       # ADK LoopAgent configuration
│   └── prompts.py          # System and user prompt templates
├── tools/
│   ├── web_search_tool.py  # Google Search / SerpAPI integration
│   ├── weather_tool.py     # OpenWeatherMap integration
│   └── database_tool.py    # PostgreSQL query tool
├── observability/
│   └── tracer.py           # Cloud Trace + ADK observability setup
├── tests/
│   ├── test_web_search.py
│   ├── test_weather_tool.py
│   ├── test_database_tool.py
│   └── test_loop_agent.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## Testing Commands
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=term-missing

# Test individual tools
pytest tests/test_web_search.py -v
pytest tests/test_weather_tool.py -v
pytest tests/test_database_tool.py -v
```

---

## Deployment Expectations
- Deploy to **Google Cloud Run**
- Container must listen on port **8080**
- All secrets injected via Cloud Run environment variables or Secret Manager
- Agent must complete within **30 seconds** per request (Cloud Run timeout)
- Observability traces must appear in **Google Cloud Trace** within 60 seconds of execution
- Each tool call must be logged as a separate trace span

---

## Key Features to Implement
1. **LoopAgent** — ADK LoopAgent with `max_iterations=3`; stops early if goal is achieved
2. **Web Search Tool** — Search Google/SerpAPI; return top 3 results as structured data
3. **Weather Tool** — Fetch current weather and 3-day forecast for a given city
4. **Database Tool** — Execute read-only SQL queries against PostgreSQL; return results as JSON
5. **Error Handling** — Each tool returns `{"status": "error", "message": "..."}` on failure; agent handles gracefully
6. **Agent Observability** — Every agent step, tool call, and LLM call is traced; viewable in Cloud Trace console
