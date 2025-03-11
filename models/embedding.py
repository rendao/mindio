import requests
import json
import os
from typing import List, Optional, Dict, Any, Union

class EmbeddingModel:
    """Model for generating text embeddings using various providers."""
    
    def __init__(self, provider: str = "ollama", model_name: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the embedding model.
        
        Args:
            provider: Provider name ("ollama", "openai", "silicoflow", or "qwen")
            model_name: Name of the embedding model (provider-specific)
            api_key: API key for cloud services (not needed for Ollama)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        
        # Set default models and endpoints based on provider
        if self.provider == "ollama":
            self.model = model_name or "nomic-embed-text"
            self.api_base = "http://localhost:11434/api"
        elif self.provider == "openai":
            self.model = model_name or "text-embedding-3-small"
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.api_base = "https://api.openai.com/v1"
        elif self.provider == "silicoflow":
            self.model = model_name or "bge-large-zh"
            self.api_key = api_key or os.getenv("SILICOFLOW_API_KEY")
            self.api_base = "https://api.silicoflow.com/v1"
        elif self.provider == "qwen":
            self.model = model_name or "text-embedding-v3"
            self.api_key = api_key or os.getenv("QWEN_API_KEY")
            self.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if self.provider == "ollama":
            return self._get_ollama_embedding(text)
        elif self.provider == "openai":
            return self._get_openai_embedding(text)
        elif self.provider == "silicoflow":
            return self._get_silicoflow_embedding(text)
        elif self.provider == "qwen":
            return self._get_qwen_embedding(text)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _get_ollama_embedding(self, text: str) -> List[float]:
        """Get embedding from Ollama local API."""
        response = requests.post(
            f"{self.api_base}/embeddings",
            json={"model": self.model, "prompt": text}
        )
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.text}")
        result = response.json()
        return result["embedding"]
    
    def _get_openai_embedding(self, text: str) -> List[float]:
        """Get embedding from OpenAI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{self.api_base}/embeddings",
            headers=headers,
            json={
                "input": text,
                "model": self.model
            }
        )
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.text}")
        result = response.json()
        return result["data"][0]["embedding"]
    
    def _get_silicoflow_embedding(self, text: str) -> List[float]:
        """Get embedding from SilicoFlow API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{self.api_base}/embeddings",
            headers=headers,
            json={
                "input": text,
                "model": self.model
            }
        )
        if response.status_code != 200:
            raise Exception(f"SilicoFlow API error: {response.text}")
        result = response.json()
        return result["data"][0]["embedding"]
    
    def _get_qwen_embedding(self, text: str) -> List[float]:
        """Get embedding from Alibaba Cloud Qwen API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{self.api_base}/embeddings",
            headers=headers,
            json={
                "model": self.model,
                "input": text
            }
        )
        if response.status_code != 200:
            raise Exception(f"Qwen API error: {response.text}")
        result = response.json()
        return result["data"][0]["embedding"]


# Usage examples:
# 1. Use Ollama locally (default)
# embedding_model = EmbeddingModel()

# 2. Use OpenAI embeddings
# embedding_model = EmbeddingModel(provider="openai", api_key="your-api-key-here")

# 3. Use SilicoFlow
# embedding_model = EmbeddingModel(provider="silicoflow", model_name="bge-large-zh", api_key="your-api-key")

# 4. Use Qwen
# embedding_model = EmbeddingModel(provider="qwen", api_key="your-api-key")