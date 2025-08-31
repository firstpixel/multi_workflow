from SwitchAgent import SwitchAgent
from WorkflowManager import WorkflowManager
from Agent import LLMAgent
from prompt_loader import prompt_loader



def custom_validate(result):
    # Access the "output" key in the result dictionary and check if "valid" is present
    output = result.get("output", "")
    return "?" in output.lower() if output else False

def custom_llm_fn(input_data):
    """Custom LLM function that uses a different API or logic."""
    print(f" #################################### TOOL EXECUTED  Custom LLM called with input: {input_data}")
    return f"TOOL EXECUTED  {input_data}"




def main():
    manager = WorkflowManager()

    # Load prompts from files
    try:
        print("Loading prompts from files...")
        available_prompts = prompt_loader.list_available_prompts()
        print(f"Available prompts: {available_prompts}")
        
        prompt1 = prompt_loader.load_prompt("prompt1_breakdown")
        prompt2 = prompt_loader.load_prompt("prompt2_detailed")
        prompt3 = prompt_loader.load_prompt("prompt3_simple")
        prompt4 = prompt_loader.load_prompt("prompt4_refine")
        prompt5 = prompt_loader.load_prompt("prompt5_summary")
        switch_prompt = prompt_loader.load_prompt("switch_agent")
        
        print("All prompts loaded successfully!")
    except FileNotFoundError as e:
        print(f"Error loading prompts: {e}")
        return

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
        "use_llm_decision": True,  # Use LLM to make decisions instead of just keywords
        "keyword_mapping": {       # Fallback keyword mappings
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

    # Register agents
    for agent in [agent1, agent2, agent3, agent4, agent5, switch_agent]:
        manager.add_agent(agent)

    # Add multiple workflows
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

    # Start with the switch agent
    initial_input = "Explain the science of photosynthesis."
    manager.run_workflow(start_agent_name="SwitchAgent", input_data=initial_input)

if __name__ == "__main__":
    main()
