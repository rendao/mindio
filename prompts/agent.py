from typing import Dict, Any, List

# Define available tools
AVAILABLE_TOOLS = {
    "symptom_search": {
        "name": "symptom_search",
        "description": "Search for information about mental health symptoms in the knowledge database",
        "parameters": {
            "symptom": {
                "type": "string",
                "description": "The mental health symptom to search for"
            }
        }
    },
    "assessment_tool": {
        "name": "assessment_tool",
        "description": "Provide a standardized psychological assessment based on specific criteria",
        "parameters": {
            "assessment_type": {
                "type": "string",
                "description": "Type of assessment to run (anxiety, depression, stress)",
                "enum": ["anxiety", "depression", "stress"]
            }
        }
    },
    "coping_strategies": {
        "name": "coping_strategies",
        "description": "Suggest evidence-based coping strategies for specific challenges",
        "parameters": {
            "challenge": {
                "type": "string",
                "description": "The type of challenge the user is facing"
            }
        }
    }
}
# define the agent prompts
AGENT_PROMPT: Dict[str, Dict[str, Any]] = {
    "greeting": {
        "prompt": "Hello! I'm here to help you today. How are you feeling?",
        "next": "assessment",
        "tools": []  # No tools needed for greeting
    },
    "assessment": {
        "prompt": "I understand. Could you tell me more about what's going on?",
        "next": "reflection",
        "tools": []  # Basic assessment doesn't use tools yet
    },
    "reflection": {
        "prompt": "Thank you for sharing. It sounds like you're experiencing {summary}. Is that right?",
        "next": "exploration",
        "tools": ["symptom_search"]  # Can use symptom search to better understand user's experience
    },
    "exploration": {
        "prompt": "Let's explore this further. What do you think might be contributing to these feelings?",
        "next": "support",
        "tools": ["symptom_search", "assessment_tool"]  # Can use assessment or symptom search during exploration
    },
    "support": {
        "prompt": "Here are some strategies that might help: {strategies}. Would you like to discuss any of these in more detail?",
        "next": "closing",
        "tools": ["coping_strategies"]  # Can suggest coping strategies in support phase
    },
    "closing": {
        "prompt": "I hope our conversation has been helpful. Is there anything else you'd like to talk about?",
        "next": "assessment",
        "tools": []  # No tools needed for closing
    },
    "tool_use": {
        "prompt": "I'll use a specialized tool to help address your concerns more effectively.",
        "next": "dynamic",  # Next node will be determined based on the tool result
        "tools": list(AVAILABLE_TOOLS.keys())  # All tools are available in tool_use mode
    }
}