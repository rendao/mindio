from typing import Dict, Any

# Define available knowledge bases
AVAILABLE_KNOWLEDGE_BASES: Dict[str, Dict[str, Any]] = {
    "general_mental_health": {
        "description": "General information about mental health concepts and terminology",
        "path": "knowledge/data/general_mental_health.json",
        "type": "embedding"
    },
    "symptom_patterns": {
        "description": "Information about common symptom patterns and their significance",
        "path": "knowledge/data/symptom_patterns.json",
        "type": "embedding"
    },
    "causes_factors": {
        "description": "Knowledge about common causes and contributing factors to mental health issues",
        "path": "knowledge/data/causes_factors.json",
        "type": "embedding"
    },
    "self_assessment": {
        "description": "Guidelines and frameworks for self-assessment",
        "path": "knowledge/data/self_assessment.json",
        "type": "embedding"
    },
    "coping_techniques": {
        "description": "Evidence-based coping techniques for various mental health challenges",
        "path": "knowledge/data/coping_techniques.json", 
        "type": "embedding"
    },
    "self_help_resources": {
        "description": "Curated list of self-help resources and references",
        "path": "knowledge/data/self_help_resources.json",
        "type": "embedding"
    }
}

def get_knowledge_base(kb_name: str) -> Dict[str, Any]:
    """
    Retrieves a specified knowledge base by name.
    
    Args:
        kb_name: The name of the knowledge base to retrieve
        
    Returns:
        The knowledge base configuration
        
    Raises:
        KeyError: If the knowledge base does not exist
    """
    if kb_name not in AVAILABLE_KNOWLEDGE_BASES:
        raise KeyError(f"Knowledge base '{kb_name}' not found")
    return AVAILABLE_KNOWLEDGE_BASES[kb_name]