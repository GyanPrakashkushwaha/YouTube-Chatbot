from rag_utils import (
    fetch_video_transcript,
    chunk_text,
    create_faiss_index_from_docs,
    save_index
)

video_id = "f8dhP521DHI"  # example YouTube ID (your notebook used this)

print("Fetching transcript...")
text = fetch_video_transcript(video_id)

print("Chunking...")
docs = chunk_text(text)

print("Creating FAISS index...")
vector_store = create_faiss_index_from_docs(docs)

print("Saving index to disk...")
folder = save_index(vector_store, video_id)

print("Index saved at:", folder)
