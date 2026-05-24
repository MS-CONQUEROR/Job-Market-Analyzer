from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import START,StateGraph,END,add_messages
from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage,ToolMessage
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

model = ChatGroq(model = "llama-3.3-70b-versatile",temperature = 0)

print(model.invoke('hi').content)

@tool
def search(query:str)->str:
    """it searches web for the role/market demand and skills required"""
    res = TavilySearch(max_results=2).invoke(query)
    return str(res)

tools = [search]

model_tools = model.bind_tools(tools)

class SkillGap(BaseModel):
    marketdemand:list[str]=Field(description="It shows the demand of that skill/role in market")
    skills:list[str]=Field(description="It stores the current skills of the user")
    mskills:list[str]=Field(description="It stores the missing skills need for that role")

class State(TypedDict):
    role:str
    messages:Annotated[list,add_messages]
    skill:list[str]
    report:SkillGap


def agent_node(state:State):
    system = SystemMessage("""You are a Job Market Analyzer assistant.
Only use the search tool when user asks about job market trends, 
required skills, or career advice.
For greetings → respond directly without searching.
""")
    print("Agent thinking....")
    message = [system] + state["messages"]
    response = model_tools.invoke(message)
    return {"messages": [response]}


def tool_node(state:State):
    print("Tool executing....")
    last_message = state["messages"][-1]
    results =[]
    for tool_call in last_message.tool_calls:
        if tool_call["name"] == "search":
            result = search.invoke(tool_call["args"])
        results.append(ToolMessage(
            content = result,
            tool_call_id = tool_call["id"]
        ))
    return {"messages":results}


def decide(state:State):
    res = state["messages"][-1]
    if res.tool_calls:
        return "tool"
    return "end"


graph = StateGraph(State)

graph.add_node("Agent",agent_node)
graph.add_node("Tool",tool_node)


graph.add_edge(START,"Agent")
graph.add_conditional_edges(
    "Agent",
    decide,
    {
        "tool": "Tool","end": END
    }
)

graph.add_edge("Tool","Agent")

app = graph.compile()


def should_generate_report(user_input: str) -> bool:
    keywords = ["i have", "i know", "my skills", "i can", "i learned"]
    return any(keyword in user_input.lower() for keyword in keywords)


history = []

structured_model = model.with_structured_output(SkillGap)

while True:
    user_input = input("\nYou: ")
    if user_input.lower()=="exit":
        break
    history.append(HumanMessage(user_input))
    response = app.invoke({"messages":history})
    if should_generate_report(user_input):
    
        report = structured_model.invoke(
            f"Based on this conversation generate skill gap report: {response['messages'][-1].content}"
        )
    
        print("\n📊 SKILL GAP REPORT:")
        print("═" * 35)
        print(f"\n🎯 Market Demand: {report.marketdemand}")
        print(f"\n💪 Your Skills:   {report.skills}")
        print(f"\n❌ Missing Skills: {report.mskills}")
        print("═" * 35)

    else:
        print(f"\n🤖 Agent: {response['messages'][-1].content}")
    history = response["messages"]
