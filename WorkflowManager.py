class WorkflowManager:
    def __init__(self):
        self.agents = {}                # All available agents (shared across flows)
        self.connections = {}           # Main workflow connections
        self.pending_inputs = {}
        self.workflows = {}             # Multiple subflows by name
        self.chat_enabled = False       # NEW: Flag for chat integration
        self.event_bus = None          # NEW: Optional event bus

    def enable_chat_integration(self, event_bus):
        """Enable chat integration with event bus"""
        self.chat_enabled = True
        self.event_bus = event_bus
        if hasattr(event_bus, 'enable'):
            event_bus.enable()

    def disable_chat_integration(self):
        """Disable chat integration"""
        self.chat_enabled = False
        if self.event_bus and hasattr(self.event_bus, 'disable'):
            self.event_bus.disable()
        self.event_bus = None

    def _extract_content(self, data):
        """Extract clean content from various data formats"""
        if data is None:
            return "None"
        
        # If it's already a string, check for problematic formats
        if isinstance(data, str):
            # Handle "TOOL EXECUTED {'output': '...'}" format
            if data.startswith("TOOL EXECUTED  "):
                # Extract the part after "TOOL EXECUTED  "
                remaining = data[15:]  # len("TOOL EXECUTED  ") = 15
                # If the remaining part is a dictionary string representation, try to extract 'output' value
                if remaining.startswith("{'output': "):
                    try:
                        # Find the 'output' value by manual parsing since it might contain nested quotes
                        # Look for the pattern {'output': '...'} and extract what's between the quotes
                        start_idx = remaining.find("'output': '") + len("'output': '")
                        if start_idx > len("'output': '") - 1:  # Found the pattern
                            # Find the end - look for the last quote before the closing brace
                            # We need to handle escaped quotes properly
                            end_idx = remaining.rfind("'}")
                            if end_idx > start_idx:
                                content = remaining[start_idx:end_idx]
                                # Unescape any escaped quotes
                                content = content.replace("\\'", "'").replace("\\n", "\n")
                                return content
                    except Exception as e:
                        # If parsing fails, fall back to returning the remaining string
                        pass
                # If it's not a dictionary format or parsing failed, return as-is
                return remaining
            
            # Handle direct "{'output': '...'}" format (when LLM returns this as a string)
            elif data.startswith("{'output': "):
                try:
                    # Find the 'output' value by manual parsing
                    start_idx = data.find("'output': '") + len("'output': '")
                    if start_idx > len("'output': '") - 1:  # Found the pattern
                        # Find the end - look for the last quote before the closing brace
                        end_idx = data.rfind("'}")
                        if end_idx > start_idx:
                            content = data[start_idx:end_idx]
                            # Unescape any escaped quotes
                            content = content.replace("\\'", "'").replace("\\n", "\n")
                            return content
                except Exception as e:
                    # If parsing fails, return the original string
                    pass
            
            return data
        
        # If it's a dictionary with 'output' key, extract that
        if isinstance(data, dict):
            if 'output' in data:
                # Recursively extract content from nested 'output' keys
                return self._extract_content(data['output'])
            else:
                # For other dictionaries, convert to string but clean it up
                return str(data)
        
        # For other types, convert to string
        return str(data)

    def _publish_agent_event(self, event_type, agent_name, data):
        """Helper to publish agent events to chat"""
        if self.chat_enabled and self.event_bus:
            try:
                # Import here to avoid circular imports
                from ChatInterface import ChatEvent
                self.event_bus.publish(ChatEvent("message", {
                    "sender": agent_name,
                    "content": data,
                    "type": event_type
                }))
            except ImportError:
                # Gracefully handle missing chat interface
                pass

    def add_agent(self, agent, next_agents=None):
        self.agents[agent.name] = agent
        self.connections[agent.name] = next_agents if next_agents else []
        self.pending_inputs[agent.name] = []
        
        # If this is a SwitchAgent, configure it with available workflows
        if hasattr(agent, 'set_available_flows'):
            agent.set_available_flows(list(self.workflows.keys()))

    def add_workflow(self, workflow_name, agent_sequence: dict):
        """
        Adds a named subflow (workflow) with agent connections.
        `agent_sequence` is a dict: {agent_name: [next_agent_names]}
        """
        self.workflows[workflow_name] = agent_sequence
        for agent_name, next_agents in agent_sequence.items():
            self.connections[agent_name] = next_agents if next_agents else []
        
        # Update any SwitchAgents with the new workflow list
        for agent in self.agents.values():
            if hasattr(agent, 'set_available_flows'):
                agent.set_available_flows(list(self.workflows.keys()))

    def switch_workflow(self, new_workflow_name):
        """Replaces the current connection map with a new subflow."""
        if new_workflow_name not in self.workflows:
            print(f" #################################### Workflow '{new_workflow_name}' not found!")
            return False
        print(f" #################################### Switching to workflow: {new_workflow_name}")
        self.connections = self.workflows[new_workflow_name]
        return True

    def run_workflow(self, start_agent_name, input_data):
        input_queue = [(start_agent_name, input_data)]
        
        # NEW: Announce workflow start
        if self.chat_enabled:
            # Don't truncate input preview - show full input
            input_preview = str(input_data)
            self._publish_agent_event("workflow_start", "System", f"🚀 Starting workflow with: {input_preview}")
        
        while input_queue:
            current_agent_name, input_data = input_queue.pop(0)
            current_agent = self.agents.get(current_agent_name)
            if current_agent is None:
                error_msg = f"Agent {current_agent_name} not found!"
                print(f" #################################### {error_msg}")
                if self.chat_enabled:
                    self._publish_agent_event("system_error", "System", f"❌ {error_msg}")
                continue

            # NEW: Announce agent processing (only for non-chat agents to avoid noise)
            # Removed the "Processing..." message - we only want to show actual outputs

            combined_input = current_agent.receive_input(input_data)
            if combined_input is None:
                wait_msg = f"{current_agent_name} is waiting for more inputs..."
                print(f" #################################### {wait_msg}")
                
                # NEW: Show waiting status in chat
                if self.chat_enabled:
                    self._publish_agent_event("agent_waiting", current_agent_name, f"⏳ Waiting for more inputs...")
                continue

            result = current_agent.run_with_retries(combined_input)
            if result["success"]:
                current_agent.reset_retry()

                # NEW: Show agent output in chat (all agents now since no DisplayAgents to handle them)
                if self.chat_enabled and not current_agent_name.startswith(('Chat', 'Workflow', 'UserInput')):
                    # Check if agent has a special display_output (like SwitchAgent decision)
                    if "display_output" in result:
                        display_data = self._extract_content(result["display_output"])
                    else:
                        display_data = self._extract_content(result["output"])
                    self._publish_agent_event("agent_output", current_agent_name, f"✅ {display_data}")

                # Special case: Agent can return `{"switch_flow": "flow_name"}`
                if "switch_flow" in result:
                    if self.switch_workflow(result["switch_flow"]):
                        # NEW: Announce workflow switch
                        if self.chat_enabled:
                            self._publish_agent_event("workflow_switch", "System", f"🔀 Switched to workflow: {result['switch_flow']}")
                        
                        # Restart from first agent in the new flow
                        first_agent = list(self.workflows[result["switch_flow"]].keys())[0]
                        # Extract clean content before passing to the new workflow
                        clean_output = self._extract_content(result["output"])
                        input_queue = [(first_agent, clean_output)]
                    continue

                next_agents = self.connections.get(current_agent_name, [])
                for next_agent in next_agents:
                    input_queue.append((next_agent, result["output"]))
            else:
                error_msg = f"❌ {current_agent_name} failed after {current_agent.retry_count} retries"
                print(f" #################################### {current_agent_name} failed after {current_agent.retry_count} retries.")
                
                # NEW: Show failure in chat
                if self.chat_enabled:
                    self._publish_agent_event("agent_error", current_agent_name, error_msg)
        
        # NEW: Announce workflow completion
        if self.chat_enabled:
            self._publish_agent_event("workflow_complete", "System", "🎉 Workflow execution completed!")
