from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from pathlib import Path
from rag_backend.bot_brain import workflow
from langchain_core.messages import HumanMessage
import uuid
import uvicorn
from pydantic import BaseModel

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

from crud import (
    get_all_videos, 
    save_video_history)

app = FastAPI()

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
        result = workflow.invoke(inputs, config=config)
        
        # 3. Get the answer
        final_answer = result["messages"][-1].content
        
        return {"reply": final_answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/<video_id>")
async def history(video_id: str):
    try:
        # Fetch history directly from LangGraph state
        state = workflow.get_state(config={
            "configurable": {
                "thread_id": video_id
            }
        })
        
        history_data = state.values.get("messages", [])
        return {
            "video_id": video_id,
            "history": history_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/videos")
async def videos_list():
    try:
        # Fetch list from LangGraph checkpoints
        video_list = get_all_videos()
        return {
            "videos": video_list
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)