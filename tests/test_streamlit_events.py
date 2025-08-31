#!/usr/bin/env python3

"""
Test to simulate the exact chat event processing that happens in Streamlit
"""

import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_main import create_base_workflow_manager, create_chat_workflows
from ChatInterface import chat_event_bus

def test_streamlit_event_processing():
    """Simulate the exact event processing that Streamlit does"""
    print("🧪 Testing Streamlit event processing simulation...")
    
    # Initialize workflow manager
    result = create_base_workflow_manager()
    if result is None:
        print("❌ Failed to create workflow manager")
        return False
        
    manager, _ = result
    manager.enable_chat_integration(chat_event_bus)
    create_chat_workflows(manager)
    
    # Collect events like Streamlit does
    collected_events = []
    
    def event_collector(event):
        if event.event_type == "message":
            collected_events.append({
                'sender': event.data.get('sender'),
                'content': event.data.get('content'),
                'type': event.data.get('message_type'),
                'raw_data': event.data
            })
    
    chat_event_bus.subscribe("message", event_collector)
    
    # Run a very simple workflow step to see what events are generated
    print("📝 Simulating workflow execution (first few steps only)...")
    
    # Just test the first few agents to see event patterns
    try:
        # Manually execute first few steps
        print("  Step 1: WorkflowStart")
        workflow_start = manager.agents["WorkflowStart"]
        start_result = workflow_start.execute("Test input")
        
        print("  Step 2: SwitchAgent") 
        switch_agent = manager.agents["SwitchAgent"]
        switch_result = switch_agent.execute(start_result["output"])
        
        print("  Step 3: Agent1")
        agent1 = manager.agents["Agent1"]
        # Simulate that we're in chat mode to test publishing
        manager.chat_enabled = True
        agent1_result = agent1.execute(switch_result["output"])
        
        print("  Step 4: DisplayAgent1") 
        display_agent1 = manager.agents["DisplayAgent1"]
        display_result = display_agent1.execute(agent1_result["output"])
        
    except Exception as e:
        print(f"⚠️ Stopped execution early (expected): {e}")
    
    # Analyze collected events
    print(f"\n📊 Collected {len(collected_events)} events:")
    
    agent_event_counts = {}
    for i, event in enumerate(collected_events):
        sender = event['sender']
        print(f"  {i+1}. {sender}: {event['content'][:80]}...")
        
        # Count by sender
        agent_event_counts[sender] = agent_event_counts.get(sender, 0) + 1
    
    print(f"\n📈 Event counts by sender:")
    duplicates_found = False
    for sender, count in agent_event_counts.items():
        status = "✅" if count == 1 else "❌ DUPLICATE"
        print(f"  {sender}: {count} events {status}")
        if count > 1:
            duplicates_found = True
    
    if duplicates_found:
        print("\n❌ DUPLICATES FOUND - analyzing causes...")
        for sender, count in agent_event_counts.items():
            if count > 1:
                print(f"\n🔍 Analyzing {sender} (appeared {count} times):")
                sender_events = [e for e in collected_events if e['sender'] == sender]
                for i, event in enumerate(sender_events):
                    print(f"  Event {i+1}: {event['content'][:100]}...")
    else:
        print("\n✅ SUCCESS: No duplicate events found!")
    
    return not duplicates_found

if __name__ == "__main__":
    success = test_streamlit_event_processing()
    sys.exit(0 if success else 1)
