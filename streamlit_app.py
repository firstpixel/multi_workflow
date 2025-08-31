"""
Streamlit Chat Interface for Multi-Workflow AI System

This module provides a web-based chat interface using Streamlit that integrates
with the multi-workflow AI system without creating tight coupling.
"""

import streamlit as st
import threading
import time
from datetime import datetime
from ChatInterface import chat_event_bus, ChatEvent
from enhanced_main import main_chat
import sys
from io import StringIO


# Configure Streamlit page
st.set_page_config(
    page_title="Multi-Workflow AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_workflow_manager():
    """Initialize the workflow manager for chat interface"""
    # Suppress console output during initialization
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        # Create workflow manager with chat integration
        manager = main_chat(enable_events=True)
        
        if manager is None:
            st.error("❌ Failed to initialize workflow manager. Check if prompts are loaded correctly.")
            return None
            
        return manager
        
    except Exception as e:
        st.error(f"❌ Error initializing workflow: {str(e)}")
        return None
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr


def run_workflow_in_background(manager, user_input, workflow_name="WorkflowStart"):
    """Run workflow in background thread"""
    try:
        # Suppress console output during workflow execution
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        manager.run_workflow(start_agent_name=workflow_name, input_data=user_input)
        
        sys.stdout = original_stdout
        
    except Exception as e:
        chat_event_bus.publish(ChatEvent("message", {
            "sender": "System",
            "content": f"❌ Error running workflow: {str(e)}",
            "type": "error"
        }))


def format_message_content(data):
    """Format message content based on type"""
    content = data["content"]
    message_type = data.get("type", "info")
    sender = data["sender"]
    
    if message_type == "workflow_start":
        return f"🚀 **{content}**"
    elif message_type == "workflow_complete":
        return f"✅ **{content}**"
    elif message_type == "context":
        return f"📋 *{content}*"
    elif message_type == "agent_output":
        return f"**{sender}**: {content}"
    elif message_type == "agent_waiting":
        return f"⏳ **{sender}**: {content}"
    elif message_type == "agent_error":
        return f"❌ **{sender}**: {content}"
    elif message_type == "workflow_switch":
        return f"🔀 **{content}**"
    elif message_type == "final_output":
        return f"📄 **Final Result**: {content}"
    else:
        return content


def main():
    # Main title
    st.title("🤖 Multi-Workflow AI Chat Interface")
    
    # Sidebar configuration
    st.sidebar.title("🔧 Workflow Controls")
    st.sidebar.markdown("### Available Workflows")
    st.sidebar.markdown("""
    - **Default Flow**: Complete analysis pipeline with user interaction
    - **Science Flow**: Scientific analysis focused workflow
    - **Engineering Flow**: Technical development focused workflow
    """)
    
    # Display options
    st.sidebar.markdown("### Display Options")
    show_system_messages = st.sidebar.checkbox("Show system messages", value=True)
    auto_scroll = st.sidebar.checkbox("Auto-scroll to latest message", value=True)
    
    # Workflow selection
    st.sidebar.markdown("### Workflow Selection")
    workflow_options = {
        "Chat Default Flow": "WorkflowStart",
        "Science Flow": "WorkflowStart", 
        "Engineering Flow": "WorkflowStart"
    }
    selected_workflow = st.sidebar.selectbox(
        "Choose workflow",
        options=list(workflow_options.keys()),
        index=0
    )
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'workflow_manager' not in st.session_state:
        with st.spinner("🔄 Initializing AI workflow system..."):
            st.session_state.workflow_manager = initialize_workflow_manager()
            if st.session_state.workflow_manager is None:
                st.stop()
    if 'workflow_running' not in st.session_state:
        st.session_state.workflow_running = False
    if 'total_messages' not in st.session_state:
        st.session_state.total_messages = 0
    
    # Status indicator
    status_container = st.container()
    with status_container:
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.session_state.workflow_running:
                st.status("🔄 Workflow Running", state="running")
            elif chat_event_bus.waiting_for_input:
                st.status("⏳ Waiting for Input", state="running") 
            else:
                st.status("✅ Ready", state="complete")
        
        with col2:
            st.metric("Messages", len(st.session_state.messages))
        
        with col3:
            if st.button("🔄 Reset Chat", help="Clear all messages and reset the chat"):
                st.session_state.messages = []
                chat_event_bus.clear_events()
                st.rerun()
    
    # Main chat interface
    st.markdown("### 💬 Chat with AI Workflow System")
    
    # Chat container
    chat_container = st.container()
    
    # Process pending events
    events = chat_event_bus.get_events()
    new_messages_added = False
    
    for event in events:
        if event.event_type == "message":
            data = event.data
            
            # Filter messages based on user preferences - removed processing messages
            if not show_system_messages and data.get("type") in ["workflow_start", "workflow_switch"]:
                continue
            
            role = "assistant" if data["sender"] != "User" else "user"
            content = format_message_content(data)
            
            message = {
                "role": role, 
                "content": content, 
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "sender": data["sender"],
                "type": data.get("type", "info")
            }
            
            # Avoid duplicates
            if message not in st.session_state.messages:
                st.session_state.messages.append(message)
                new_messages_added = True
    
    # Display chat messages
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                # Show timestamp and sender for assistant messages
                if message["role"] == "assistant":
                    st.caption(f"{message['sender']} • {message['timestamp']}")
                st.markdown(message["content"])
    
    # Handle user input requests
    if chat_event_bus.waiting_for_input and chat_event_bus.current_input_request:
        st.warning(f"⏳ **AI is requesting input**: {chat_event_bus.current_input_request['prompt']}")
        
        # Create unique key for input widget
        input_key = f"input_{chat_event_bus.current_input_request['timestamp']}"
        
        col1, col2 = st.columns([4, 1])
        with col1:
            user_response = st.text_input(
                "Your response:", 
                key=input_key,
                placeholder="Type your response here..."
            )
        with col2:
            send_response = st.button("Send", key=f"send_{input_key}")
        
        if send_response and user_response:
            chat_event_bus.provide_user_input(user_response)
            st.rerun()
    
    # Main chat input (only when not waiting for specific input)
    elif not st.session_state.workflow_running and not chat_event_bus.waiting_for_input:
        if prompt := st.chat_input("Enter your request to start the AI workflow..."):
            # Add user message
            user_message = {
                "role": "user", 
                "content": prompt, 
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "sender": "User",
                "type": "user_input"
            }
            st.session_state.messages.append(user_message)
            
            # Start workflow
            st.session_state.workflow_running = True
            
            # Clear any existing events
            chat_event_bus.clear_events()
            
            # Switch workflow based on selection
            workflow_name = workflow_options[selected_workflow]
            
            # Run workflow in background thread
            workflow_thread = threading.Thread(
                target=run_workflow_in_background,
                args=(st.session_state.workflow_manager, prompt, workflow_name),
                daemon=True
            )
            workflow_thread.start()
            
            st.rerun()
    
    # Check if workflow is complete
    for event in events:
        if event.event_type == "workflow_complete":
            st.session_state.workflow_running = False
            if not chat_event_bus.waiting_for_input:
                st.success("🎉 Workflow completed successfully!")
                time.sleep(1)  # Brief pause to show success message
    
    # Auto-refresh while workflow is running or waiting for input
    if st.session_state.workflow_running or chat_event_bus.waiting_for_input or new_messages_added:
        if auto_scroll:
            time.sleep(0.5)  # Small delay for smoother updates
        st.rerun()
    
    # Footer information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    This is an AI-powered multi-workflow system that can:
    - Analyze complex topics
    - Switch between different processing flows
    - Request user input during processing
    - Provide detailed step-by-step results
    
    **Built with**: Python, Streamlit, Ollama
    """)


if __name__ == "__main__":
    main()
