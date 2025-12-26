from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from typing import TypedDict, Annotated
from dotenv import load_dotenv
load_dotenv()


model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", temperature = 0.1)

class LLMState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
def node_brain(state: LLMState):
    res = model.invoke(state["messages"])
    return {"messages": [res]}

graph = StateGraph(LLMState)
graph.add_node("bot", node_brain)

graph.add_node(START, "bot")
graph.add_node("bot", END)

conn = sqlite3.connect(database= "memory.db", check_same_thread=False)
checkPointer = SqliteSaver(conn = conn)

workflow = graph.compile(checkpointer=checkPointer)
