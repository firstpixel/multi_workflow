class WorkflowManager:
    def __init__(self):
        self.agents = {}                # All available agents (shared across flows)
        self.connections = {}           # Main workflow connections
        self.pending_inputs = {}
        self.workflows = {}             # Multiple subflows by name

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
        while input_queue:
            current_agent_name, input_data = input_queue.pop(0)
            current_agent = self.agents.get(current_agent_name)
            if current_agent is None:
                print(f" #################################### Agent {current_agent_name} not found!")
                continue

            combined_input = current_agent.receive_input(input_data)
            if combined_input is None:
                print(f" #################################### {current_agent_name} is waiting for more inputs...")
                continue

            result = current_agent.run_with_retries(combined_input)
            if result["success"]:
                current_agent.reset_retry()

                # Special case: Agent can return `{"switch_flow": "flow_name"}`
                if "switch_flow" in result:
                    if self.switch_workflow(result["switch_flow"]):
                        # Restart from first agent in the new flow
                        first_agent = list(self.workflows[result["switch_flow"]].keys())[0]
                        input_queue = [(first_agent, result["output"])]
                    continue

                next_agents = self.connections.get(current_agent_name, [])
                for next_agent in next_agents:
                    input_queue.append((next_agent, result["output"]))
            else:
                print(f" #################################### {current_agent_name} failed after {current_agent.retry_count} retries.")
