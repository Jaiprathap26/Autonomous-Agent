import os
import logging
from google.adk.agents import LoopAgent, LlmAgent
from tools import web_search_tool, weather_tool, database_tool
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_telemetry():
    """Sets up OpenTelemetry with Google Cloud Trace exporter."""
    # Don't fail if we can't set up the exporter (e.g. no GCP credentials)
    try:
        project_id = os.environ.get("OTEL_EXPORTER_GCP_PROJECT")

        provider = TracerProvider()
        trace.set_tracer_provider(provider)

        if project_id:
            # Requires Google Cloud credentials to be available
            exporter = CloudTraceSpanExporter(project_id=project_id)
            processor = BatchSpanProcessor(exporter)
            provider.add_span_processor(processor)
            logger.info("OpenTelemetry configured with Google Cloud Trace")
        else:
            logger.info("OTEL_EXPORTER_GCP_PROJECT not set, skipping Cloud Trace export")

    except Exception as e:
        logger.error(f"Failed to set up telemetry: {e}")

# Call setup_telemetry when the module is imported
setup_telemetry()

# Create the LLM agent with tools
llm_agent = LlmAgent(
    name="worker_agent",
    model="gemini-2.5-flash",
    instruction="""You are a helpful assistant. Use your tools to answer user queries:
    1. Web Search: For general knowledge or up-to-date information.
    2. Weather: To find the current weather for a location.
    3. Database: To read from or write to the database using SQL queries.
    Make sure to provide clear and concise answers.
    """,
    tools=[web_search_tool, weather_tool, database_tool]
)

# Create the LoopAgent that orchestrates the workflow
loop_agent = LoopAgent(
    name="main_loop_agent",
    sub_agents=[llm_agent],
    max_iterations=3
)
