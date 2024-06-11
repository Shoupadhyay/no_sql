import chromadb
from sentence_transformers import SentenceTransformer

class ChromaDBIntegration:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name="langchain-collection")
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def add_to_collection(self, text: str):
        vector = self.model.encode(text)
        self.collection.add(text, vector)

    def query_collection(self, query: str):
        query_vector = self.model.encode(query)
        results = self.collection.query(query_vector, top_k=1)
        return results