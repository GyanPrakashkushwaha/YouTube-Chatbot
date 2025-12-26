from rag_utils import load_index

video_id = "f8dhP521DHI"  # same ID you indexed

print("Loading FAISS index...")
vs = load_index(video_id)

print("Index loaded!")

# create a retriever
retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 3})

query = "what is divide and conquer?"
print("\nQuery:", query)

docs = retriever.invoke(query)
print("\nRetrieved chunks:", len(docs))
print("\nPreview of first chunk:\n", docs[0].page_content[:200])
