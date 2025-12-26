from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from database import engine, Base
import models 
from pathlib import Path
from rag_backend.bot_brain import workflow
from langchain_core.messages import HumanMessage
import uuid

from rag_backend.augmentation import (
    load_index,
    augment_query_with_context)

from rag_backend.retrieval import(
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
    save_message_pair, 
    get_chat_history, 
    get_all_videos, 
    save_video_history)



app = Flask(__name__)
CORS(app)
Base.metadata.create_all(bind=engine)


@app.route("/index", methods = ["POST"])
def index_video():
    data = request.get_json()
    video_id = data.get("video_id")
    
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
            
            return jsonify({
                "message": "Index created successfully.",
                "video_id": video_id,
                "chunks_created": len(docs),
                "index_path": path
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({
                "message": "Index Already Created ",
                "video_id": video_id,
                "index_path": str(folder)
            }), 200
    

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    video_id = data.get("video_id")
    question = data.get("message")

    if not video_id or not question:
        return jsonify({"error": "video_id and message are required"}), 400

    try:
        # 1. Use video_id as thread_id
        config = {
            "configurable": {
                "thread_id": video_id,
                "video_id": video_id # Pass this if retrieval node needs it
            }
        }

        # 2. Invoke the graph
        inputs = {"messages": [HumanMessage(content=question)]}
        result = workflow.invoke(inputs, config=config)
        
        # 3. Get the answer
        final_answer = result["messages"][-1].content
        
        save_message_pair(video_id, question, final_answer)
        
        return jsonify({"reply": final_answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/history/<video_id>", methods=["GET"])
def history(video_id):
    try:
        # Fetch history directly from LangGraph state
        history_data = get_chat_history(video_id)
        return jsonify({
            "video_id": video_id,
            "history": history_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/videos", methods=["GET"])
def videos_list():
    try:
        # Fetch list from LangGraph checkpoints
        video_list = get_all_videos()
        return jsonify({"videos": video_list}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)