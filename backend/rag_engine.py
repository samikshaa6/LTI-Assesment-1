try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Warning: sentence_transformers not installed. Using Mock Embeddings.")
    SentenceTransformer = None

from pypdf import PdfReader
import os
import math
from typing import List, Dict

# Simple In-Memory Vector Store
VECTOR_STORE = []

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
    return dot_product / (magnitude_v1 * magnitude_v2)

class RAGEngine:
    def __init__(self, api_key=None):
        try:
            # Load local model (CPU friendly)
            if SentenceTransformer:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            else:
                 self.model = None
        except Exception as e:
            print(f"Failed to load sentence-transformers: {e}")
            self.model = None

    def parse_pdf(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error parse PDF: {e}")
            return ""

    def chunk_text(self, text: str, chunk_size=1000, overlap=200) -> List[str]:
        chunks = []
        start = 0
        if not text: return []
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def get_embedding(self, text: str) -> List[float]:
        if not self.model:
            # Fallback mock if model failed to load
            return [0.0] * 384
        try:
            return self.model.encode(text).tolist()
        except Exception as e:
            print(f"Embedding error: {e}")
            return []

    def index_document(self, text: str, metadata: Dict):
        global VECTOR_STORE
        VECTOR_STORE = []
        
        chunks = self.chunk_text(text)
        for i, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)
            if embedding:
                VECTOR_STORE.append({
                    "id": f"chunk_{i}",
                    "text": chunk,
                    "embedding": embedding,
                    "metadata": metadata
                })

    def retrieve_context(self, query: str, n_results=3) -> List[str]:
        # Embed query
        try:
             query_embedding = self.get_embedding(query)
             if not query_embedding: return []
        except:
            return []

        # Cosine Search
        scored_chunks = []
        for item in VECTOR_STORE:
            score = cosine_similarity(query_embedding, item["embedding"])
            scored_chunks.append((score, item["text"]))
        
        # Sort and return top N
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:n_results]]
