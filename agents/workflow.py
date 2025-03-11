from typing import Dict, Any, Callable
from models.chat import ChatModel
from utils.logger import log
from prompts.system import SYSTEM_PROMPT
from prompts.agent import AGENT_PROMPT
from prompts.assistent import get_assistant_prompt
from knowledge.base import KnowledgeBase
from models.embedding import EmbeddingModel

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
        system_prompt = SYSTEM_PROMPT
        
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
        """Execute a workflow node and return the response"""
        try:
            # For the greeting node with no input, use the template
            # if node_id == "greeting" and not user_input:
            #     return self.nodes[node_id]["prompt"]
            
            # For other cases, use LLM to generate response
            return self.generate_response_with_llm(node_id, user_input)
                
        except KeyError:
            # Handle case when node doesn't exist
            return "I'm not sure how to respond to that."
    
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