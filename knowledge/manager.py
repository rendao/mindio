from typing import Dict, Any, List, Optional
from models.embedding import EmbeddingModel
from knowledge.base import KnowledgeBase
from prompts.knowledge import AVAILABLE_KNOWLEDGE_BASES, get_knowledge_base
import os
import json

class KnowledgeManager:
    """Manages multiple knowledge bases and provides unified search interface"""
    
    def __init__(self):
        """Initialize the knowledge manager with embedding model"""
        self.embedding_model = EmbeddingModel(provider="qwen")
        self.knowledge_bases = {}
        self.general_kb = KnowledgeBase(self.embedding_model)
        
        # Load all available knowledge bases
        self._load_all_knowledge_bases()
    
    def _load_all_knowledge_bases(self):
        """Load all knowledge bases defined in prompts/knowledge.py"""
        for kb_name, kb_info in AVAILABLE_KNOWLEDGE_BASES.items():
            try:
                kb = KnowledgeBase(self.embedding_model)
                path = kb_info.get('path', '')
                
                # Make sure path exists and is valid
                if path and os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # Process data based on its structure
                    # This depends on how your knowledge files are structured
                    if isinstance(data, dict):
                        for key, items in data.items():
                            if isinstance(items, list):
                                for item in items:
                                    if isinstance(item, dict):
                                        content = json.dumps(item)
                                        kb.add_document({
                                            "content": content,
                                            "metadata": {
                                                "source": kb_name,
                                                "category": key
                                            }
                                        })
                    
                    # Store the knowledge base
                    self.knowledge_bases[kb_name] = kb
                    
            except Exception as e:
                print(f"Error loading knowledge base {kb_name}: {e}")
    
    def add_document(self, document: Dict[str, Any]):
        """Add a document to the general knowledge base"""
        self.general_kb.add_document(document)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search across all knowledge bases"""
        results = []
        
        # Search general knowledge base
        general_results = self.general_kb.search(query, top_k=top_k)
        results.extend(general_results)
        
        # Search all specific knowledge bases
        for kb_name, kb in self.knowledge_bases.items():
            kb_results = kb.search(query, top_k=1)  # Limit results from each KB
            results.extend(kb_results)
        
        # Sort by relevance and limit to top_k
        results = sorted(results, key=lambda x: x.get('score', 0), reverse=True)[:top_k]
        
        return results
    
    def search_in_bases(self, query: str, kb_names: List[str], top_k: int = 3) -> List[Dict[str, Any]]:
        """Search only in specified knowledge bases"""
        results = []
        
        # Always search in general knowledge base
        general_results = self.general_kb.search(query, top_k=1)
        results.extend(general_results)
        
        # Search in specified knowledge bases
        for kb_name in kb_names:
            if kb_name in self.knowledge_bases:
                kb_results = self.knowledge_bases[kb_name].search(query, top_k=1)
                results.extend(kb_results)
        
        # Sort by relevance and limit to top_k
        results = sorted(results, key=lambda x: x.get('score', 0), reverse=True)[:top_k]
        
        return results