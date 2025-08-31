from Agent import LLMAgent
import json
import ollama

class PromptAgent(LLMAgent):
    """
    An agent that creates or modifies prompts for other agents based on user input.
    This agent can analyze the user's request and generate appropriate system prompts
    for downstream agents to use.
    """
    
    def __init__(self, name, model_config, system=None, retry_limit=3, 
                 prompt_templates=None, target_agents=None):
        super().__init__(name, model_config, system, retry_limit)
        self.prompt_templates = prompt_templates or {}
        self.target_agents = target_agents or {}
        
    def execute(self, user_input):
        """
        Analyze user input and generate/modify prompts for other agents.
        Returns both the original input and the generated prompt modifications.
        """
        print(f" #################################### {self.name}: Analyzing input for prompt generation: {user_input}")
        
        # Prepare the full prompt for prompt generation
        full_prompt = f"""
Based on the user's request, generate appropriate system prompts or modifications for the following agents.

User Request: {user_input}

Available Agent Types and Their Purposes:
{self._get_agent_descriptions()}

Please provide:
1. Analysis of the user's intent
2. Recommended prompt modifications for each relevant agent
3. Any new system prompts that should be created

Format your response as JSON with the following structure:
{{
    "analysis": "Your analysis of the user's intent",
    "prompt_modifications": {{
        "agent_name": "new or modified system prompt",
        ...
    }},
    "workflow_suggestions": "Any workflow adjustments needed"
}}
"""
        
        messages = [
            {"role": "system", "content": self.system},
            {"role": "user", "content": full_prompt}
        ]
        
        try:
            response = ollama.chat(
                model=self.model_config["model"],
                stream=False,
                messages=messages,
                options={
                    "temperature": self.model_config["temperature"],
                    "top_p": self.model_config["top_p"],
                    "frequency_penalty": self.model_config["frequency_penalty"],
                    "presence_penalty": self.model_config["presence_penalty"]
                }
            )
            output = response['message']['content'].strip()
            print(f" #################################### {self.name}: Generated prompt analysis - {output}")
            
            # Try to parse as JSON, fall back to plain text if needed
            try:
                prompt_data = json.loads(output)
            except json.JSONDecodeError:
                prompt_data = {
                    "analysis": "Could not parse structured response",
                    "prompt_modifications": {},
                    "raw_output": output
                }
            
            # Return both original input and prompt modifications
            result = {
                "original_input": user_input,
                "prompt_data": prompt_data,
                "output": output,
                "prompt_modifications": prompt_data.get("prompt_modifications", {})
            }
            
            success = self.validate({"output": output})
            print(f" #################################### {self.name}: validate - {success}")
            
            return {"output": result, "success": success}
            
        except Exception as e:
            print(f" #################################### {self.name}: Error during prompt generation - {e}")
            return {"output": None, "success": False}
    
    def _get_agent_descriptions(self):
        """Get descriptions of available agents for prompt generation context."""
        descriptions = []
        for agent_name, description in self.target_agents.items():
            descriptions.append(f"- {agent_name}: {description}")
        return "\n".join(descriptions) if descriptions else "No specific agent descriptions provided"


class EnhancedLLMAgent(LLMAgent):
    """
    Enhanced LLM Agent that can receive and use dynamically generated prompts,
    while preserving the original input throughout the workflow.
    """
    
    def __init__(self, name, model_config, system="", retry_limit=3, expected_inputs=1, validate_fn=None, llm_fn=None):
        super().__init__(name, model_config, validate_fn, llm_fn, system, "", "", retry_limit, expected_inputs)
        self.original_system = system  # Keep backup of original system prompt
        self.input_history = []        # Track input history
        
    def update_system_prompt(self, new_system_prompt):
        """Update the system prompt dynamically."""
        print(f" #################################### {self.name}: Updating system prompt")
        self.system = new_system_prompt
        
    def restore_original_prompt(self):
        """Restore the original system prompt."""
        self.system = self.original_system
        
    def execute(self, user_input):
        """Enhanced execute that handles input preservation and prompt modifications."""
        
        # Handle different input types
        if isinstance(user_input, dict):
            # Check if this is from a PromptAgent
            if "original_input" in user_input and "prompt_modifications" in user_input:
                return self._execute_with_prompt_modification(user_input)
            # Check if this is preserved input format
            elif "original_input" in user_input and "processed_output" in user_input:
                return self._execute_with_preserved_input(user_input)
        
        # Standard execution with input preservation
        return self._execute_standard_with_preservation(user_input)
    
    def _execute_with_prompt_modification(self, input_data):
        """Execute when receiving input from a PromptAgent with prompt modifications."""
        original_input = input_data["original_input"]
        prompt_modifications = input_data["prompt_modifications"]
        
        # Apply prompt modification if this agent is targeted
        if self.name in prompt_modifications:
            old_system = self.system
            self.update_system_prompt(prompt_modifications[self.name])
            print(f" #################################### {self.name}: Applied new system prompt from PromptAgent")
            
            # Execute with the original input but new prompt
            result = self._execute_standard_with_preservation(original_input)
            
            # Restore original prompt for future use
            self.system = old_system
            
            # Preserve the prompt modification information
            if result["success"] and isinstance(result["output"], dict):
                result["output"]["applied_prompt_modification"] = True
                result["output"]["modified_prompt"] = prompt_modifications[self.name]
            
            return result
        else:
            # No modification for this agent, use original input
            return self._execute_standard_with_preservation(original_input)
    
    def _execute_with_preserved_input(self, input_data):
        """Execute with already preserved input format."""
        original_input = input_data["original_input"]
        processed_output = input_data["processed_output"]
        
        print(f" #################################### {self.name}: Executing with preserved input")
        print(f" #################################### Original: {original_input}")
        print(f" #################################### Previous: {processed_output}")
        
        # Use the processed output for this agent's work
        result = super().execute(processed_output)
        
        if result["success"]:
            # Preserve the original input in the output
            result["output"] = {
                "original_input": original_input,
                "processed_output": result["output"],
                "agent_name": self.name,
                "input_history": self.input_history + [processed_output]
            }
        
        return result
    
    def _execute_standard_with_preservation(self, user_input):
        """Standard execution with input preservation."""
        print(f" #################################### {self.name}: Executing with input: {user_input}")
        
        # Track input history
        self.input_history.append(user_input)
        
        # Call parent execute method
        result = super().execute(user_input)
        
        if result["success"]:
            # Wrap output to preserve original input
            result["output"] = {
                "original_input": user_input,
                "processed_output": result["output"],
                "agent_name": self.name,
                "input_history": [user_input]
            }
        
        return result


class InputPreservationManager:
    """
    Utility class to help manage input preservation across workflow chains.
    """
    
    @staticmethod
    def extract_original_input(data):
        """Extract the original input from preserved data structure."""
        if isinstance(data, dict) and "original_input" in data:
            return data["original_input"]
        return data
    
    @staticmethod
    def extract_processed_output(data):
        """Extract the most recent processed output."""
        if isinstance(data, dict) and "processed_output" in data:
            return data["processed_output"]
        return data
    
    @staticmethod
    def get_input_history(data):
        """Get the full input history if available."""
        if isinstance(data, dict) and "input_history" in data:
            return data["input_history"]
        return []
    
    @staticmethod
    def create_preserved_input(original_input, processed_output, agent_name=None):
        """Create a properly formatted preserved input structure."""
        return {
            "original_input": original_input,
            "processed_output": processed_output,
            "agent_name": agent_name,
            "input_history": [original_input] if not isinstance(original_input, dict) else 
                           original_input.get("input_history", []) + [processed_output]
        }
