import streamlit as st
from agents.workflow import Workflow
import os

def initialize_session():
    """Initialize session state variables if they don't exist"""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'workflow' not in st.session_state:
        st.session_state.workflow = Workflow()
    if 'current_node' not in st.session_state:
        st.session_state.current_node = "greeting"
    if 'greeting_shown' not in st.session_state:
        st.session_state.greeting_shown = False
    
    # Initialize model settings
    if 'chat_provider' not in st.session_state:
        st.session_state.chat_provider = "deepseek"
    if 'chat_model' not in st.session_state:
        st.session_state.chat_model = "deepseek-chat"
    if 'chat_api_key' not in st.session_state:
        st.session_state.chat_api_key = ""
    if 'chat_api_base' not in st.session_state:
        st.session_state.chat_api_base = "https://api.deepseek.com/v1"
        
    # Embedding model settings
    if 'embedding_provider' not in st.session_state:
        st.session_state.embedding_provider = "openai"
    if 'embedding_model' not in st.session_state:
        st.session_state.embedding_model = "text-embedding-3-small"
    if 'embedding_api_key' not in st.session_state:
        st.session_state.embedding_api_key = ""
    if 'embedding_api_base' not in st.session_state:
        st.session_state.embedding_api_base = "https://api.openai.com/v1"

def display_conversation():
    """Display the conversation history with auto-scrolling"""
    # Create a container for the conversation with fixed height for scrolling
    chat_container = st.container()
    
    # Display all messages in the container
    with chat_container:
        for message in st.session_state.conversation_history:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.markdown(message['content'])
            else:
                with st.chat_message("assistant", avatar="🧠"):
                    st.markdown(message['content'])
    
    # Auto-scroll to bottom using JavaScript
    if st.session_state.conversation_history:
        js = '''
        <script>
            function scrollToBottom() {
                const mainBody = window.parent.document.querySelector('.main');
                if (mainBody) {
                    mainBody.scrollTo({
                        top: mainBody.scrollHeight,
                        behavior: 'smooth'
                    });
                }
            }
            setTimeout(scrollToBottom, 300);
        </script>
        '''
        st.components.v1.html(js, height=0)

def process_user_input(user_input):
    """Process user input through the agent workflow"""
    # Add user message to history
    st.session_state.conversation_history.append({
        'role': 'user',
        'content': user_input
    })
    
    # Execute current node with user input
    workflow = st.session_state.workflow
    result = workflow.execute_node(st.session_state.current_node, user_input)
    
    # Add assistant response to history
    if result:
        st.session_state.conversation_history.append({
            'role': 'assistant',
            'content': result
        })
    
    # Move to the next node in the workflow
    st.session_state.current_node = workflow.get_next_node(st.session_state.current_node, user_input)

def main():
    st.set_page_config(
        page_title="MindIO Chat",
        page_icon="🧠",
        layout="centered"
    )
    
    # Initialize session
    initialize_session()
    
    # Apply some custom CSS to improve the chat interface
    st.markdown("""
    <style>
        /* Increase the chat container height */
        .element-container {
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
        }
        
        /* Style the chat messages */
        .stChatMessage {
            padding: 10px;
            border-radius: 15px;
            margin-bottom: 10px;
        }
        
        /* Keep the chat input visible at the bottom */
        .stChatInputContainer {
            position: sticky;
            bottom: 0;
            background-color: white;
            padding: 10px 0;
            z-index: 100;
        }
        
        /* Make the main content area taller */
        .main {
            height: calc(100vh - 80px);
            overflow-y: auto;
        }
        
        /* Add a bit of margin to the bottom to ensure we can scroll to see the last message */
        .block-container {
            padding-bottom: 100px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # App title
    st.title("MindIO Chat")
    
    # Display greeting message if it hasn't been shown yet
    if not st.session_state.greeting_shown:
        greeting = st.session_state.workflow.execute_node("greeting")
        st.session_state.conversation_history.append({
            'role': 'assistant',
            'content': greeting
        })
        st.session_state.greeting_shown = True
    
    # Display conversation history
    display_conversation()
    
    # Chat input - always at the bottom
    st.markdown('<div class="stChatInputContainer">', unsafe_allow_html=True)
    user_input = st.chat_input("Type your message here...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if user_input:
        process_user_input(user_input)
        st.rerun()  # Refresh the app to show the updated conversation

if __name__ == "__main__":
    main()