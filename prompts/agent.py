from typing import Dict, Any

AGENT_PROMPT: Dict[str, str] = {
        "greeting": {
            "prompt": "Hello! I'm here to help you today. How are you feeling?",
            "next": "assessment"
        },
        "assessment": {
            "prompt": "I understand. Could you tell me more about what's going on?",
            "next": "reflection"
        },
        "reflection": {
            "prompt": "Thank you for sharing. It sounds like you're experiencing {summary}. Is that right?",
            "next": "exploration"
        },
        "exploration": {
            "prompt": "Let's explore this further. What do you think might be contributing to these feelings?",
            "next": "support"
        },
        "support": {
            "prompt": "Here are some strategies that might help: {strategies}. Would you like to discuss any of these in more detail?",
            "next": "closing"
        },
        "closing": {
            "prompt": "I hope our conversation has been helpful. Is there anything else you'd like to talk about?",
            "next": "assessment"
        }
    }