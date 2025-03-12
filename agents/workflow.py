from typing import Dict, Any, Callable
from models.chat import ChatModel
from utils.logger import log
from prompts.system import SYSTEM_PROMPT
from prompts.agent import AGENT_PROMPT
from prompts.agent import AVAILABLE_TOOLS
from prompts.assistent import get_assistant_prompt
from knowledge.base import KnowledgeBase
from models.embedding import EmbeddingModel
import json

class Workflow:
    def __init__(self):
        # Initialize the workflow nodes
        self.nodes = AGENT_PROMPT
        
        # Initialize AI client
        self.client = ChatModel(provider="qwen")
        
        # Conversation history to provide context for LLM
        self.conversation_history = []
        
        # Initialize knowledge base
        try:
            embedding_model = EmbeddingModel(provider="qwen")
            self.knowledge_base = KnowledgeBase(embedding_model)
            # 
            # Load knowledge from files
            # use relative path
            self.knowledge_base.load_documents_from_json("data/knowledge.json")
            self.knowledge_base.add_document({
                "content": "When there is a possibility of self harm or injury to others, emergency calls should be made immediately：119。",
                "metadata": {"source": "emergency-resources", "category": "resources"}
            })
        except Exception as e:
            print(f"Error initializing knowledge base: {e}")
            self.knowledge_base = None
    
    def select_node_with_llm(self, current_node_id, user_input):
        """Use LLM to intelligently select the next appropriate node based on user input"""
        
        # Create a prompt for the LLM to decide the next node
        system_prompt = f"""
        Based on the user's input, select the most appropriate next conversation stage from the following options:
        
        {', '.join(self.nodes.keys())}
        
        Current stage: {current_node_id}
        User input: "{user_input}"
        
        If the user's request would benefit from using specialized tools or assessments, select "tool_use".
        Otherwise, choose the most appropriate conversation stage.
        
        Respond with only the name of the selected stage, nothing else.
        """
        
        # Add the current conversation context
        user_prompt = f"Current node: {current_node_id}\nUser message: {user_input}\nWhich node should I go to next?"
        log('INFO', f"[current node]: {user_prompt}")
        # Call the LLM
        try:
            response = self.client.generate_response(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2  # Low temperature for more deterministic responses
            )
            
            next_node = response.strip().lower()
            
            # Validate the node exists
            log('INFO', f"[next node]: {next_node}")
            if next_node in self.nodes:
                return next_node
            else:
                # Fallback to default logic if LLM returns invalid node
                return self.nodes[current_node_id]["next"]
                
        except Exception as e:
            # Fallback to default logic if LLM call fails
            print(f"Error calling LLM: {e}")
            return self.nodes[current_node_id]["next"]
    
    def generate_response_with_llm(self, node_id, user_input):
        """Use LLM to generate a dynamic response based on the node and user input"""
        
        # Add current exchange to conversation history
        if user_input:
            self.conversation_history.append({"role": "user", "content": user_input})
        
        # Create system prompt based on current node
        node_info = self.nodes[node_id]
        system_prompt = get_assistant_prompt(node_id, node_info)
        
        # Retrieve relevant knowledge if available
        knowledge_context = ""
        if user_input and self.knowledge_base:
            try:
                relevant_docs = self.knowledge_base.search(user_input, top_k=2)
                if relevant_docs:
                    knowledge_context = "\n\nRelevant information from knowledge base(your answer must prioritize the use of knowledge):\n"
                    for i, doc in enumerate(relevant_docs):
                        knowledge_context += f"{i+1}. {doc['content']}\n"
                    log('INFO', f"Knowledge context: {knowledge_context}")
            except Exception as e:
                print(f"Error retrieving from knowledge base: {e}")
        
        # Add knowledge to system prompt if available
        if knowledge_context:
            system_prompt += knowledge_context
            
        # Prepare messages for the API call
        messages = [{"role": "system", "content": system_prompt}]
        
        # Include relevant conversation history (last 4 exchanges)
        for item in self.conversation_history[-8:]:
            messages.append(item)
            
        try:
            response = self.client.generate_response(
                messages=messages,
                temperature=0.7  # Higher temperature for more creative responses
            )
            log('DEBUG', f"LLM response: {response}")   
            llm_response = response.strip()
            
            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": llm_response})
            
            return llm_response
            
        except Exception as e:
            # Fallback to template-based response
            print(f"Error generating LLM response: {e}")
            return self._generate_template_response(node_id, user_input)
    
    def _generate_template_response(self, node_id, user_input):
        """Fallback method using template-based responses"""
        node = self.nodes[node_id]
        
        if node_id == "reflection":
            summary = "feelings of " + user_input.split()[-1] if user_input else "various emotions"
            return node["prompt"].replace("{summary}", summary)
        elif node_id == "support":
            strategies = "practicing mindfulness, talking with friends, and engaging in physical activity"
            return node["prompt"].replace("{strategies}", strategies)
        else:
            return node["prompt"]
    
    def execute_node(self, node_id, user_input=None):
        """Execute a node in the workflow"""
        # If we're executing a tool-related node, handle it differently
        if node_id == "tool_use":
            # For tool_use node, we should generate a response with tools
            # rather than trying to execute a tool immediately
            node_info = self.nodes[node_id]
            return self.generate_response_with_tools(node_id, user_input)
        
        # Regular node execution
        # Get node information
        node_info = self.nodes[node_id]
        
        # Check if LLM should generate dynamic response or use template
        if user_input:
            # User has provided input, generate dynamic response
            return self.generate_response_with_llm(node_id, user_input)
        elif "tools" in node_info and node_info["tools"]:
            # Tools are available but no user input yet, give a prompt that explains available tools
            tool_intro = "I can help you with several specialized functions. Just let me know what you need assistance with."
            return tool_intro
        else:
            # Basic template response
            return node_info["prompt"]

    def generate_response_with_tools(self, node_id, user_input):
        """Generate a response with potential tool usage"""
        # Add current exchange to conversation history
        if user_input:
            self.conversation_history.append({"role": "user", "content": user_input})
        
        # Create system prompt based on current node
        node_info = self.nodes[node_id]
        system_prompt = get_assistant_prompt(node_id, node_info)
        
        # Add tool description if tools are available for this node
        if "tools" in node_info and node_info["tools"]:
            available_tools = {tool: AVAILABLE_TOOLS[tool] for tool in node_info["tools"] if tool in AVAILABLE_TOOLS}
            if available_tools:
                tools_description = json.dumps(available_tools, indent=2)
                system_prompt += f"\n\nYou have access to the following tools:\n{tools_description}\n"
                system_prompt += "\nIf you believe a tool would help address the user's needs, you can use it by responding with:\n"
                system_prompt += '{"tool": "tool_name", "parameters": {"param1": "value1", ...}}'
                system_prompt += "\nBe warm, empathetic, and conversational - avoid clinical or generic questions\n"
                system_prompt += "\nOnly use tools when they would clearly benefit the conversation."
        
        # Knowledge context handling remains the same as before
        # [...]
        # Send messages to LLM
        messages = [{"role": "system", "content": system_prompt}]
        
        # Include relevant conversation history (last 8 exchanges)
        for item in self.conversation_history[-8:]:
            messages.append(item)
            
        try:
            response = self.client.generate_response(
                messages=messages,
                temperature=0.7
            )
            log('DEBUG', f"LLM response: {response}")
            
            # Check if the response is a tool call
            if response.strip().startswith("{") and "tool" in response:
                try:
                    tool_call = json.loads(response)
                    # Add the assistant's intent to use a tool to the conversation
                    self.conversation_history.append({
                        "role": "assistant", 
                        "content": f"I'll use the {tool_call['tool']} tool to help address your question."
                    })
                    
                    # Move to tool execution node
                    self.tool_to_execute = tool_call
                    return self.execute_tool_node(user_input)
                except json.JSONDecodeError:
                    # Not a valid JSON, treat as normal response
                    pass
            
            # Normal response handling
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
                
        except Exception as e:
            # Fallback to template-based response
            print(f"Error generating LLM response: {e}")
            return self._generate_template_response(node_id, user_input)

    def execute_tool_node(self, user_input):
        """Execute a tool and incorporate the result into the conversation"""
        if not hasattr(self, 'tool_registry'):
            from tools.tools import ToolRegistry
            self.tool_registry = ToolRegistry(knowledge_base=self.knowledge_base)
        
        if not hasattr(self, 'tool_to_execute'):
            return "I'm not sure which tool to use. Could you clarify your question?"
        
        tool_call = self.tool_to_execute
        tool_name = tool_call.get('tool')
        parameters = tool_call.get('parameters', {})
        
        # Execute the tool
        result = self.tool_registry.execute_tool(tool_name, parameters)
        
        # Record tool execution in conversation history
        self.conversation_history.append({
            "role": "system", 
            "content": f"Tool execution result: {json.dumps(result)}"
        })
        
        # For assessment tools, provide specific guidance to the LLM
        if tool_name == "assessment_tool" and "guidance" in result.get("result", {}):
            assessment_info = result["result"].get("assessment_info", {})
            guidance = result["result"].get("guidance", "")
            
            messages = [
                {"role": "system", "content": f"You are conducting a psychological assessment. {guidance}\n\n"
                                             f"Assessment: {assessment_info.get('name')}\n"
                                             f"Description: {assessment_info.get('description')}\n"
                                             f"Begin by introducing the assessment and its purpose, then ask the first question."}
            ]
            
            # Include recent conversation history
            for item in self.conversation_history[-4:]:
                messages.append(item)
            
            # Generate assessment introduction and first question
            response = self.client.generate_response(
                messages=messages,
                temperature=0.7
            )
            
            # Save the current assessment type for future reference
            self.current_assessment_type = parameters.get("assessment_type")
            
            # Add to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep tool_to_execute for follow-up
            self.in_assessment = True
            return response
        
        # For continuing an assessment that's in progress
        if hasattr(self, 'in_assessment') and self.in_assessment:
            messages = [
                {"role": "system", "content": "You are continuing a psychological assessment. "
                                             "Review the user's response and either:\n"
                                             "1. Ask the next question in the sequence if more questions remain\n"
                                             "2. Provide a thoughtful analysis if all questions have been answered\n\n"
                                             "Do not show numerical scores. Focus on patterns and helpful insights."}
            ]
            
            # Include more conversation history for assessment context
            for item in self.conversation_history[-12:]:
                messages.append(item)
            
            response = self.client.generate_response(
                messages=messages,
                temperature=0.7
            )
            
            # Check if this appears to be the end of the assessment
            assessment_complete = any(phrase in response.lower() for phrase in 
                                    ["based on your responses", "your assessment results", 
                                     "assessment complete", "here's what i've gathered"])
            
            # If assessment is complete, clear the assessment state
            if assessment_complete:
                self.in_assessment = False
                if hasattr(self, 'current_assessment_type'):
                    delattr(self, 'current_assessment_type')
                if hasattr(self, 'tool_to_execute'):
                    delattr(self, 'tool_to_execute')
            
            # Add to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # For other tools, generate a response based on tool results
        messages = [
            {"role": "system", "content": "You are a helpful assistant. The system has just executed a tool. "
                                         "Formulate a helpful response based on the tool results. "
                                         "Make your response conversational and friendly, as if you're having a natural "
                                         "dialogue. Don't mention that you used a tool unless necessary."}
        ]
        
        # Include relevant conversation history
        for item in self.conversation_history[-6:]:
            messages.append(item)
        
        # Generate response
        try:
            response = self.client.generate_response(
                messages=messages,
                temperature=0.7
            )
            
            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Clear the tool execution state
            if hasattr(self, 'tool_to_execute'):
                delattr(self, 'tool_to_execute')
            
            return response
            
        except Exception as e:
            print(f"Error generating tool response: {e}")
            # Simple fallback
            return "Based on the information I've gathered, I can provide some insights about your situation. Would you like to discuss specific strategies or concerns?"

    def get_next_node(self, current_node_id, user_input=None):
        """Get the ID of the next node in the workflow, using LLM if input is provided"""
        try:
            # If we have user input, use LLM to determine next node
            if user_input:
                return self.select_node_with_llm(current_node_id, user_input)
            else:
                # Otherwise use the default next node
                return self.nodes[current_node_id]["next"]
        except (KeyError, TypeError):
            # Default to assessment if there's an error
            return "assessment"