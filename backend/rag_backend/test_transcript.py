from rag_utils import fetch_video_transcript, chunk_text


video_id = "f8dhP521DHI"  # or any video with captions ON
text = fetch_video_transcript(video_id)
print("Transcript length:", len(text if text else ""))

docs = chunk_text(text)
print("Chunks:", len(docs))
print("First chunk preview:", docs[0].page_content[:200])