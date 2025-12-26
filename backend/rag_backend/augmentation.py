from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from .retrieval import INDEX_DIR
load_dotenv()


def load_index(video_id):
    folder = INDEX_DIR / video_id
    if not folder.exists():
        raise FileNotFoundError(f"Index for {video_id} not found.")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.load_local(str(folder), embeddings, allow_dangerous_deserialization= True)
    return vector_store

def augment_query_with_context(vector_store, query, k = 3):
    retriever = vector_store.as_retriever(search_type = "mmr",
                                          search_kwargs = {"k": k})
    
    docs = retriever.invoke(query)
    context_dict = {
        f"chunk_{i+1}": doc.page_content
        for i, doc in enumerate(docs)
    }
    return {
        "query": query,
        "context": context_dict
    }
    