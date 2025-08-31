#!/usr/bin/env python3

"""
Test what the SwitchAgent actually returns for "Explain solar system"
"""

def test_switch_logic():
    """Test the SwitchAgent keyword matching logic"""
    
    test_input = "Explain solar system"
    
    keyword_mapping = {
        "machine learning": "chat_science_flow",
        "data analysis": "chat_science_flow", 
        "software": "chat_engineering_flow",
        "programming": "chat_engineering_flow",
        "development": "chat_engineering_flow"
    }
    
    default_flow = "chat_default_flow"
    
    print(f"🧪 Testing SwitchAgent logic for: '{test_input}'")
    print(f"📋 Keyword mappings: {keyword_mapping}")
    print(f"🔧 Default flow: {default_flow}")
    
    # Test each keyword
    matched_keywords = []
    for keyword, flow_name in keyword_mapping.items():
        if keyword.lower() in test_input.lower():
            matched_keywords.append((keyword, flow_name))
            print(f"  ✅ MATCH: '{keyword}' → {flow_name}")
        else:
            print(f"  ❌ NO MATCH: '{keyword}'")
    
    if matched_keywords:
        # Use the first match
        final_flow = matched_keywords[0][1]
        print(f"\n🎯 Result: First match '{matched_keywords[0][0]}' → {final_flow}")
    else:
        final_flow = default_flow
        print(f"\n🎯 Result: No matches → default: {final_flow}")
    
    # Check what the first agent would be in each flow
    workflows = {
        "chat_default_flow": ["WorkflowStart", "SwitchAgent", "Agent1", "DisplayAgent1", "Agent2", "DisplayAgent2", "UserInputPoint", "Agent3", "Agent4", "Agent5", "DisplayFinal", "WorkflowComplete"],
        "chat_science_flow": ["WorkflowStart", "Agent2", "DisplayAgent1", "Agent4", "DisplayAgent2", "Agent5", "DisplayFinal", "WorkflowComplete"],
        "chat_engineering_flow": ["WorkflowStart", "Agent3", "DisplayAgent1", "Agent2", "DisplayAgent2", "Agent4", "Agent5", "DisplayFinal", "WorkflowComplete"]
    }
    
    if final_flow in workflows:
        flow_agents = workflows[final_flow]
        print(f"\n📊 Workflow '{final_flow}' sequence:")
        for i, agent in enumerate(flow_agents):
            print(f"  {i+1}. {agent}")
        
        # If we switch workflow after SwitchAgent, where do we restart?
        first_agent_after_switch = flow_agents[0]  # This is what WorkflowManager does
        print(f"\n⚠️  After switch, restart from: {first_agent_after_switch}")
        
        if final_flow == "chat_science_flow":
            print("🔍 POTENTIAL ISSUE: chat_science_flow starts with WorkflowStart → Agent2")
            print("   If we restart from WorkflowStart, it will loop!")
            print("   If we restart from Agent2, DisplayAgent1 will get Agent2's output!")
            
        if final_flow == "chat_engineering_flow":
            print("🔍 POTENTIAL ISSUE: chat_engineering_flow starts with WorkflowStart → Agent3")
            print("   If we restart from WorkflowStart, it will loop!")
            print("   If we restart from Agent3, DisplayAgent1 will get Agent3's output!")

if __name__ == "__main__":
    test_switch_logic()
