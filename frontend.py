"""
frontend.py
Streamlit UI for GenQuery: A Multi-Agent Conversational AI System.

Run the backend first:   python backend.py
Then run this UI:        streamlit run frontend.py
"""

import requests
import streamlit as st

API_URL = "http://127.0.0.1:9999/chat"

MODELS = {
    "Groq": ["llama3-70b-8192", "groq/compound-mini", "llama-3.3-70b-versatile"],
    "Gemini": ["gemini-2.0-flash", "gemini-2.5-pro"],
    "OpenAI": ["openai/gpt-oss-120b"],
}

st.set_page_config(page_title="GenQuery", page_icon="🤖", layout="wide")

# ---------- Session state ----------
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"query", "mode", "result"}

# ---------- Sidebar: settings ----------
with st.sidebar:
    st.header("⚙️ Settings")

    provider = st.selectbox("Model provider", list(MODELS.keys()))
    model_name = st.selectbox("Model", MODELS[provider])

    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful assistant.",
        height=100,
    )

    allow_search = st.toggle("🌐 Enable web search (Tavily)", value=True)

    st.divider()
    mode = st.radio(
        "Operating mode",
        ["Single Agent", "Sequential Multi-Agent", "Debate Multi-Agent"],
        help=(
            "Single: one LLM (optional search)\n\n"
            "Sequential: Research → Analyzer → Writer\n\n"
            "Debate: Optimist / Skeptic / Neutral + Mediator"
        ),
    )

    if st.button("🗑️ Clear history", use_container_width=True):
        st.session_state.history = []
        st.rerun()

use_multi_agent = mode != "Single Agent"
agent_mode = "debate" if mode == "Debate Multi-Agent" else "sequential"


# ---------- Helpers ----------
def call_backend(query: str) -> dict:
    payload = {
        "model_name": model_name,
        "model_provider": provider,
        "system_prompt": system_prompt,
        "messages": [query],
        "allow_search": allow_search,
        "use_multi_agent": use_multi_agent,
        "agent_mode": agent_mode,
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=300)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot reach the backend. Start it with `python backend.py`."}
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Try a simpler query or a faster model."}
    except Exception as e:
        return {"error": f"Request failed: {e}"}


def render_steps(steps):
    if not steps:
        return
    with st.expander("🧭 Agent reasoning trace", expanded=False):
        for s in steps:
            st.markdown(f"- {s.get('message', '')}")


def render_result(result: dict, mode_label: str):
    if "error" in result:
        st.error(result["error"])
        return

    # Final answer
    st.markdown("### ✅ Final Response")
    st.markdown(result.get("final_response", "_No response returned._"))

    # Sequential extras
    if mode_label == "Sequential Multi-Agent":
        with st.expander("🔍 Research Agent output (raw data)"):
            st.markdown(result.get("research_data", "_n/a_"))
        with st.expander("🧠 Analyzer Agent output"):
            st.markdown(result.get("analysis", "_n/a_"))

    # Debate extras
    if mode_label == "Debate Multi-Agent":
        debate = result.get("debate_responses")
        if debate:
            cols = st.columns(len(debate))
            for col, d in zip(cols, debate):
                with col:
                    st.markdown(f"#### {d.get('emoji', '')} {d.get('agent', '')}")
                    st.markdown(d.get("response", ""))
        else:  # fallback to the README-style keys
            for label, key in [
                ("🌟 Optimist", "optimist_response"),
                ("⚠️ Skeptic", "skeptic_response"),
                ("📊 Neutral", "neutral_response"),
            ]:
                if key in result:
                    with st.expander(label):
                        st.markdown(result[key])

    render_steps(result.get("steps"))

    meta = result.get("metadata")
    if meta:
        st.caption(" • ".join(f"{k}: {v}" for k, v in meta.items()))


# ---------- Main page ----------
st.title("🤖 GenQuery")
st.caption("A Multi-Agent Conversational AI System")

# Past conversations
for item in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(item["query"])
    with st.chat_message("assistant"):
        st.caption(f"Mode: {item['mode']}")
        render_result(item["result"], item["mode"])

# New query
query = st.chat_input("Ask GenQuery anything...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        spinner_text = {
            "Single Agent": "Thinking...",
            "Sequential Multi-Agent": "Research → Analysis → Writing in progress...",
            "Debate Multi-Agent": "Optimist, Skeptic and Neutral are debating...",
        }[mode]
        with st.spinner(spinner_text):
            result = call_backend(query)

        st.caption(f"Mode: {mode}")
        render_result(result, mode)

    st.session_state.history.append({"query": query, "mode": mode, "result": result})
