from rag_utils import load_index, augment_query_with_context

video_id = "f8dhP521DHI"  # same ID you indexed

print("Loading FAISS index...")
vs = load_index(video_id)

query = "what is divide and conquer?"
print("\nQuery:", query)

prompt = augment_query_with_context(vs, query)
print(prompt)