from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langgraph.graph import START, StateGraph, END, add_messages
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

# ============================================
# SETUP
# ============================================
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

@tool
def search(query: str) -> str:
    """it searches web for the role/market demand and skills required"""
    res = TavilySearch(max_results=2).invoke(query)
    return str(res)

tools = [search]
model_tools = model.bind_tools(tools)

# ============================================
# PYDANTIC
# ============================================
class SkillGap(BaseModel):
    marketdemand: list[str] = Field(description="Skills demanded in market")
    skills: list[str] = Field(description="User's current skills")
    mskills: list[str] = Field(description="Missing skills needed")

# ============================================
# STATE
# ============================================
class State(TypedDict):
    role: str
    messages: Annotated[list, add_messages]
    skill: list[str]
    report: SkillGap

# ============================================
# NODES
# ============================================
def agent_node(state: State):
    system = SystemMessage("""You are a Job Market Analyzer assistant.
Only use the search tool when user asks about job market trends, 
required skills, or career advice.
For greetings → respond directly without searching.
""")
    message = [system] + state["messages"]
    response = model_tools.invoke(message)
    return {"messages": [response]}

def tool_node(state: State):
    last_message = state["messages"][-1]
    results = []
    for tool_call in last_message.tool_calls:
        if tool_call["name"] == "search":
            result = search.invoke(tool_call["args"])
        results.append(ToolMessage(
            content=result,
            tool_call_id=tool_call["id"]
        ))
    return {"messages": results}

def decide(state: State):
    res = state["messages"][-1]
    if res.tool_calls:
        return "tool"
    return "end"

# ============================================
# GRAPH
# ============================================
graph = StateGraph(State)
graph.add_node("Agent", agent_node)
graph.add_node("Tool", tool_node)
graph.add_edge(START, "Agent")
graph.add_conditional_edges("Agent", decide, {"tool": "Tool", "end": END})
graph.add_edge("Tool", "Agent")
app = graph.compile()

structured_model = model.with_structured_output(SkillGap)

# ============================================
# KEYWORD DETECTION
# ============================================
def should_generate_report(user_input: str) -> bool:
    keywords = ["i have", "i know", "my skills", "i can", "i learned"]
    return any(keyword in user_input.lower() for keyword in keywords)

# ============================================
# STREAMLIT UI
# ============================================
st.set_page_config(page_title="Job Market Analyzer", page_icon="🤖", layout="wide")

st.title("🤖 Job Market Analyzer")
st.caption("Powered by LangGraph + LangChain + Groq + Tavily")

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Display chat history
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "report" in msg:
            report = msg["report"]
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("🎯 Market Demand")
                for skill in report.marketdemand:
                    st.write(f"• {skill}")
            with col2:
                st.subheader("💪 Your Skills")
                for skill in report.skills:
                    st.write(f"• {skill}")
            with col3:
                st.subheader("❌ Missing Skills")
                for skill in report.mskills:
                    st.write(f"• {skill}")

# Chat input
if user_input := st.chat_input("Ask about job market trends or mention your skills..."):

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.chat_messages.append({"role": "user", "content": user_input})

    # Process
    st.session_state.history.append(HumanMessage(user_input))

    with st.spinner("🧠 Agent thinking..."):
        response = app.invoke({"messages": st.session_state.history})

    answer = response["messages"][-1].content
    st.session_state.history = response["messages"]

    # Show response
    with st.chat_message("assistant"):
        if should_generate_report(user_input):
            with st.spinner("📊 Generating skill gap report..."):
                report = structured_model.invoke(
                    f"Based on this conversation generate skill gap report: {answer}"
                )
            st.write(answer)
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("🎯 Market Demand")
                for skill in report.marketdemand:
                    st.write(f"• {skill}")
            with col2:
                st.subheader("💪 Your Skills")
                for skill in report.skills:
                    st.write(f"• {skill}")
            with col3:
                st.subheader("❌ Missing Skills")
                for skill in report.mskills:
                    st.write(f"• {skill}")

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": answer,
                "report": report
            })
        else:
            st.write(answer)
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": answer
            })