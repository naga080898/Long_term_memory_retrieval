from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def call_openai_chat_with_messages(
    messages,
    tools=None,
    tool_choice=None,
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1024,
    api_key=None
):
    """
    Calls OpenAI ChatCompletion endpoint using a full `messages` list.

    Args:
        messages (list): List of messages in OpenAI chat format.
        tools (list): Optional list of tools (functions, code interpreter etc.).
        tool_choice (str|dict): Optional tool selection ('auto' or specific function).
        model (str): Model to use.
        temperature (float): Sampling temperature.
        max_tokens (int): Max output tokens.
        api_key (str): OpenAI API key (optional; defaults to env var OPENAI_API_KEY).
    
    Returns:
        dict: Full API response.
    """
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if tools:
        payload["tools"] = tools
    if tool_choice:
        payload["tool_choice"] = tool_choice

    response = client.chat.completions.create(**payload)
    return response
