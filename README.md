# Autonomous AI Agent (Google ADK)

This project implements a production-grade Autonomous AI Agent using the Google Agent Development Kit (ADK). It orchestrates an AI workflow to iteratively solve tasks using various integrated tools. The project includes full error handling, Agent Observability via Cloud Trace, and a user-friendly Streamlit web interface.

## Tech Stack
- **Language:** Python 3.12
- **Agent Framework:** Google ADK (Agent Development Kit)
- **Architecture:** Workflow with iterative execution
- **UI:** Streamlit
- **Tools:** Web Search, Weather, Database (PostgreSQL)
- **Observability:** Google Cloud Trace + ADK built-in tracing
- **LLM Model:** Gemini (gemini-2.5-flash)

## Features
1. **Interactive Workflow:** Orchestrates the problem-solving loop, executing tools as needed.
2. **Web Search Tool:** Searches Wikipedia (as a proxy/mock) for general knowledge.
3. **Weather Tool:** Fetches current weather data for locations using Open-Meteo.
4. **Database Tool:** Executes read-only SQL queries against a PostgreSQL database via SQLAlchemy.
5. **Observability:** Telemetry integrated with Google Cloud Trace to trace execution spans and tool calls.
6. **Streamlit UI:** A clean interface to chat with the agent and see real-time tool executions.

## Setup & Build Instructions

### Prerequisites
- Python 3.12+
- Gemini API key
- PostgreSQL database
- (Optional) Google Cloud project with Cloud Trace enabled

### Installation
1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with the following variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   DATABASE_URL=postgresql://user:password@host:5432/agent_db
   # Optional: For Google Cloud Trace
   OTEL_EXPORTER_GCP_PROJECT=your_gcp_project_id
   GOOGLE_APPLICATION_CREDENTIALS=path_to_your_service_account.json
   ```

### Running Locally
Run the Streamlit application:
```bash
streamlit run app.py
```
The app will be available at `http://localhost:8501`.

### Running with Docker
You can also run the agent using Docker:
```bash
docker build -t autonomous-agent .
docker run -p 8501:8501 --env-file .env autonomous-agent
```

## Testing
The project uses `pytest` for testing. Run the tests with:
```bash
pytest agent_project/tests/ -v
```
