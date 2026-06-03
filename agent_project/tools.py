import logging
import os
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from google.adk.tools import FunctionTool

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def web_search(query: str) -> str:
    """Uses a mocked search API to answer queries."""
    logger.info(f"Executing web_search for query: {query}")
    try:
        # We'll use Wikipedia API as a simple mock search API,
        # or just return a dummy response if it fails.
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&utf8=&format=json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "query" in data and "search" in data["query"] and data["query"]["search"]:
            first_result = data["query"]["search"][0]
            # remove html tags from snippet
            import re
            snippet = re.sub(r'<[^>]+>', '', first_result["snippet"])
            return f"Search result for '{query}': {first_result['title']} - {snippet}"
        else:
            return f"No results found for '{query}'."

    except requests.RequestException as e:
        logger.error(f"Web search failed: {e}")
        return f"Error executing web search: {e}"
    except Exception as e:
        logger.error(f"Unexpected error in web search: {e}")
        return f"Unexpected error in web search: {e}"

def get_weather(location: str) -> str:
    """Fetches current weather for a given location."""
    logger.info(f"Executing get_weather for location: {location}")
    try:
        # Using Open-Meteo geocoding and weather API (no key required)
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geocode_response = requests.get(geocode_url, timeout=5)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if "results" not in geocode_data or not geocode_data["results"]:
            return f"Could not find location: {location}"

        lat = geocode_data["results"][0]["latitude"]
        lon = geocode_data["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url, timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if "current_weather" in weather_data:
            temp = weather_data["current_weather"]["temperature"]
            return f"Current temperature in {location} is {temp}°C."
        else:
            return f"Weather data not available for {location}."

    except requests.RequestException as e:
        logger.error(f"Weather fetch failed: {e}")
        return f"Error executing weather fetch: {e}"
    except Exception as e:
        logger.error(f"Unexpected error in weather fetch: {e}")
        return f"Unexpected error in weather fetch: {e}"

def execute_database_query(query: str) -> str:
    """Reads/writes to PostgreSQL via SQLAlchemy."""
    logger.info(f"Executing database query: {query}")
    try:
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            return "Error: DATABASE_URL environment variable is not set."

        engine = create_engine(database_url)
        with engine.connect() as connection:
            result = connection.execute(text(query))

            # If it's a SELECT query, return the fetched rows
            if query.strip().upper().startswith("SELECT"):
                rows = result.fetchall()
                # Convert rows to string representation
                return f"Query returned {len(rows)} rows: {str(rows)}"
            else:
                # For INSERT/UPDATE/DELETE, commit and return success
                connection.commit()
                return "Query executed successfully."

    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return f"Error executing database query: {e}"
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        return f"Unexpected database error: {e}"

# Wrap tools with FunctionTool
web_search_tool = FunctionTool(web_search)
weather_tool = FunctionTool(get_weather)
database_tool = FunctionTool(execute_database_query)
