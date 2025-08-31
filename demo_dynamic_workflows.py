#!/usr/bin/env python3

from SwitchAgent import SwitchAgent
from WorkflowManager import WorkflowManager
from Agent import LLMAgent
from prompt_loader import prompt_loader

def demo_dynamic_workflow_creation():
    """Demonstrate how to dynamically create new workflows and configure the SwitchAgent"""
    
    print("=" * 80)
    print("DEMONSTRATION: DYNAMIC WORKFLOW CREATION WITH CONFIGURABLE SWITCH AGENT")
    print("=" * 80)
    
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
    
    # Create configurable switch agent
    switch_config = {
        "use_llm_decision": True,
        "keyword_mapping": {
            "creative": "creative_flow",
            "writing": "creative_flow", 
            "story": "creative_flow",
            "urgent": "emergency_flow",
            "emergency": "emergency_flow",
            "critical": "emergency_flow",
            "financial": "finance_flow",
            "money": "finance_flow",
            "budget": "finance_flow"
        },
        "default_flow": "standard_flow"
    }
    
    switch_agent = SwitchAgent(
        name="SwitchAgent",
        model_config=model_config,
        system=switch_prompt,
        retry_limit=1,
        workflow_config=switch_config
    )
    
    # Create agents for different purposes
    agents = {
        "Intake": LLMAgent(name="Intake", model_config=model_config, system="Initial processing", retry_limit=1),
        "CreativeWriter": LLMAgent(name="CreativeWriter", model_config=model_config, system="Creative content", retry_limit=1),
        "TechnicalAnalyst": LLMAgent(name="TechnicalAnalyst", model_config=model_config, system="Technical analysis", retry_limit=1),
        "EmergencyHandler": LLMAgent(name="EmergencyHandler", model_config=model_config, system="Emergency processing", retry_limit=1),
        "FinancialExpert": LLMAgent(name="FinancialExpert", model_config=model_config, system="Financial analysis", retry_limit=1),
        "QualityChecker": LLMAgent(name="QualityChecker", model_config=model_config, system="Quality assurance", retry_limit=1),
        "FinalReporter": LLMAgent(name="FinalReporter", model_config=model_config, system="Final reporting", retry_limit=1)
    }
    
    # Register all agents
    for agent in agents.values():
        manager.add_agent(agent)
    manager.add_agent(switch_agent)
    
    print("\n📋 Step 1: Creating workflows dynamically...")
    
    # Create different workflow patterns
    workflows = {
        "standard_flow": {
            "Intake": ["TechnicalAnalyst"],
            "TechnicalAnalyst": ["QualityChecker"],
            "QualityChecker": ["FinalReporter"],
            "FinalReporter": []
        },
        "creative_flow": {
            "Intake": ["CreativeWriter"],
            "CreativeWriter": ["QualityChecker"],
            "QualityChecker": ["FinalReporter"],
            "FinalReporter": []
        },
        "emergency_flow": {
            "EmergencyHandler": ["FinalReporter"],
            "FinalReporter": []
        },
        "finance_flow": {
            "Intake": ["FinancialExpert"],
            "FinancialExpert": ["QualityChecker"],
            "QualityChecker": ["FinalReporter"],
            "FinalReporter": []
        }
    }
    
    # Add all workflows
    for workflow_name, workflow_config in workflows.items():
        manager.add_workflow(workflow_name, workflow_config)
        print(f"   ✅ Added workflow: {workflow_name}")
    
    print(f"\n🔄 Step 2: SwitchAgent automatically updated with {len(workflows)} available flows")
    print(f"   Available flows: {list(workflows.keys())}")
    
    print(f"\n🎯 Step 3: Testing workflow selection...")
    
    # Test different scenarios
    test_scenarios = [
        ("Write a creative story about space", "Should select creative_flow"),
        ("Urgent: System is down!", "Should select emergency_flow"),
        ("Analyze our budget for next quarter", "Should select finance_flow"),
        ("Standard technical analysis needed", "Should select standard_flow"),
        ("Help me with writing a novel", "Should select creative_flow"),
        ("Critical security breach detected", "Should select emergency_flow"),
        ("Review financial statements", "Should select finance_flow")
    ]
    
    for test_input, expected in test_scenarios:
        print(f"\n   📝 Input: '{test_input}'")
        print(f"      Expected: {expected}")
        
        result = switch_agent.execute(test_input)
        if result["success"] and "switch_flow" in result:
            print(f"      ✅ Selected: {result['switch_flow']}")
        else:
            print(f"      ❌ Failed: {result}")
    
    print("\n" + "=" * 80)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("\n✅ Key Benefits of Configurable SwitchAgent:")
    print("   1. Dynamic Flow Discovery: Automatically detects available workflows")
    print("   2. Intelligent LLM Decisions: Uses AI to understand context and intent")
    print("   3. Custom Keyword Mapping: Allows precise control over routing rules")
    print("   4. Easy Workflow Addition: No code changes needed to add new flows")
    print("   5. Backward Compatible: Still supports old hardcoded patterns")
    print("   6. Flexible Configuration: Can be tuned per use case")
    
    print("\n🛠️ Configuration Options:")
    print("   • use_llm_decision: Enable/disable AI-powered routing")
    print("   • keyword_mapping: Define custom keyword → flow mappings")
    print("   • default_flow: Set fallback flow for unmatched inputs")
    print("   • System prompt automatically updates with available flows")
    
    print("\n🔮 Future Possibilities:")
    print("   • Machine learning-based flow recommendation")
    print("   • User preference learning")
    print("   • Context-aware routing based on conversation history")
    print("   • Dynamic workflow creation based on patterns")

if __name__ == "__main__":
    demo_dynamic_workflow_creation()
