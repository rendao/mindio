from agents.workflow import Workflow
import os
import argparse
import importlib


class CommandLineInterface:
    def __init__(self, workflow_class=None):
        self.conversation_history = []
        self.workflow = workflow_class() if workflow_class else Workflow()
        self.current_node = "greeting"
        self.greeting_shown = False

    def process_user_input(self, user_input):
        """Process user input through the agent workflow"""
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        # Execute current node with user input
        try:
            # Use select_node_with_llm if available
            try:
                self.current_node = self.workflow.select_node_with_llm(self.current_node, user_input)
            except AttributeError:
                # For backwards compatibility with workflows that use get_next_node
                if hasattr(self.workflow, 'get_next_node'):
                    self.current_node = self.workflow.get_next_node(self.current_node)

            result = self.workflow.execute_node(self.current_node, user_input)
            
            # Add assistant response to history
            if result:
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': result
                })
                print(f"\nAssistant: {result}")
    
            return True
        except Exception as e:
            print(f"\nError: {str(e)}")
            return False

    def show_help(self):
        """Display available commands"""
        print("\n=== Available Commands ===")
        print("/h - Show this help message")
        print("/x - Exit the application")
        print("=========================\n")

    def start(self):
        """Start the interactive console"""
        print("\n===== MindIO Command Line Interface =====")
        print("Type /h for available commands")
        print("========================================\n")
        
        # Display greeting if not shown yet
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
        
        # Main interaction loop
        running = True
        while running:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle commands
                if user_input.lower() == "/x":
                    print("\nGoodbye!\n")
                    running = False
                elif user_input.lower() == "/h":
                    self.show_help()
                else:
                    # Process as normal conversation input
                    self.process_user_input(user_input)
                    
            except KeyboardInterrupt:
                print("\n\nPressed Ctrl+C. Type /x to quit.")
            except EOFError:
                print("\n\nInput ended. Exiting...")
                running = False
            except Exception as e:
                print(f"\nError: {str(e)}")

def main():

    # Load the workflow class
    workflow_class = None

    # Create and start the interface
    cli = CommandLineInterface(workflow_class)
    cli.start()


if __name__ == "__main__":
    main()