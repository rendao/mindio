import os
from typing import List, Dict, Any, Optional, Union
from openai import OpenAI
from dotenv import load_dotenv

class ChatModel:
    """
    Unified AI model interface supporting chat functionality from multiple providers.
    Supported providers: openai, deepseek, qwen, silicoflow, ollama
    """
    
    def __init__(self, 
                 provider: str = "deepseek", 
                 api_key: Optional[str] = None,
                 api_base: Optional[str] = None,
                 chat_model: Optional[str] = None):
        """
        Initialize the AI model interface.
        
        Args:
            provider: Provider name ("openai", "deepseek", "qwen", "silicoflow", "ollama")
            api_key: API key (not needed for Ollama)
            api_base: API base URL (optional, defaults to standard endpoints)
            chat_model: Chat model name (optional, uses provider-specific defaults)
        """
        load_dotenv()

        self.provider = provider.lower()
        
        # Set API key
        self.api_key = api_key or os.getenv(f"{self.provider.upper()}_API_KEY")
        
        # Set default models and API base URLs
        if self.provider == "openai":
            self.chat_model = chat_model or "gpt-3.5-turbo"
            self.api_base = api_base or "https://api.openai.com/v1"
        elif self.provider == "deepseek":
            self.chat_model = chat_model or "deepseek-chat"
            self.api_base = api_base or "https://api.deepseek.com"
        elif self.provider == "qwen":
            self.chat_model = chat_model or "qwen-max"
            self.api_base = api_base or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        elif self.provider == "silicoflow":
            self.chat_model = chat_model or "glm-4"  # Assuming GLM-4 is default
            self.api_base = api_base or "https://api.silicoflow.com/v1"
        elif self.provider == "ollama":
            self.chat_model = chat_model or "llama3"
            self.api_base = api_base or "http://localhost:11434/api"
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        # Initialize OpenAI client for all providers
        # Special handling for Ollama which doesn't use API keys
        if self.provider == "ollama":
            self.client = OpenAI(base_url=self.api_base)
        else:
            self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)
    def generate_response(self, 
                          messages: List[Dict[str, str]], 
                          temperature: float = 0.7, 
                          max_tokens: Optional[int] = None,
                          model: Optional[str] = None) -> str:
        """
        Generate a response using a chat model.
        
        Args:
            messages: List of messages, each with "role" and "content"
            temperature: Temperature parameter controlling randomness
            max_tokens: Maximum number of tokens (optional)
            model: Model name (optional, overrides default)
        
        Returns:
            Generated response text
        """
        # Use specified model or default
        model_name = model or self.chat_model
        
        try:
            # Create params dict
            params = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
            }
            
            if max_tokens:
                params["max_tokens"] = max_tokens
                
            # Special handling for Ollama's different API endpoint
            if self.provider == "ollama":
                # For Ollama, we use the client but with custom endpoint
                params["stream"] = False
                response = self.client.post(
                    url="chat",
                    json=params
                )
                result = response.json()
                return result["message"]["content"]
            else:
                # For OpenAI-compatible APIs, use the standard client method
                response = self.client.chat.completions.create(**params)
                return response.choices[0].message.content
                
        except Exception as e:
            raise Exception(f"{self.provider.capitalize()} API error: {str(e)}")


# Usage examples:

# 1. Using DeepSeek (default)
# model = ChatModel(api_key="your-api-key")
# response = model.generate_response(messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"}
# ])

# 2. Using OpenAI
# model = ChatModel(provider="openai", api_key="your-api-key")
# response = model.generate_response(messages=[...])

# 3. Using local Ollama
# model = ChatModel(provider="ollama")
# response = model.generate_response(messages=[...], model="llama3")