from typing import TypedDict, Annotated, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables import RunnableConfig
import sqlite3
import os

# Import your existing RAG tools
from .augmentation import load_index, augment_query_with_context
from .generation import convert_context_dict_to_text

# Define the State
class BotState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    context: str # We will store the retrieved context here

# Initialize Model
model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", temperature=0.1)

# --- Define Nodes ---

def retrieve_node(state: BotState, config: RunnableConfig):
    """
    Retrieves relevant context based on the user's last message.
    """
    # 1. Get the video_id from the runtime configuration
    video_id = config.get("configurable", {}).get("video_id")
    if not video_id:
        raise ValueError("video_id is missing from configuration")

    # 2. Get the latest user question
    last_message = state["messages"][-1].content

    # 3. Load index and retrieve (using your existing functions)
    # Note: We are reusing your logic from augmentation.py
    vector_store = load_index(video_id) 
    aug_data = augment_query_with_context(vector_store, last_message)
    
    # 4. Format context
    context_text = convert_context_dict_to_text(aug_data["context"])
    
    return {"context": context_text}

def generate_node(state: BotState):
    """
    Generates an answer using the retrieved context and history.
    """
    context = state["context"]
    messages = state["messages"]
    
    # Construct a prompt that includes context + chat history
    # We can pass the messages directly to the model, but we need to inject the context.
    # A simple system message or prepended context works well.
    
    system_instruction = f"""Use the following video context to answer the question.
    
    CONTEXT:
    {context}
    
    Answer clearly and concisely.
    If question asked out of topic answer it as well."""
    
    # Create a new list of messages for the model call: System Instruction + Chat History
    prompt_messages = [HumanMessage(content=system_instruction)] + messages
    
    response = model.invoke(prompt_messages)
    
    return {"messages": [response]}

# --- Build Graph ---

builder = StateGraph(BotState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)

# Flow: Start -> Retrieve -> Generate -> End
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

# --- Persistence ---

# Ensure the database exists or is created
db_path = "memory.db"
conn = sqlite3.connect(database="memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

workflow = builder.compile(checkpointer=checkpointer)

# --- NEW HELPER FUNCTIONS ---

def get_chat_history(video_id: str):
    """
    Fetches the message history for a specific video (thread).
    """
    config = {"configurable": {"thread_id": video_id}}
    # get_state returns a StateSnapshot
    current_state = workflow.get_state(config)
    
    # The 'messages' key holds the list of BaseMessages
    messages = current_state.values.get("messages", [])
    
    # Convert to the format your frontend expects (dictionaries)
    formatted_history = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "model"
        formatted_history.append({
            "role": role,
            "text": msg.content # Ensure this matches frontend key (e.g., 'text' or 'content')
        })
        
    return formatted_history

def get_all_videos():
    """
    Lists all unique video IDs (thread_ids) present in the storage.
    """
    # checkpointer.list(None) returns an iterator of all checkpoints
    # We iterate through them to find unique thread_ids
    unique_video_ids = set()
    
    # Note: list(None) lists all checkpoints. 
    # For a large production app, you'd want a more optimized SQL query,
    # but for a local app, this works fine.
    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config["configurable"]["thread_id"]
        unique_video_ids.add(thread_id)
        
    # Format for frontend. 
    # Note: We only have the ID here. If you need titles, 
    # we'd need to store them in the state or metadata previously.
    return [{"video_id": vid, "title": f"Video {vid}"} for vid in unique_video_ids]