"""
ai_agent.py
Single-agent mode for GenQuery.

backend.py calls:
    get_response_from_ai_agent(llm_id, request.messages, allow_search, system_prompt, provider)
"""

import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


def _get_llm(llm_id: str, provider: str):
    """Return the LangChain chat model for the chosen provider."""
    provider = (provider or "").strip().lower()

    if provider == "groq":
        return ChatGroq(model=llm_id)
    if provider == "openai":
        return ChatOpenAI(model=llm_id)
    if provider == "gemini":
        return ChatGoogleGenerativeAI(model=llm_id, google_api_key=GEMINI_API_KEY)

    raise ValueError(f"Unsupported model provider: {provider!r}. Use Groq, OpenAI or Gemini.")


def get_response_from_ai_agent(
    llm_id: str,
    query: List[str],
    allow_search: bool,
    system_prompt: str,
    provider: str,
) -> str:
    """
    Run a single LangGraph/LangChain agent and return its final text answer.

    Args:
        llm_id:        model name, e.g. "llama-3.3-70b-versatile"
        query:         list of user messages (backend passes request.messages)
        allow_search:  if True, the agent can use Tavily web search
        system_prompt: system-level instruction for the agent
        provider:      "Groq" | "OpenAI" | "Gemini"
    """
    try:
        llm = _get_llm(llm_id, provider)
        tools = [TavilySearch(max_results=3)] if allow_search else []

        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt or "You are a helpful assistant.",
        )

        state = {"messages": query}
        response = agent.invoke(state)

        messages = response.get("messages", [])
        ai_messages = [m.content for m in messages if isinstance(m, AIMessage) and m.content]

        if not ai_messages:
            return "No response generated."

        final = ai_messages[-1]
        # Some providers (Gemini) can return a list of content blocks
        if isinstance(final, list):
            final = "".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in final
            )
        return final

    except Exception as e:  # keep the API alive, show the error in the UI
        return f"Error while running the agent: {e}"
