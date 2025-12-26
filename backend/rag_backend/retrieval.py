from youtube_transcript_api import YouTubeTranscriptApi, YouTubeDataUnparsable
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
import requests
from bs4 import BeautifulSoup
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
    

def fetch_video_title(vid):
    VIDEO_ID = 'f8dhP521DHI'
    url = f"https://www.youtube.com/watch?v={vid}"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('meta', property='og:title')
    
    if not title_tag:
        return "Not found"
    return title_tag["content"]


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