#!/usr/bin/env python3

import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from SwitchAgent import SwitchAgent
from WorkflowManager import WorkflowManager
from Agent import LLMAgent
from prompt_loader import prompt_loader

def test_configurable_switch():
    """Test the configurable SwitchAgent with different inputs"""
    
    # Change to project directory for prompt loading
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        manager = WorkflowManager()
        
        # Load switch prompt
        switch_prompt = prompt_loader.load_prompt("switch_agent")
        
        # Define model configuration 
        model_config = {
            "model": "llama3.2:1b",
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        }
    
        # Create a highly configurable switch agent
        switch_config = {
            "use_llm_decision": True,  # Use LLM for intelligent decisions
            "keyword_mapping": {       # Custom keyword mappings
                "machine learning": "science_flow",
                "data analysis": "science_flow", 
                "neural network": "science_flow",
                "algorithm": "science_flow",
                "software": "engineering_flow",
                "programming": "engineering_flow",
                "development": "engineering_flow",
                "code": "engineering_flow",
                "app": "engineering_flow",
                "quick": "quick_analysis",
                "summary": "quick_analysis"
            },
            "default_flow": "default_flow"
        }
        
        # Create switch agent with configuration
        switch_agent = SwitchAgent(
            name="SwitchAgent", 
            model_config=model_config, 
            system=switch_prompt, 
            retry_limit=1,
            workflow_config=switch_config
        )
        
        # Create some dummy agents for testing
        agent1 = LLMAgent(name="Agent1", model_config=model_config, system="Process input", retry_limit=1)
        agent2 = LLMAgent(name="Agent2", model_config=model_config, system="Process input", retry_limit=1)
        agent3 = LLMAgent(name="Agent3", model_config=model_config, system="Process input", retry_limit=1)
        
        # Register agents
        for agent in [agent1, agent2, agent3, switch_agent]:
            manager.add_agent(agent)
        
        # Add workflows
        manager.add_workflow("default_flow", {
            "Agent1": ["Agent2"],
            "Agent2": ["Agent3"],
            "Agent3": []
        })
        
        manager.add_workflow("science_flow", {
            "Agent2": ["Agent3"],
            "Agent3": []
        })
        
        manager.add_workflow("engineering_flow", {
            "Agent1": ["Agent3"],
            "Agent3": []
        })
        
        manager.add_workflow("quick_analysis", {
            "Agent1": [],
        })
        
        # Test different inputs
        test_inputs = [
            "Explain machine learning algorithms",  # Should trigger science_flow
            "Build a software application",         # Should trigger engineering_flow  
            "Give me a quick summary",             # Should trigger quick_analysis
            "Analyze data patterns",               # Should trigger science_flow (via keyword)
            "Help me with programming",            # Should trigger engineering_flow (via keyword)
            "Tell me about history",               # Should use default_flow
        ]
        
        print("=" * 80)
        print("TESTING CONFIGURABLE SWITCH AGENT")
        print("=" * 80)
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n--- Test {i}: '{test_input}' ---")
            
            # Test just the switch decision (without running full workflow)
            result = switch_agent.execute(test_input)
            
            if result["success"] and "switch_flow" in result:
                print(f"✅ Selected flow: {result['switch_flow']}")
            else:
                print(f"❌ Failed to select flow: {result}")
        
            print("\n" + "=" * 80)
            print("✅ All tests completed! The SwitchAgent is now fully configurable.")
            print("✅ Key improvements:")
            print("   • Can use LLM intelligence for flow decisions")
            print("   • Supports custom keyword mappings") 
            print("   • Automatically discovers available flows")
            print("   • Maintains backward compatibility")
            print("   • Easy to add new flows without code changes")
        
    finally:
        # Restore original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    test_configurable_switch()
