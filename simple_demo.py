#!/usr/bin/env python3

from Agent import LLMAgent
from WorkflowManager import WorkflowManager
from prompt_loader import prompt_loader
import json

class SimplePromptAgent(LLMAgent):
    """A simpler version of PromptAgent for demonstration purposes."""
    
    def execute(self, user_input):
        """Analyze user input and create prompt suggestions."""
        print(f" #################################### {self.name}: Creating prompts for: {user_input}")
        
        # Analyze the input and create prompt modifications
        analysis = self._analyze_input(user_input)
        
        # Return both original input and prompt modifications
        result = {
            "original_input": user_input,
            "prompt_modifications": analysis,
            "analysis": f"Generated custom prompts for: {user_input}"
        }
        
        return {"output": result, "success": True}
    
    def _analyze_input(self, user_input):
        """Simple analysis that creates basic prompt modifications."""
        input_lower = user_input.lower()
        
        prompt_mods = {}
        
        if "quantum" in input_lower or "science" in input_lower:
            prompt_mods["Processor"] = "You are a science educator. Explain complex scientific concepts clearly and use analogies to help understanding."
        elif "story" in input_lower or "creative" in input_lower:
            prompt_mods["Processor"] = "You are a creative writer. Focus on narrative, character development, and engaging storytelling."
        elif "economic" in input_lower or "business" in input_lower:
            prompt_mods["Processor"] = "You are a business analyst. Provide data-driven insights and consider economic implications."
        else:
            prompt_mods["Processor"] = "You are a helpful assistant. Provide clear, informative responses."
        
        if "student" in input_lower or "high school" in input_lower:
            prompt_mods["Processor"] += " Use simple language appropriate for students."
        
        return prompt_mods


class InputPreservingAgent(LLMAgent):
    """Agent that preserves original input while processing."""
    
    def execute(self, user_input):
        """Execute while preserving input context."""
        
        # Handle different input formats
        if isinstance(user_input, dict):
            if "original_input" in user_input and "prompt_modifications" in user_input:
                return self._execute_with_prompt_modification(user_input)
            elif "original_input" in user_input:
                return self._execute_with_preserved_input(user_input)
        
        # Standard execution with preservation
        return self._execute_with_preservation(user_input)
    
    def _execute_with_prompt_modification(self, input_data):
        """Execute when receiving prompt modifications."""
        original_input = input_data["original_input"]
        prompt_modifications = input_data.get("prompt_modifications", {})
        
        print(f" #################################### {self.name}: Received original input: {original_input}")
        print(f" #################################### {self.name}: Received prompt modifications: {prompt_modifications}")
        
        # Apply prompt modification if available for this agent
        if self.name in prompt_modifications:
            old_system = self.system
            self.system = prompt_modifications[self.name]
            print(f" #################################### {self.name}: Applied custom prompt: {self.system}")
        
        # Execute with original input
        result = super().execute(original_input)
        
        # Restore original system if modified
        if self.name in prompt_modifications:
            self.system = old_system
        
        # Preserve input in output
        if result["success"]:
            result["output"] = {
                "original_input": original_input,
                "processed_output": result["output"],
                "agent_name": self.name,
                "used_custom_prompt": self.name in prompt_modifications
            }
        
        return result
    
    def _execute_with_preserved_input(self, input_data):
        """Execute with already preserved input."""
        original_input = input_data["original_input"]
        processed_output = input_data.get("processed_output", original_input)
        
        print(f" #################################### {self.name}: Processing with preserved context")
        print(f" #################################### Original: {original_input}")
        print(f" #################################### Previous: {processed_output}")
        
        # Process the previous output
        result = super().execute(str(processed_output))
        
        if result["success"]:
            result["output"] = {
                "original_input": original_input,
                "processed_output": result["output"],
                "agent_name": self.name,
                "input_chain": input_data.get("input_chain", []) + [processed_output]
            }
        
        return result
    
    def _execute_with_preservation(self, user_input):
        """Standard execution with input preservation."""
        print(f" #################################### {self.name}: Starting preservation chain with: {user_input}")
        
        result = super().execute(user_input)
        
        if result["success"]:
            result["output"] = {
                "original_input": user_input,
                "processed_output": result["output"],
                "agent_name": self.name,
                "input_chain": [user_input]
            }
        
        return result


def demo_simple_prompt_and_preservation():
    """Demonstrate the core concepts with a simpler implementation."""
    
    print("=" * 80)
    print("SIMPLE DEMONSTRATION: PROMPT MODIFICATION + INPUT PRESERVATION")
    print("=" * 80)
    
    manager = WorkflowManager()
    
    # Model configuration
    model_config = {
        "model": "llama3.2:1b",
        "temperature": 0.7,
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    
    # Create agents
    prompt_agent = SimplePromptAgent(
        name="PromptCreator",
        model_config=model_config,
        system="You create prompts for other agents",
        retry_limit=1
    )
    
    processor = InputPreservingAgent(
        name="Processor", 
        model_config=model_config,
        system="You are a general processing agent",
        retry_limit=1
    )
    
    finalizer = InputPreservingAgent(
        name="Finalizer",
        model_config=model_config, 
        system="You finalize and summarize results",
        retry_limit=1
    )
    
    # Register agents
    for agent in [prompt_agent, processor, finalizer]:
        manager.add_agent(agent)
    
    # Create workflow
    manager.add_workflow("prompt_demo", {
        "PromptCreator": ["Processor"],
        "Processor": ["Finalizer"], 
        "Finalizer": []
    })
    
    print("\n📋 Workflow: PromptCreator → Processor → Finalizer")
    print("   • PromptCreator analyzes input and creates custom prompts")
    print("   • Processor uses custom prompt and preserves original input")
    print("   • Finalizer receives both original and processed data")
    
    # Test scenarios
    test_inputs = [
        "Explain quantum computing for high school students",
        "Write a creative story about robots",
        "Analyze the economic impact of AI"
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {test_input}")
        print(f"{'='*60}")
        
        manager.run_workflow("PromptCreator", test_input)
        
        print(f"\n✅ Test {i} completed!")
    
    print("\n" + "=" * 80)
    print("🎉 DEMONSTRATION COMPLETE!")
    
    print("\n✅ Successfully Demonstrated:")
    print("   1. ✅ Prompt Agent: Creates custom prompts based on user input")
    print("   2. ✅ Prompt Modification: Agents use custom prompts dynamically")
    print("   3. ✅ Input Preservation: Original input maintained through workflow")
    print("   4. ✅ Context Tracking: Full processing history available")
    
    print("\n🔧 Key Features:")
    print("   • Dynamic prompt generation based on content analysis")
    print("   • Automatic prompt application to downstream agents") 
    print("   • Original input preserved throughout the entire workflow")
    print("   • Processing history tracked for full context")
    print("   • Flexible architecture supports various workflow patterns")


if __name__ == "__main__":
    demo_simple_prompt_and_preservation()
