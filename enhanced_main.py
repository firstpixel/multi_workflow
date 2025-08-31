"""
Enhanced Main Module for Multi-Workflow AI System

This module provides the main workflow setup with optional chat integration.
It maintains backward compatibility with the original terminal version while
adding support for chat interfaces.
"""

from SwitchAgent import SwitchAgent
from WorkflowManager import WorkflowManager
from Agent import LLMAgent
from prompt_loader import prompt_loader
from ChatAgents import ChatDisplayAgent, UserInputAgent, WorkflowStartAgent, WorkflowCompleteAgent
from ChatInterface import chat_event_bus


def custom_validate(result):
    """Custom validation function"""
    output = result.get("output", "")
    return "?" in output.lower() if output else False


def custom_llm_fn(input_data):
    """Custom LLM function that uses a different API or logic."""
    print(f" #################################### TOOL EXECUTED  Custom LLM called with input: {input_data}")
    return f"TOOL EXECUTED  {input_data}"


def create_base_workflow_manager():
    """Create the base workflow manager with all agents"""
    manager = WorkflowManager()

    # Load prompts from files
    try:
        print("Loading prompts from files...")
        prompt1 = prompt_loader.load_prompt("prompt1_breakdown")
        prompt2 = prompt_loader.load_prompt("prompt2_detailed")
        prompt3 = prompt_loader.load_prompt("prompt3_simple")
        prompt4 = prompt_loader.load_prompt("prompt4_refine")
        prompt5 = prompt_loader.load_prompt("prompt5_summary")
        switch_prompt = prompt_loader.load_prompt("switch_agent")
    except FileNotFoundError as e:
        print(f"Error loading prompts: {e}")
        return None

    # Define LLaMA model configuration
    model_config = {
        "model": "llama3.2:1b",
        "temperature": 0.7,
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    model_config2 = {
        "model": "gemma3:latest",
        "temperature": 0.7,
        "top_p": 0.2,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    # Create LLM agents
    agent1 = LLMAgent(name="Agent1", model_config=model_config2, validate_fn=custom_validate, system=prompt1, retry_limit=3, expected_inputs=1)
    agent2 = LLMAgent(name="Agent2", model_config=model_config2, llm_fn=custom_llm_fn, system=prompt2, retry_limit=3, expected_inputs=1)
    agent3 = LLMAgent(name="Agent3", model_config=model_config2, system=prompt3, retry_limit=3, expected_inputs=1)
    agent4 = LLMAgent(name="Agent4", model_config=model_config2, system=prompt4, retry_limit=3, expected_inputs=1)
    agent5 = LLMAgent(name="Agent5", model_config=model_config2, system=prompt5, retry_limit=3, expected_inputs=1)

    # Special switch agent with configuration
    switch_config = {
        "use_llm_decision": True,  # Keep LLM decision making as requested
        "keyword_mapping": {
            "machine learning": "science_flow",
            "data analysis": "science_flow", 
            "software": "engineering_flow",
            "programming": "engineering_flow",
            "development": "engineering_flow"
        },
        "default_flow": "default_flow"
    }
    
    switch_agent = SwitchAgent(
        name="SwitchAgent", 
        model_config=model_config, 
        system=switch_prompt, 
        retry_limit=1,
        workflow_config=switch_config
    )

    # Register core agents
    core_agents = [agent1, agent2, agent3, agent4, agent5, switch_agent]
    for agent in core_agents:
        manager.add_agent(agent)

    return manager, core_agents


def create_terminal_workflows(manager):
    """Create original terminal workflows"""
    # Add original workflows (for terminal mode)
    manager.add_workflow("default_flow", {
        "Agent1": ["Agent2"],
        "Agent2": ["Agent3"],
        "Agent3": ["Agent4"],
        "Agent4": ["Agent5"],
        "Agent5": []
    })

    manager.add_workflow("science_flow", {
        "Agent2": ["Agent4"],
        "Agent4": ["Agent5"],
        "Agent5": []
    })

    manager.add_workflow("engineering_flow", {
        "Agent3": ["Agent2"],
        "Agent2": ["Agent4"],
        "Agent4": ["Agent5"],
        "Agent5": []
    })

    # New configurable workflow for testing
    manager.add_workflow("quick_analysis", {
        "Agent1": ["Agent5"],
        "Agent5": []
    })


def create_chat_workflows(manager):
    """Create chat-enhanced workflows with chat agents"""
    # Create chat enhancement agents
    workflow_start = WorkflowStartAgent("WorkflowStart")
    display_after_agent1 = ChatDisplayAgent("DisplayAgent1", "🧠 Initial Analysis: ")
    display_after_agent2 = ChatDisplayAgent("DisplayAgent2", "🔧 Detailed Processing: ")
    user_input_point = UserInputAgent("UserInputPoint", "Would you like to provide additional context or modifications?")
    display_final = ChatDisplayAgent("DisplayFinal", "📋 Final Result: ")
    workflow_complete = WorkflowCompleteAgent("WorkflowComplete")

    # Register chat agents
    chat_agents = [workflow_start, display_after_agent1, display_after_agent2, 
                   user_input_point, display_final, workflow_complete]
    
    for agent in chat_agents:
        manager.add_agent(agent)

    # Reconfigure SwitchAgent for chat mode - switch to chat workflows instead of terminal workflows
    switch_agent = manager.agents.get("SwitchAgent")
    if switch_agent:
        # Update the switch configuration to point to chat workflows
        switch_agent.keyword_mapping = {
            "machine learning": "chat_science_flow",
            "data analysis": "chat_science_flow", 
            "software": "chat_engineering_flow",
            "programming": "chat_engineering_flow",
            "development": "chat_engineering_flow"
        }
        switch_agent.default_flow = "chat_default_flow"
        
        # Set available flows to the chat workflows
        switch_agent.set_available_flows(["chat_default_flow", "chat_science_flow", "chat_engineering_flow"])

    # Enhanced workflows with chat integration - removed SwitchAgent from individual workflows
    # Add a router workflow that uses SwitchAgent to choose the target workflow
    manager.add_workflow("chat_router", {
        "WorkflowStart": ["SwitchAgent"],
        "SwitchAgent": [],  # SwitchAgent will switch to the target workflow
    })
    
    manager.add_workflow("chat_default_flow", {
        "WorkflowStart": ["Agent1"],
        "Agent1": ["Agent2"],
        "Agent2": ["UserInputPoint"],
        "UserInputPoint": ["Agent3"],
        "Agent3": ["Agent4"],
        "Agent4": ["Agent5"],
        "Agent5": ["WorkflowComplete"],
        "WorkflowComplete": []
    })

    manager.add_workflow("chat_science_flow", {
        "WorkflowStart": ["Agent2"],
        "Agent2": ["Agent4"],
        "Agent4": ["Agent5"],
        "Agent5": ["WorkflowComplete"],
        "WorkflowComplete": []
    })

    manager.add_workflow("chat_engineering_flow", {
        "WorkflowStart": ["Agent3"],
        "Agent3": ["Agent2"],
        "Agent2": ["Agent4"],
        "Agent4": ["Agent5"],
        "Agent5": ["WorkflowComplete"],
        "WorkflowComplete": []
    })

    # Set the router workflow to be active initially
    manager.switch_workflow("chat_router")

    return chat_agents


def main_terminal():
    """Run original terminal version"""
    print("🖥️  Running Terminal Mode")
    result = create_base_workflow_manager()
    if result is None:
        return
    
    manager, _ = result
    create_terminal_workflows(manager)
    
    # Start with the switch agent (original behavior)
    initial_input = "Explain the science of photosynthesis."
    manager.run_workflow(start_agent_name="SwitchAgent", input_data=initial_input)


def main_chat(enable_events=True):
    """Run chat-enhanced version"""
    print("💬 Running Chat-Enhanced Mode")
    result = create_base_workflow_manager()
    if result is None:
        return None
    
    manager, core_agents = result
    create_terminal_workflows(manager)  # Keep original workflows for compatibility
    chat_agents = create_chat_workflows(manager)  # Add chat workflows
    
    if enable_events:
        # Enable chat integration
        manager.enable_chat_integration(chat_event_bus)
        
        # Subscribe to chat events for terminal display (optional)
        def display_chat_message(event):
            data = event.data
            print(f"💬 {data['sender']}: {data['content']}")
        
        chat_event_bus.subscribe("message", display_chat_message)
    
    return manager


def main_chat_demo():
    """Run a demo of the chat-enhanced workflow"""
    manager = main_chat(enable_events=True)
    if manager is None:
        return
    
    print("🚀 Starting chat-enhanced workflow demo...")
    initial_input = "Explain the science of photosynthesis."
    
    # Run workflow with chat integration
    manager.run_workflow(start_agent_name="WorkflowStart", input_data=initial_input)


def main():
    """Main entry point - runs terminal version by default"""
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "--chat":
            main_chat_demo()
        elif mode == "--terminal":
            main_terminal()
        else:
            print("Usage: python enhanced_main.py [--terminal|--chat]")
            print("Default: terminal mode")
            main_terminal()
    else:
        main_terminal()


if __name__ == "__main__":
    main()
