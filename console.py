from agents.workflow import Workflow
import os
from history.record import save_conversation, get_conversation_by_index, list_conversations

class CommandLineInterface:
    def __init__(self):
        self.conversation_history = []
        self.workflow = Workflow()
        self.current_node = "greeting"
        self.greeting_shown = False

    def process_user_input(self, user_input):
        """Process user input and update conversation history"""
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Use LLM to select next node
        try:
            self.current_node = self.workflow.select_node_with_llm(self.current_node, user_input)
        except AttributeError:
            if hasattr(self.workflow, 'get_next_node'):
                self.current_node = self.workflow.get_next_node(self.current_node)

        # Execute current node and get result
        result = self.workflow.execute_node(self.current_node, user_input)
        
        # Add assistant response to history
        if result:
            self.conversation_history.append({
                'role': 'assistant',
                'content': result
            })
            print(f"\nAssistant: {result}")
        return True
    
    def display_greeting(self):
        """Display welcome message"""
        if not self.greeting_shown:
            try:
                greeting = self.workflow.execute_node("greeting")
                if greeting:
                    self.conversation_history.append({
                        'role': 'assistant',
                        'content': greeting
                    })
                    print(f"Assistant: {greeting}")
                    self.greeting_shown = True
            except Exception as e:
                print(f"Error displaying greeting: {str(e)}")
    
    def save_current_conversation(self):
        """Save current conversation history"""
        filename = save_conversation(self.conversation_history)
        print(f"Conversation saved to {filename}")
        
    def load_conversation_file(self, index):
        """Load conversation file and restore context"""
        loaded_history = get_conversation_by_index(index)
        if not loaded_history:
            print(f"\nError: Could not load conversation or file is empty")
            return False
            
        # Update conversation history
        self.conversation_history = loaded_history
        self.workflow.conversation_history = loaded_history.copy()
        
        # Determine current node
        self._determine_current_node(loaded_history)
        
        # Display loading information
        print(f"Loaded {len(loaded_history)} messages")
        if loaded_history:
            last_msg = loaded_history[-1]
            print(f"Last message ({last_msg['role']}): {last_msg['content']}")
        return True
        
    def _determine_current_node(self, history):
        """Determine current node based on loaded conversation history"""
        try:
            if len(history) >= 2:
                last_user_input = next((msg["content"] for msg in reversed(history) 
                                       if msg["role"] == "user"), None)
                if last_user_input:
                    self.current_node = self.workflow.select_node_with_llm("assessment", last_user_input)
                    print(f"Current conversation node set to: {self.current_node}")
        except Exception as e:
            print(f"\nWarning: Could not determine conversation node: {e}")
            self.current_node = "assessment"  # Default node
    
    def list_saved_conversations(self):
        """List all saved conversation files"""
        files = list_conversations()
        if files:
            print("\nSaved conversations:")
            for i, f in enumerate(files):
                print(f"{i+1}. {f}")
        else:
            print("\nNo saved conversations found.")

    def show_help(self):
        """Display available commands help"""
        print("\n=== Available Commands ===")
        print("/h - Show this help message")
        print("/x - Exit the application")
        print("/s - Save conversation")
        print("/l <index> - Load conversation from file")
        print("/ls - List all saved conversations")
        print("=========================\n")

    def start(self):
        """Start interactive console"""
        print("\n===== MindIO Command Line Interface =====")
        print("/h for help or /x to exit at any time.")
        print("========================================\n")
        
        # Display greeting
        self.display_greeting()
        
        # Main interaction loop
        running = True
        while running:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle commands
                if user_input.lower() == "/x":
                    print("\nGood bye!\n")
                    running = False
                elif user_input.lower() == "/h":
                    self.show_help()
                elif user_input.lower() == "/s":
                    self.save_current_conversation()
                elif user_input.lower().startswith("/l "):
                    self.load_conversation_file(user_input[3:].strip())
                elif user_input.lower() == "/ls":
                    self.list_saved_conversations()
                else:
                    # Process regular conversation input
                    self.process_user_input(user_input)
                    
            except KeyboardInterrupt:
                print("\n\nPressed Ctrl+C. Type /x to quit.")
            except EOFError:
                print("\n\nInput ended. Exiting...")
                running = False
            except Exception as e:
                print(f"\nError: {str(e)}")

def main():
    # Create and start interface
    cli = CommandLineInterface()
    cli.start()

if __name__ == "__main__":
    main()