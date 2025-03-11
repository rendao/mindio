import os
from typing import List, Dict, Any
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class KnowledgeBase:
    """Knowledge base for storing and retrieving information."""
    
    def __init__(self, embedding_model=None):
        """
        Initialize the knowledge base.
        
        Args:
            embedding_model: Model to generate embeddings for text
        """
        self.documents = []
        self.embeddings = []
        self.embedding_model = embedding_model
    
    def add_document(self, document: Dict[str, Any]):
        """
        Add a document to the knowledge base without generating embeddings immediately.
        
        Args:
            document: Document with at least 'content' and optional 'metadata'
        """
        if 'content' not in document:
            raise ValueError("Document must contain 'content' field")
        
        self.documents.append(document)
        # Note: We don't generate embeddings here, we'll do it when needed
    
    def load_documents_from_json(self, filepath: str):
        """Load documents from a JSON file without generating embeddings immediately."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            docs = json.load(f)
        
        for doc in docs:
            self.add_document(doc)
    
    def _ensure_embeddings(self):
        """Generate embeddings for all documents if they don't exist yet."""
        if not self.embedding_model:
            return False
            
        # If embeddings haven't been generated yet or don't match document count
        if len(self.embeddings) != len(self.documents):
            self.embeddings = []
            for doc in self.documents:
                embedding = self.embedding_model.get_embedding(doc['content'])
                self.embeddings.append(embedding)
            return True
        return False
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant documents based on a query.
        """
        if not self.embedding_model:
            # Fall back to keyword search if no embeddings
            return self._keyword_search(query, top_k)
        
        # Ensure all documents have embeddings
        self._ensure_embeddings()
        
        # Generate embedding for query
        query_embedding = self.embedding_model.get_embedding(query)
        
        # Calculate similarity scores
        similarities = []
        for doc_embedding in self.embeddings:
            similarity = self._calculate_similarity(query_embedding, doc_embedding)
            similarities.append(similarity)
        
        # Get indices of top k documents
        indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:top_k]
        
        # Return top k documents
        return [self.documents[i] for i in indices]
    
    def _calculate_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        # Simple cosine similarity implementation
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0
    
    def _keyword_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Simple keyword search fallback."""
        query_terms = set(query.lower().split())
        
        # Calculate relevance scores based on term overlap
        scores = []
        for doc in self.documents:
            doc_terms = set(doc['content'].lower().split())
            overlap = len(query_terms.intersection(doc_terms))
            scores.append(overlap)
        
        # Get indices of top k documents
        indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        # Return top k documents
        return [self.documents[i] for i in indices]