from youtube_transcript_api import YouTubeTranscriptApi, YouTubeDataUnparsable
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

INDEX_DIR = Path('.indexes')
INDEX_DIR.mkdir(exist_ok=True)

def fetch_video_transcript(vid):
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(vid)
        transcript = "/n/n".join(chunk.text for chunk in transcript_list)
        return transcript
    except TranscriptsDisabled:
        raise RuntimeError("Transcripts are disabled for this video.")
    except Exception as e:
        raise RuntimeError(f"Could not fetch transcript: {e}")        
    
def chunk_text(text, chunk_size = 1000, chunk_overlap = 200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap= chunk_overlap
    )
    
    chunks = splitter.split_text(text)
    docs = [Document(page_content=c) for c in chunks]
    return docs


def create_faiss_index_from_docs(docs):
    embedding_model = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")
    vector_store = FAISS.from_documents(
        embedding=embedding_model,
        documents=docs
    )
    return vector_store


def save_index(vector_store, video_id):
    folder = INDEX_DIR/video_id
    # print(folder)
    folder.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(folder))
    return str(folder)
    
def load_index(video_id):
    folder = INDEX_DIR / video_id
    if not folder.exists():
        raise FileNotFoundError(f"Index for {video_id} not found.")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.load_local(str(folder), embeddings, allow_dangerous_deserialization= True)
    return vector_store

def augment_query_with_context(vector_store, query, k = 3):
    retriever = vector_store.as_retriever(search_type = "similarity",
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
    
    
def generate_answer_with_gemini(context_text, query):
    # Build the prompt exactly like notebook
    prompt_template = (
        "Use the following video transcript context to answer the question.\n\n"
        "CONTEXT:\n"
        f"{context_text}\n\n"
        "QUESTION:\n"
        f"{query}\n\n"
        "Answer in a clear and concise way."
    )

    model = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature = 0)

    # invoke() is the typical LangChain call for chat models
    response = model.invoke(prompt_template)

    # Extract final text
    return response.content


def convert_context_dict_to_text(context_dict):
    
    parts = []
    for key, value in context_dict.items():
        parts.append(f"[{key}]\n{value}\n")
    return "\n".join(parts)
