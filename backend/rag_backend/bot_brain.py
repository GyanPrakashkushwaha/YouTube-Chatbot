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


# StateSnapshot(values={'messages': [HumanMessage(content='hii', additional_kwargs={}, response_metadata={}, id='b1075579-aea1-4fd9-8e0f-56b7b8d92499'), AIMessage(content='Hi there! How can I help you today? 😊', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--79b6434c-a2c5-47a0-aa7f-f8060a090656-0', usage_metadata={'input_tokens': 2, 'output_tokens': 11, 'total_tokens': 13, 'input_token_details': {'cache_read': 0}}), HumanMessage(content='helo', additional_kwargs={}, response_metadata={}, id='125ae76c-19b9-4a4a-a350-9ea179361d59'), AIMessage(content='Hello! How can I assist you?', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--7b07a056-f594-4ad7-8704-f54af2464e52-0', usage_metadata={'input_tokens': 17, 'output_tokens': 8, 'total_tokens': 25, 'input_token_details': {'cache_read': 0}}), HumanMessage(content='my name is gyan prakash ', additional_kwargs={}, response_metadata={}, id='2485e6c2-b558-4a21-bb2e-ab01ab8072fb'), AIMessage(content="Hello Gyan Prakash! It's nice to meet you. How can I help you today?", additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--46e84360-bfb5-4bb3-91a1-90358cb0f1df-0', usage_metadata={'input_tokens': 35, 'output_tokens': 19, 'total_tokens': 54, 'input_token_details': {'cache_read': 0}}), HumanMessage(content="what's 2+3", additional_kwargs={}, response_metadata={}, id='3af4fe72-4110-4c17-a84e-89a244c98508'), AIMessage(content='2 + 3 = 5', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--78165b4e-18a0-4a3e-aab9-85695186d47e-0', usage_metadata={'input_tokens': 63, 'output_tokens': 7, 'total_tokens': 70, 'input_token_details': {'cache_read': 0}}), HumanMessage(content="what's my name", additional_kwargs={}, response_metadata={}, id='445189e5-3d5b-4604-b512-adb132109e4d'), AIMessage(content='Your name is Gyan Prakash.', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--cde64e1e-325f-44bc-aac6-b58215d14c61-0', usage_metadata={'input_tokens': 77, 'output_tokens': 6, 'total_tokens': 83, 'input_token_details': {'cache_read': 0}})]},
              
              
# next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0e2056-1f0a-6107-800d-c09fbd7e8edc'}}, metadata={'source': 'loop', 'step': 13, 'parents': {}}, created_at='2025-12-26T02:48:39.435891+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0e2056-1690-6592-800c-902910128c86'}}, tasks=(), interrupts=()),
