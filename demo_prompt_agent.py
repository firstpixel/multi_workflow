#!/usr/bin/env python3

from PromptAgent import PromptAgent, EnhancedLLMAgent, InputPreservationManager
from WorkflowManager import WorkflowManager
from prompt_loader import prompt_loader
import json

def demo_prompt_agent_and_input_preservation():
    """
    Demonstrates:
    1. PromptAgent creating/modifying prompts for other agents
    2. Input preservation throughout the workflow chain
    """
    
    print("=" * 80)
    print("DEMONSTRATION: PROMPT AGENT + INPUT PRESERVATION")
    print("=" * 80)
    
    manager = WorkflowManager()
    
    # Load prompts
    try:
        prompt_agent_prompt = prompt_loader.load_prompt("prompt_agent")
        print("✅ Loaded PromptAgent system prompt")
    except FileNotFoundError:
        prompt_agent_prompt = "You are a prompt engineering agent that creates system prompts for other agents."
        print("⚠️  Using fallback PromptAgent prompt")
    
    # Model configuration
    model_config = {
        "model": "llama3.2:1b",
        "temperature": 0.7,
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    
    # Create PromptAgent with knowledge of target agents
    target_agents = {
        "Analyzer": "Analyzes input and breaks down complex topics",
        "Writer": "Generates detailed written content",
        "Summarizer": "Creates concise summaries",
        "Reviewer": "Reviews and improves content quality"
    }
    
    prompt_agent = PromptAgent(
        name="PromptAgent",
        model_config=model_config,
        system=prompt_agent_prompt,
        retry_limit=1,
        target_agents=target_agents
    )
    
    # Create Enhanced LLM Agents that support dynamic prompts and input preservation
    analyzer = EnhancedLLMAgent(
        name="Analyzer",
        model_config=model_config,
        system="You are an analytical agent that breaks down complex topics into understandable components.",
        retry_limit=1
    )
    
    writer = EnhancedLLMAgent(
        name="Writer", 
        model_config=model_config,
        system="You are a writing agent that creates detailed, well-structured content.",
        retry_limit=1
    )
    
    summarizer = EnhancedLLMAgent(
        name="Summarizer",
        model_config=model_config, 
        system="You are a summarization agent that creates concise, informative summaries.",
        retry_limit=1
    )
    
    reviewer = EnhancedLLMAgent(
        name="Reviewer",
        model_config=model_config,
        system="You are a review agent that improves content quality and clarity.",
        retry_limit=1
    )
    
    # Register all agents
    agents = [prompt_agent, analyzer, writer, summarizer, reviewer]
    for agent in agents:
        manager.add_agent(agent)
    
    # Create a workflow that demonstrates both features
    manager.add_workflow("prompt_enhanced_flow", {
        "PromptAgent": ["Analyzer"],      # PromptAgent analyzes and creates prompts
        "Analyzer": ["Writer"],           # Analyzer processes with custom prompt
        "Writer": ["Summarizer"],         # Writer creates content with custom prompt
        "Summarizer": ["Reviewer"],       # Summarizer creates summary with custom prompt
        "Reviewer": []                    # Reviewer finalizes with custom prompt
    })
    
    print("\n📋 Created workflow: PromptAgent → Analyzer → Writer → Summarizer → Reviewer")
    print("   • PromptAgent will create custom prompts for each agent")
    print("   • Original input will be preserved throughout the chain")
    print("   • Each agent will receive optimized prompts for the specific task")
    
    # Test scenarios
    test_scenarios = [
        {
            "input": "Explain quantum computing for a high school student audience",
            "description": "Educational content with specific audience"
        },
        {
            "input": "Write a creative story about time travel with scientific accuracy",
            "description": "Creative writing with technical constraints"
        },
        {
            "input": "Analyze the economic impact of renewable energy adoption",
            "description": "Technical analysis requiring depth and data"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"TEST SCENARIO {i}: {scenario['description']}")
        print(f"Input: '{scenario['input']}'")
        print(f"{'='*60}")
        
        # Run the workflow
        print("\n🚀 Starting workflow...")
        manager.run_workflow("PromptAgent", scenario["input"])
        
        print(f"\n✅ Scenario {i} completed!")
    
    print("\n" + "=" * 80)
    print("🎉 DEMONSTRATION COMPLETE!")
    
    print("\n✅ Key Features Demonstrated:")
    print("   1. PromptAgent Creation:")
    print("      • Analyzes user input and intent")
    print("      • Generates custom system prompts for downstream agents")
    print("      • Optimizes prompts based on task requirements")
    print("      • Provides structured JSON output for agent configuration")
    
    print("\n   2. Input Preservation:")
    print("      • Original user input is maintained throughout the workflow")
    print("      • Each agent can access both original and processed inputs")
    print("      • Full input history is tracked")
    print("      • Agents can work with modified prompts while preserving context")
    
    print("\n🔧 Technical Implementation:")
    print("   • PromptAgent: Specialized agent for prompt engineering")
    print("   • EnhancedLLMAgent: Supports dynamic prompt updates")
    print("   • InputPreservationManager: Utilities for input tracking")
    print("   • Structured data format: Preserves both original and processed data")
    
    print("\n🚀 Benefits:")
    print("   • Adaptive workflows that optimize for specific tasks")
    print("   • Context preservation across complex agent chains")  
    print("   • Dynamic prompt engineering based on user intent")
    print("   • Better output quality through specialized prompts")


def test_input_preservation_only():
    """Test just the input preservation feature independently."""
    
    print("\n" + "=" * 80)
    print("TESTING INPUT PRESERVATION INDEPENDENTLY")
    print("=" * 80)
    
    manager = WorkflowManager()
    
    model_config = {
        "model": "llama3.2:1b",
        "temperature": 0.7,
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    
    # Create a simple chain of Enhanced agents
    agent1 = EnhancedLLMAgent("Agent1", model_config, "You add 'STEP1:' to the input", 1)
    agent2 = EnhancedLLMAgent("Agent2", model_config, "You add 'STEP2:' to the input", 1)
    agent3 = EnhancedLLMAgent("Agent3", model_config, "You add 'STEP3:' to the input", 1)
    
    for agent in [agent1, agent2, agent3]:
        manager.add_agent(agent)
    
    manager.add_workflow("preservation_test", {
        "Agent1": ["Agent2"],
        "Agent2": ["Agent3"], 
        "Agent3": []
    })
    
    print("\n🧪 Testing input preservation with: 'Hello World!'")
    manager.run_workflow("Agent1", "Hello World!")
    
    print("\n✅ Input preservation test completed!")


if __name__ == "__main__":
    demo_prompt_agent_and_input_preservation()
    test_input_preservation_only()
