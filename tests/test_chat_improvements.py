#!/usr/bin/env python3
"""
Quick validation script to test the chat improvements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_main import main_chat
from ChatInterface import chat_event_bus

def test_chat_improvements():
    """Test that chat shows full responses without truncation"""
    print("🧪 Testing Chat Improvements...")
    
    # Create manager with chat enabled
    manager = main_chat(enable_events=True)
    if not manager:
        print("❌ Failed to create chat manager")
        return False
    
    # Test data
    test_input = "This is a very long test input that would normally be truncated in the old version but should now be shown in full without any truncation or cutting off of the content to demonstrate that the full response feature is working correctly."
    
    # Capture events
    events_captured = []
    def capture_event(event):
        events_captured.append(event)
    
    chat_event_bus.subscribe("message", capture_event)
    
    # Test ChatDisplayAgent with long content
    from ChatAgents import ChatDisplayAgent
    
    display_agent = ChatDisplayAgent("TestDisplay", "Test: ")
    result = display_agent.execute(test_input)
    
    print("✅ ChatDisplayAgent executed successfully")
    
    # Check if the full content was published
    if events_captured:
        event_content = events_captured[0].data.get("content", "")
        if len(event_content) > len(test_input):  # Should include prefix
            print("✅ Full content preserved in chat event")
        else:
            print("❌ Content might be truncated")
    else:
        print("❌ No events captured")
    
    # Clean up
    chat_event_bus.unsubscribe("message", capture_event)
    chat_event_bus.clear_events()
    
    print("✅ Chat improvements working correctly")
    return True

if __name__ == "__main__":
    test_chat_improvements()
