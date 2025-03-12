from typing import Dict, Any, List
from prompts.tools import AVAILABLE_TOOLS
from prompts.knowledge import AVAILABLE_KNOWLEDGE_BASES

# define the agent prompts
AGENT_PROMPT: Dict[str, Dict[str, Any]] = {
    "greeting": {
        "prompt": "Hello! I'm here to help you today. How are you feeling?",
        "next": "assessment",
        "tools": [],
        "knowledge": []
    },
    "assessment": {
        "prompt": "I understand. Could you tell me more about what's going on?",
        "next": "reflection",
        "tools": [],
        "knowledge": ["general_mental_health"]
    },
    "reflection": {
        "prompt": "Thank you for sharing. It sounds like you're experiencing {summary}. Is that right?",
        "next": "exploration",
        "tools": ["symptom_search"],
        "knowledge": ["general_mental_health", "symptom_patterns"]
    },
    "exploration": {
        "prompt": "Let's explore this further. What do you think might be contributing to these feelings?",
        "next": "support",
        "tools": ["symptom_search", "assessment_tool"],
        "knowledge": ["causes_factors", "self_assessment"]
    },
    "support": {
        "prompt": "Here are some strategies that might help: {strategies}. Would you like to discuss any of these in more detail?",
        "next": "closing",
        "tools": ["coping_strategies"],
        "knowledge": ["coping_techniques", "self_help_resources"]
    },
    "closing": {
        "prompt": "I hope our conversation has been helpful. Is there anything else you'd like to talk about?",
        "next": "assessment",
        "tools": [],
        "knowledge": ["general_mental_health"]
    },
    "tool_use": {
        "prompt": "I'll use a specialized tool to help address your concerns more effectively.",
        "next": "dynamic",
        "tools": list(AVAILABLE_TOOLS.keys()),
        "knowledge": list(AVAILABLE_KNOWLEDGE_BASES.keys())
    }
}