from Agent import LLMAgent

class SwitchAgent(LLMAgent):
    def __init__(self, name, model_config, system=None, retry_limit=1, workflow_config=None):
        super().__init__(name, model_config, system=system or "", retry_limit=retry_limit)
        self.workflow_config = workflow_config or {}
        self.available_flows = []
        self.keyword_mapping = {}
        self.default_flow = "default_flow"
        
        # Override llm_fn to return just the output value, not stringified dict
        self.llm_fn = self._switch_agent_llm_fn
        
        # Configure from workflow_config if provided
        if workflow_config:
            self.available_flows = workflow_config.get("available_flows", [])
            self.keyword_mapping = workflow_config.get("keyword_mapping", {})
            self.default_flow = workflow_config.get("default_flow", "default_flow")
            self.use_llm_decision = workflow_config.get("use_llm_decision", False)

    def _switch_agent_llm_fn(self, input_data):
        """Custom LLM function for SwitchAgent that returns just the output value"""
        if isinstance(input_data, dict) and "output" in input_data:
            return input_data["output"]
        return str(input_data)

    def set_available_flows(self, flows):
        """Set available flows dynamically from WorkflowManager"""
        self.available_flows = flows
        # Don't overwrite the system prompt - it should be set properly from the prompt file
        # The available flows are already included in the prompt file content
    
    def execute(self, user_input):
        print(f" #################################### SwitchAgent deciding on workflow with input: {user_input}")
        
        # If configured to use LLM for decision making
        if self.workflow_config.get("use_llm_decision", False) and self.system:
            try:
                # Use the parent LLM execution to make the decision
                llm_result = super().execute(user_input)
                if llm_result["success"]:
                    raw_output = llm_result["output"]
                    # Handle case where output might be a string or needs extraction
                    if isinstance(raw_output, str):
                        flow_name = raw_output.strip()
                    else:
                        flow_name = str(raw_output).strip()
                    # Validate that the suggested flow exists
                    if flow_name in self.available_flows:
                        return {
                            "output": user_input,  # Keep original input for workflow continuation
                            "success": True, 
                            "switch_flow": flow_name,
                            "display_output": f"� LLM Decision: Routing '{user_input}' to '{flow_name}'",
                            "llm_decision": flow_name
                        }
                    else:
                        print(f" #################################### LLM suggested invalid flow '{flow_name}', using default")
                        return {
                            "output": user_input,  # Keep original input for workflow continuation
                            "success": True, 
                            "switch_flow": self.default_flow,
                            "display_output": f"� LLM Decision: Invalid flow '{flow_name}', using default '{self.default_flow}'",
                            "llm_decision": f"invalid:{flow_name}→{self.default_flow}"
                        }
            except Exception as e:
                print(f" #################################### Error in LLM decision: {e}, falling back to keyword matching")
                # Continue to fallback logic, will be handled below
        
        # Fallback to keyword-based matching
        user_input_lower = user_input.lower()
        
        # Check configured keyword mappings first
        for keyword, flow in self.keyword_mapping.items():
            if keyword.lower() in user_input_lower:
                return {
                    "output": user_input,  # Keep original input
                    "success": True, 
                    "switch_flow": flow,
                    "display_output": f"🔍 Keyword Match: Found '{keyword}' → Routing to '{flow}'",
                    "decision_method": "keyword"
                }
        
        # Default hardcoded fallbacks (for backward compatibility)
        if "science" in user_input_lower:
            return {
                "output": user_input,
                "success": True, 
                "switch_flow": self.default_flow,
                "display_output": f"🔍 Keyword Match: Found 'science' → Using default '{self.default_flow}'",
                "decision_method": "keyword_fallback"
            }
        elif "build" in user_input_lower or "engineering" in user_input_lower:
            # Check if we have engineering flow configured, otherwise use default
            if "chat_engineering_flow" in self.available_flows:
                return {
                    "output": user_input,
                    "success": True, 
                    "switch_flow": "chat_engineering_flow",
                    "display_output": f"🔍 Keyword Match: Found 'build/engineering' → Routing to 'chat_engineering_flow'",
                    "decision_method": "keyword_fallback"
                }
            elif "engineering_flow" in self.available_flows:
                return {
                    "output": user_input,
                    "success": True, 
                    "switch_flow": "engineering_flow",
                    "display_output": f"🔍 Keyword Match: Found 'build/engineering' → Routing to 'engineering_flow'",
                    "decision_method": "keyword_fallback"
                }
            else:
                return {
                    "output": user_input,
                    "success": True, 
                    "switch_flow": self.default_flow,
                    "display_output": f"🔍 Keyword Match: Found 'build/engineering' but no engineering flow available → Using default '{self.default_flow}'",
                    "decision_method": "keyword_fallback"
                }
        else:
            return {
                "output": user_input,
                "success": True, 
                "switch_flow": self.default_flow,
                "display_output": f"🔍 No Keywords Matched → Using default flow '{self.default_flow}'",
                "decision_method": "default"
            }
