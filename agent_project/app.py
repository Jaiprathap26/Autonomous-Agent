import asyncio
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from agent import loop_agent
from google.adk.runners import Runner

# Initialize Streamlit page
st.set_page_config(page_title="ADK Autonomous Agent", page_icon="🤖")
st.title("Google ADK Autonomous Agent")
st.markdown("This agent uses a `LoopAgent` to iteratively solve tasks using Web Search, Weather, and Database tools.")

# Validate API Key
if not os.environ.get("GOOGLE_API_KEY") and not os.environ.get("GEMINI_API_KEY"):
    st.warning("⚠️ Warning: GOOGLE_API_KEY or GEMINI_API_KEY is not set. The agent will not be able to run.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to run the agent async
async def run_agent(prompt: str):
    runner = Runner(agent=loop_agent)

    # Store events to display
    events = []

    try:
        async for event in runner.run(prompt):
            events.append(event)

            # Display agent reasoning or tool calls
            if hasattr(event, "content") and event.content:
                parts = event.content.parts if hasattr(event.content, "parts") else []
                text_content = "".join([part.text for part in parts if hasattr(part, "text") and part.text])

                if text_content:
                    with st.chat_message("assistant"):
                        st.markdown(text_content)
                        st.session_state.messages.append({"role": "assistant", "content": text_content})

            # Log tool calls in an expander for better visibility
            if hasattr(event, "get_function_calls"):
                function_calls = event.get_function_calls()
                if function_calls:
                    for call in function_calls:
                        with st.expander(f"🛠️ Tool Call: {call.name}"):
                            st.json(call.args)

            if hasattr(event, "get_function_responses"):
                function_responses = event.get_function_responses()
                if function_responses:
                    for response in function_responses:
                        with st.expander(f"✅ Tool Response: {response.name}"):
                            st.json(response.response)

    except Exception as e:
        with st.chat_message("error"):
            error_msg = f"An error occurred: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "error", "content": error_msg})

# Accept user input
if prompt := st.chat_input("Enter a task for the agent..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run the agent and display the results
    with st.spinner("Agent is thinking..."):
        asyncio.run(run_agent(prompt))
