import pytest
import asyncio
from unittest.mock import patch, MagicMock

# Ensure we can import from parent directory
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import web_search_tool, weather_tool, database_tool
from agent import loop_agent, llm_agent

def test_web_search_tool_success():
    """Test web search tool with mocked successful request."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "query": {
            "search": [
                {"title": "Test Title", "snippet": "Test <span class=\"searchmatch\">Snippet</span>"}
            ]
        }
    }

    # Extract the original function from FunctionTool
    original_func = web_search_tool.func

    with patch('requests.get', return_value=mock_response):
        result = original_func("Test query")
        assert "Test Title" in result
        assert "Test Snippet" in result

def test_web_search_tool_error_handling():
    """Test web search tool handles errors gracefully."""
    import requests
    original_func = web_search_tool.func

    with patch('requests.get', side_effect=requests.RequestException("Mocked error")):
        result = original_func("Test query")
        assert "Error executing web search" in result
        assert "Mocked error" in result

def test_database_tool_select_query():
    """Test database tool select query."""
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_result = MagicMock()

    mock_engine.connect.return_value.__enter__.return_value = mock_connection
    mock_connection.execute.return_value = mock_result
    mock_result.fetchall.return_value = [("test1",), ("test2",)]

    original_func = database_tool.func

    with patch('tools.create_engine', return_value=mock_engine):
        with patch.dict(os.environ, {"DATABASE_URL": "mock://db"}):
            result = original_func("SELECT * FROM test_table")
            assert "Query returned 2 rows" in result

def test_database_tool_error_handling():
    """Test database tool handles errors gracefully."""
    from sqlalchemy.exc import SQLAlchemyError

    original_func = database_tool.func

    with patch('tools.create_engine', side_effect=SQLAlchemyError("Mocked DB error")):
        with patch.dict(os.environ, {"DATABASE_URL": "mock://db"}):
            result = original_func("SELECT * FROM test_table")
            assert "Error executing database query" in result

def test_agent_initialization():
    """Test that the agent was initialized correctly."""
    assert loop_agent.name == "main_loop_agent"
    assert loop_agent.max_iterations == 3
    assert len(loop_agent.sub_agents) == 1

    sub_agent = loop_agent.sub_agents[0]
    assert sub_agent.name == "worker_agent"
    assert sub_agent.model == "gemini-2.5-flash"
    assert len(sub_agent.tools) == 3
