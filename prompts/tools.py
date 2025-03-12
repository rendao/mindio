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