import os
import json
import datetime
from typing import List, Dict, Any, Optional

def save_conversation(conversation: List[Dict], filename: str = None, metadata: Dict = None) -> str:
    """Save conversation to JSON file, returns filename"""
    if not filename:
        os.makedirs("history/data", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"history/data/conversation_{timestamp}.json"
    
    data = {"conversation": conversation}
    if metadata:
        data["metadata"] = metadata
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def load_conversation(filename: str) -> List[Dict]:
    """Load conversation from JSON file, returns conversation history"""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("conversation", [])

def list_conversations(directory: str = "history/data") -> List[str]:
    """
    List saved conversation files
    
    Args:
        directory: Directory containing conversation files
        
    Returns:
        List of filenames
    """
    if not os.path.exists(directory):
        return []
    
    files = [f for f in os.listdir(directory) if f.startswith("conversation_") and f.endswith(".json")]
    # Sort files by modification time (newest first)
    files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
    
    return files

def get_conversation_by_index(index: int, directory: str = "history/data") -> Optional[List[Dict]]:
    """
    Get conversation by its index in the list of saved conversations
    
    Args:
        index: 1-based index of the conversation file
        directory: Directory containing conversation files
        
    Returns:
        Conversation history list or None if index is invalid
    """
    files = list_conversations(directory)
    
    # Check if index is valid (1-based)
    try:
        # Convert to int if string was passed
        index = int(index)
        
        if 1 <= index <= len(files):
            filename = files[index-1]
            full_path = os.path.join(directory, filename)
            try:
                return load_conversation(full_path)
            except Exception:
                return None
    except (ValueError, TypeError):
        return None
    
    return None