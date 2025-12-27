from typing import TypedDict, Annotated, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnableConfig
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

async def retrieve_node(state: BotState, config: RunnableConfig):
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
    # Note: We are reusing the logic from augmentation.py
    vector_store = load_index(video_id) 
    aug_data = augment_query_with_context(vector_store, last_message)
    
    # 4. Format context
    context_text = convert_context_dict_to_text(aug_data["context"])
    
    return {"context": context_text}


async def generate_node(state: BotState):
    """
    Generates an answer using the retrieved context and history.
    """
    context = state["context"]
    messages = state["messages"]

    system_instruction = f"""Use the following video context to answer the question.
    
    CONTEXT:
    {context}
    
    Answer clearly and concisely.
    If question asked out of topic answer it as well."""
    
    # Create a new list of messages for the model call: System Instruction + Chat History
    prompt_messages = [HumanMessage(content=system_instruction)] + messages
    
    response = await model.ainvoke(prompt_messages)
    
    return {"messages": [response]}

# --- Build Graph ---

builder = StateGraph(BotState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)

# Flow: Start -> Retrieve -> Generate -> End
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

# --- Globals (Initialized in app.py) ---
workflow = None
checkpointer = None

async def ai_only_stream(video_id: str, query: str):
    """
    Generator that yields tokens from the LLM response.
    """
    config = {
        "configurable": {
            "thread_id": video_id,
            "video_id": video_id
        }
    }
    inputs = {
        "messages": [HumanMessage(content=query)]
    }
    async for event in workflow.astream_events(inputs, config=config, version="v1"):
            # We filter for the specific event where the LLM emits a token
            if event["event"] == "on_chat_model_stream":
                # Get the chunk data
                chunk = event["data"]["chunk"]
                if chunk.content:
                    # Yield just the text content (token)
                    yield chunk.content
                    

async def get_chat_history(video_id: str):
    """
    Fetches the message history for a specific video (thread).
    """
    if workflow is None:
        return []
    config = {"configurable": {"thread_id": video_id}}
    # get_state returns a StateSnapshot
    current_state = await workflow.aget_state(config)
    
    # The 'messages' key holds the list of BaseMessages
    messages = current_state.values.get("messages", [])
    
    # Convert to the format your frontend expects (dictionaries)
    formatted_history = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "model"
        formatted_history.append({
            "role": role,
            "text": msg.content
        })
        
    return formatted_history

async def get_all_videos():
    """
    Async function to fetch all videos from the checkpointer.
    """
    unique_video_ids = set()
    async for checkpoint in checkpointer.alist(None):
        thread_id = checkpoint.config["configurable"]["thread_id"]
        unique_video_ids.add(thread_id)
    return [{"video_id": vid, "title": f"Video {vid}"} for vid in unique_video_ids]