# This file contains system prompts that define the behavior and personality of the agents.

def get_assistant_prompt(node_id, node_info):
    """
    Generate the assistant prompt for a specific conversation node.
    
    Args:
        node_id (str): The ID of the current conversation node
        node_info (dict): Information about the current node including its prompt
        
    Returns:
        str: The formatted assistant prompt
    """
    return f"""
You are a supportive counselor having a conversation with someone.
You are currently at the '{node_id}' stage of the conversation.

The base prompt template for this stage is: "{node_info['prompt']}"

Respond in a compassionate, thoughtful manner while following the general intent of the 
template above. Personalize your response based on the conversation history and current input.
Keep your response concise (3-4 sentences maximum).
"""

# Example usage:
# ASSISTANT_PROMPT = get_assistant_prompt(current_node_id, current_node_info)