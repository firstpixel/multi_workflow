from Agent import LLMAgent

class SwitchAgent(LLMAgent):
    def __init__(self, name, model_config, system=None, retry_limit=1, workflow_config=None):
        super().__init__(name, model_config, system, retry_limit)
        self.workflow_config = workflow_config or {}
        self.available_flows = []
        self.keyword_mapping = {}
        self.default_flow = "default_flow"
        
        # Configure from workflow_config if provided
        if workflow_config:
            self.available_flows = workflow_config.get("available_flows", [])
            self.keyword_mapping = workflow_config.get("keyword_mapping", {})
            self.default_flow = workflow_config.get("default_flow", "default_flow")
            self.use_llm_decision = workflow_config.get("use_llm_decision", False)
    
    def set_available_flows(self, flows):
        """Set available flows dynamically from WorkflowManager"""
        self.available_flows = flows
        # Update system prompt with current flows
        if self.system and "available flows:" in self.system.lower():
            flows_list = "\n".join(self.available_flows)
            # Update the system prompt to include current flows
            base_prompt = "Decide which flow to follow based on the topic.\nrespond only the flow name, here is list of available flows:"
            self.system = f"{base_prompt}\n{flows_list}"
    
    def execute(self, user_input):
        print(f" #################################### SwitchAgent deciding on workflow with input: {user_input}")
        
        # If configured to use LLM for decision making
        if self.workflow_config.get("use_llm_decision", False) and self.system:
            try:
                # Use the parent LLM execution to make the decision
                llm_result = super().execute(user_input)
                if llm_result["success"]:
                    flow_name = llm_result["output"].strip()
                    # Validate that the suggested flow exists
                    if flow_name in self.available_flows:
                        return {"output": user_input, "success": True, "switch_flow": flow_name}
                    else:
                        print(f" #################################### LLM suggested invalid flow '{flow_name}', using default")
                        return {"output": user_input, "success": True, "switch_flow": self.default_flow}
            except Exception as e:
                print(f" #################################### Error in LLM decision: {e}, falling back to keyword matching")
        
        # Fallback to keyword-based matching
        user_input_lower = user_input.lower()
        
        # Check configured keyword mappings first
        for keyword, flow in self.keyword_mapping.items():
            if keyword.lower() in user_input_lower:
                return {"output": user_input, "success": True, "switch_flow": flow}
        
        # Default hardcoded fallbacks (for backward compatibility)
        if "science" in user_input_lower:
            return {"output": user_input, "success": True, "switch_flow": "science_flow"}
        elif "build" in user_input_lower or "engineering" in user_input_lower:
            return {"output": user_input, "success": True, "switch_flow": "engineering_flow"}
        else:
            return {"output": user_input, "success": True, "switch_flow": self.default_flow}
