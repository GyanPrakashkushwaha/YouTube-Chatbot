from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
import models
from pathlib import Path
from rag_backend.bot_brain import workflow, ai_only_stream, get_chat_history, get_all_videos
from langchain_core.messages import HumanMessage
import uuid
import uvicorn
from pydantic import BaseModel
from crud import save_video_history
import rag_backend.bot_brain as bot_brain


from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from rag_backend.augmentation import (
    load_index,
    augment_query_with_context)

from rag_backend.retrieval import (
    fetch_video_transcript,
    fetch_video_title,
    chunk_text,
    create_faiss_index_from_docs,
    save_index,
    INDEX_DIR)

from rag_backend.generation import (
    convert_context_dict_to_text,
    generate_answer_with_gemini)



@asynccontextmanager
async def lifespan(app: FastAPI): # The connection closes automatically when the app stops
    # Initialization
    async with AsyncSqliteSaver.from_conn_string("memory.db") as saver:
        # Injection of checkpointer and workflow.
        bot_brain.checkpointer = saver
        bot_brain.workflow = bot_brain.builder.compile(checkpointer = saver)
        yield
        
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

# Request Bodies
class IndexRequest(BaseModel):
    video_id: str

class ChatRequest(BaseModel):
    video_id: str
    query : str

@app.post("/index")
async def index_video(request: IndexRequest):
    video_id = request.video_id
    
    if not video_id:
        return jsonify({"error": "video_id is required"}), 400
    
    folder = INDEX_DIR/video_id
    if not folder.exists():
        try:
            transcript = fetch_video_transcript(video_id)
            title = fetch_video_title(video_id)
            docs = chunk_text(transcript)
            vector_store = create_faiss_index_from_docs(docs)
            path = save_index(vector_store, video_id)
            save_video_history(video_id, title)
            
            return {
                "message": "Index created successfully.",
                "video_id": video_id,
                "chunks_created": len(docs),
                "index_path": path
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return {
            "message": "Index Already Created ",
            "video_id": video_id,
            "index_path": str(folder)
            }
    

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Standard non-streaming chat endpoint.
    """
    video_id = request.video_id
    question = request.query

    try:
        # 1. Use video_id as thread_id
        config = {
            "configurable": {
                "thread_id": video_id,
                "video_id": video_id 
            }
        }
        # 2. Invoke the graph
        inputs = {"messages": [HumanMessage(content=question)]}
        if bot_brain.workflow is None:
            raise HTTPException(status_code=500, detail="Workflow not initialized")
        
        result = await bot_brain.workflow.ainvoke(inputs, config=config)
        
        # 3. Get the answer
        final_answer = result["messages"][-1].content
        
        return {"reply": final_answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint using Server-Sent Events (SSE).
    """
    video_id = request.video_id
    question = request.query
    
    async def event_stream():
        try:
            async for token in ai_only_stream(video_id, question):
                yield f"data: {token}\n\n"
            yield "data: [DONE]"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/history/{video_id}")
async def history(video_id: str):
    try:
        # Fetch history directly from LangGraph state
        state = get_chat_history(video_id)
        
        return {
            "video_id": video_id,
            "history": state
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/videos")
async def videos_list():
    try:
        # Fetch list from LangGraph checkpoints
        video_list = await get_all_videos()
        return {
            "videos": video_list
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)