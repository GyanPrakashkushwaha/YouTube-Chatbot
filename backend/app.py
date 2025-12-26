from flask import Flask, request, jsonify
from flask_cors import CORS
import random
# from rag_backend.rag_utils import (
#     fetch_video_transcript,
#     fetch_video_title,
#     chunk_text,
#     create_faiss_index_from_docs,
#     save_index,
#     load_index,
#     augment_query_with_context,
#     convert_context_dict_to_text,
#     generate_answer_with_gemini,
#     INDEX_DIR)

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


from database import engine, Base
import models 
from crud import (save_message_pair, 
                  get_chat_history, 
                  get_all_videos, 
                  save_video_history)
from pathlib import Path



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

    if not video_id:
        return jsonify({"error": "video_id is required"}), 400
    if not question:
        return jsonify({"error": "message is required"}), 400

    try:
        vector_store = load_index(video_id)
        aug = augment_query_with_context(vector_store, question, k=3)
        context_text = convert_context_dict_to_text(aug["context"])

        final_answer = generate_answer_with_gemini(context_text, question)
        save_message_pair(video_id, question, final_answer)
        
        return jsonify({
            "reply": final_answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/history/<video_id>", methods = ["GET"])
def history(video_id):
    try:
        history = get_chat_history(video_id)
        return jsonify({
            "video_id": video_id,
            "history": history
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route("/videos", methods = ["GET"])
def videos_list():
    try:
        video_history = get_all_videos()
        return jsonify({
            "videos": video_history
        }), 200
        
    except Exception as e:
        return jsonify({"error": e}), 500

if __name__ == "__main__":
    app.run(debug=True)