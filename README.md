# Multi-Workflow AI Agent System

A flexible multi-agent workflow system with dynamic prompt loading, configurable agent flows, intelligent prompt generation, and input preservation capabilities.

## 🚀 Latest Features

### ✨ **Configurable SwitchAgent** (NEW!)
- **Intelligent Flow Selection**: Uses LLM-powered decision making instead of hardcoded keywords
- **Dynamic Flow Discovery**: Automatically detects available workflows from WorkflowManager
- **Custom Keyword Mapping**: Define precise routing rules for specific use cases
- **Backward Compatible**: Still supports original hardcoded patterns as fallback

### ✨ **Prompt Agent** (NEW!)
- **Dynamic Prompt Generation**: Creates custom system prompts for other agents based on user input
- **Intelligent Analysis**: Understands user intent, domain, audience, and complexity requirements
- **Automatic Application**: Generated prompts are automatically applied to downstream agents
- **Context-Aware**: Considers factors like target audience and desired output format

### ✨ **Input Preservation System** (NEW!)
- **Original Input Tracking**: Maintains user's original request throughout the entire workflow
- **Processing History**: Tracks full transformation chain for complete audit trail
- **Context Preservation**: Agents can access both original and processed inputs
- **Flexible Data Structures**: Supports complex data while remaining backward compatible

## Project Structure

```
multi_workflow/
├── Agent.py                    # Base agent classes (Agent, LLMAgent)
├── SwitchAgent.py             # Configurable agent for intelligent workflow switching
├── PromptAgent.py             # NEW: Prompt generation and input preservation agents
├── WorkflowManager.py         # Enhanced workflow management with flow discovery
├── main.py                    # Main application with configurable examples
├── simple_demo.py             # NEW: Simple demonstration of prompt generation and preservation
├── demo_dynamic_workflows.py  # NEW: Advanced workflow configuration demonstration
├── test_configurable_switch.py # NEW: Test suite for configurable SwitchAgent
├── prompt_loader.py           # Prompt loading utilities
├── prompt_manager.py          # Prompt management utility
├── prompts/                   # Directory containing prompt files
│   ├── prompt1_breakdown.txt
│   ├── prompt2_detailed.txt
│   ├── prompt3_simple.txt
│   ├── prompt4_refine.txt
│   ├── prompt5_summary.txt
│   ├── switch_agent.txt
│   └── prompt_agent.txt       # NEW: System prompt for PromptAgent
├── CONFIGURABLE_SWITCH_SOLUTION.md  # NEW: Documentation for SwitchAgent
├── PROMPT_AGENT_SOLUTION.md         # NEW: Documentation for Prompt Agent features
└── README.md                        # This file (updated!)
```

## Features

### Core System
- **Multi-Agent System**: Define multiple LLM agents with different roles and prompts
- **Dynamic Workflows**: Switch between different agent flows based on input content
- **Prompt Management**: Store prompts in separate files for easy maintenance
- **Configurable Models**: Support for different Ollama models and configurations
- **Retry Logic**: Built-in retry mechanism for failed agent executions
- **Custom Validation**: Define custom validation functions for agent outputs

### Advanced Features (NEW!)

#### 🧠 **Intelligent Workflow Routing**
- **Configurable SwitchAgent**: LLM-powered workflow selection instead of hardcoded keywords
- **Dynamic Flow Discovery**: Automatically detects and configures available workflows
- **Custom Keyword Mapping**: Define precise routing rules for specific domains
- **Fallback Mechanisms**: Multiple layers of decision-making for robust routing

#### 🎯 **Dynamic Prompt Engineering**
- **PromptAgent**: Analyzes user input and generates custom prompts for other agents
- **Context-Aware Generation**: Considers domain, audience, complexity, and output format
- **Automatic Prompt Application**: Seamless integration with existing workflow structure
- **Quality Optimization**: Task-specific prompts improve agent performance

#### 📋 **Input Preservation & Context Management**
- **Original Input Tracking**: Maintains user's original request throughout workflows
- **Processing History**: Complete audit trail of all transformations
- **Context Accessibility**: Agents can access both original and processed inputs
- **Data Structure Flexibility**: Supports both simple strings and complex data objects

#### 🔄 **Enhanced Workflow Capabilities**
- **Adaptive Workflows**: Automatically optimize for specific tasks and requirements
- **Context Continuity**: Never lose original intent during processing chains
- **Quality Improvement**: Better outputs through specialized, generated prompts
- **Traceability**: Full visibility from original request to final output

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install ollama
   ```

2. **Ensure Ollama is running** with the required models:
   ```bash
   ollama list
   ```

3. **Run the main application**:
   ```bash
   python main.py
   ```

## 🎮 New Demonstrations & Examples

### Basic Prompt Agent Demo
```bash
python simple_demo.py
```
Demonstrates:
- Dynamic prompt generation based on user input
- Input preservation throughout workflow chains
- Custom prompt application to agents

### Advanced Configurable Workflows
```bash
python demo_dynamic_workflows.py
```
Demonstrates:
- Dynamic workflow creation and management
- Intelligent SwitchAgent with custom configurations
- Multiple workflow patterns (creative, emergency, finance flows)

### SwitchAgent Testing
```bash
python test_configurable_switch.py
```
Demonstrates:
- Configurable keyword mapping
- LLM-powered flow selection
- Dynamic flow discovery

## 💡 Usage Examples

### Example 1: Educational Content with Custom Prompts
```python
# Input: "Explain quantum computing for high school students"
# PromptAgent generates: "You are a science educator. Use simple language appropriate for students."
# Result: Age-appropriate explanation with analogies
```

### Example 2: Creative Writing with Context Preservation
```python
# Input: "Write a creative story about robots"
# PromptAgent generates: "You are a creative writer. Focus on narrative and character development."
# Original request preserved through story creation → editing → summarization
```

### Example 3: Business Analysis with Specialized Prompts
```python
# Input: "Analyze the economic impact of AI"
# PromptAgent generates: "You are a business analyst. Provide data-driven insights."
# Result: Comprehensive analysis with recommendations and data
```

## Prompt Management

### Using the Prompt Loader

The `prompt_loader.py` module provides easy access to prompt files:

```python
from prompt_loader import prompt_loader

# Load a single prompt
prompt = prompt_loader.load_prompt("prompt1_breakdown")

# Load all prompts
all_prompts = prompt_loader.load_all_prompts()

# List available prompts
available = prompt_loader.list_available_prompts()
```

### Using the Prompt Manager Utility

The `prompt_manager.py` script provides command-line tools for managing prompts:

```bash
# List all available prompts
python prompt_manager.py list

# View a specific prompt
python prompt_manager.py view prompt1_breakdown

# Create a new prompt
python prompt_manager.py create my_new_prompt

# Edit an existing prompt
python prompt_manager.py edit prompt1_breakdown

# Delete a prompt
python prompt_manager.py delete old_prompt
```

### Adding New Prompts

1. **Method 1: Direct file creation**
   ```bash
   echo "Your prompt content here" > prompts/my_prompt.txt
   ```

2. **Method 2: Using the prompt manager**
   ```bash
   python prompt_manager.py create my_prompt
   # Then enter your prompt content
   ```

3. **Method 3: Programmatically**
   ```python
   from prompt_loader import PromptLoader
   loader = PromptLoader()
   # Create file manually, then load it
   content = loader.load_prompt("my_prompt")
   ```

## Agent Workflows

The system supports multiple predefined workflows:

### Default Flow
```
Agent1 (breakdown) → Agent2 (detailed) → Agent3 (simple) → Agent4 (refine) → Agent5 (summary)
```

### Science Flow
```
Agent2 (detailed) → Agent4 (refine) → Agent5 (summary)
```

### Engineering Flow
```
Agent3 (simple) → Agent2 (detailed) → Agent4 (refine) → Agent5 (summary)
```

## Configuration

### Model Configuration

Edit the model configurations in `main.py`:

```python
model_config = {
    "model": "llama3.2:1b",
    "temperature": 0.7,
    "top_p": 0.9,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}
```

### Agent Configuration

Each agent can be configured with:
- `name`: Unique identifier
- `model_config`: Model parameters
- `system`: System prompt (loaded from prompts/)
- `validate_fn`: Custom validation function
- `llm_fn`: Custom LLM processing function
- `retry_limit`: Maximum retry attempts
- `expected_inputs`: Number of inputs the agent expects

## Workflow Switching

### Legacy SwitchAgent (Backward Compatible)
The basic `SwitchAgent` supports simple keyword matching:
- Contains "science" → `science_flow`
- Contains "build" → `engineering_flow`
- Default → `default_flow`

### NEW: Configurable SwitchAgent 🚀

The enhanced `SwitchAgent` supports advanced configuration:

```python
switch_config = {
    "use_llm_decision": True,          # Enable AI-powered routing
    "keyword_mapping": {               # Custom keyword rules
        "machine learning": "science_flow",
        "data analysis": "science_flow", 
        "software": "engineering_flow",
        "programming": "engineering_flow",
        "urgent": "emergency_flow",
        "creative": "creative_flow"
    },
    "default_flow": "standard_flow"    # Fallback flow
}

switch_agent = SwitchAgent(
    name="SwitchAgent",
    model_config=model_config,
    system=switch_prompt,
    workflow_config=switch_config
)
```

#### Features:
- **LLM-Powered Decisions**: Uses AI to understand context and intent
- **Dynamic Flow Discovery**: Automatically detects available workflows
- **Custom Keyword Mapping**: Define precise routing rules
- **Multiple Fallback Layers**: LLM → Keywords → Hardcoded → Default
- **Easy Configuration**: Add new flows without code changes

## NEW: Prompt Agent System 🎯

### Basic Usage

```python
from PromptAgent import PromptAgent, EnhancedLLMAgent

# Create a PromptAgent that generates custom prompts
prompt_agent = PromptAgent(
    name="PromptAgent",
    model_config=model_config,
    system=prompt_agent_system,
    target_agents={
        "Analyzer": "Analyzes and breaks down topics",
        "Writer": "Creates detailed content",
        "Summarizer": "Creates concise summaries"
    }
)

# Create agents that can use dynamic prompts and preserve input
analyzer = EnhancedLLMAgent(
    name="Analyzer",
    model_config=model_config,
    system="Default analysis prompt"
)
```

### Workflow Example

```python
# Workflow: PromptAgent → Analyzer → Writer → Summarizer
manager.add_workflow("intelligent_flow", {
    "PromptAgent": ["Analyzer"],
    "Analyzer": ["Writer"],
    "Writer": ["Summarizer"],
    "Summarizer": []
})

# Input: "Explain quantum computing for high school students"
# PromptAgent generates custom prompts for each agent
# Original input preserved throughout the chain
manager.run_workflow("PromptAgent", user_input)
```

## NEW: Input Preservation 📋

### Automatic Input Preservation

All `EnhancedLLMAgent` instances automatically preserve input context:

```python
{
    "original_input": "User's original request",
    "processed_output": "Agent's result",
    "agent_name": "ProcessingAgent",
    "input_history": ["step1", "step2", "step3"]
}
```

### Benefits:
- **Traceability**: Full audit trail from request to result
- **Context Access**: Agents can reference original intent
- **Quality Assurance**: Verify transformations maintain original meaning
- **Debugging**: Easy to track where issues occur in the chain

## Custom Functions

### Validation Function Example
```python
def custom_validate(result):
    output = result.get("output", "")
    return "?" in output.lower() if output else False
```

### Custom LLM Function Example
```python
def custom_llm_fn(input_data):
    print(f"Custom processing: {input_data}")
    return f"Processed: {input_data}"
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'ollama'**
   ```bash
   pip install ollama
   ```

2. **Model not found errors**
   ```bash
   ollama pull llama3.2:1b
   ollama pull gemma3:latest
   ```

3. **Prompt file not found**
   - Check that the prompt file exists in the `prompts/` directory
   - Use `python prompt_manager.py list` to see available prompts
   - Ensure the filename matches exactly (case-sensitive)

4. **Agent waiting for inputs**
   - Check that the agent's `expected_inputs` matches the workflow configuration
   - Verify the workflow connections in `main.py`

### NEW Feature Issues

5. **PromptAgent validation errors**
   - Ensure the `prompt_agent.txt` system prompt exists
   - Check that target_agents configuration is properly set
   - Verify JSON parsing in PromptAgent responses

6. **Input preservation not working**
   - Make sure you're using `EnhancedLLMAgent` instead of `LLMAgent`
   - Check that the input structure includes preservation fields
   - Verify the `receive_input` method handles complex data structures

7. **SwitchAgent configuration issues**
   - Ensure `workflow_config` is properly formatted as a dictionary
   - Check that flow names in keyword mapping match actual workflow names
   - Verify that `available_flows` are being set correctly

8. **LLM decision-making failures**
   - Check that the model has sufficient context length for complex prompts
   - Verify that the system prompt for SwitchAgent includes available flows
   - Ensure fallback mechanisms are working (keywords → hardcoded → default)

### Debug Tips

- **Enable detailed logging**: Add print statements to track data flow
- **Test individual components**: Use the demo scripts to isolate issues
- **Check data structures**: Verify that complex objects are properly formatted
- **Validate configurations**: Ensure all required fields are present in config dictionaries

### Performance Optimization

- **Model Selection**: Use appropriate model sizes for your use case
- **Prompt Length**: Keep generated prompts concise but informative
- **Workflow Design**: Minimize unnecessary agent chains
- **Caching**: Consider caching frequently used prompt generations

## Contributing

### Adding New Features

1. **Add new prompt files** to the `prompts/` directory
2. **Create new agent types** by extending `Agent` or `LLMAgent`
3. **Implement custom workflow patterns** in new demonstration files
4. **Update agent configurations** in `main.py` or create new demo files
5. **Test with existing demo scripts** to ensure compatibility

### Development Guidelines

- **Use EnhancedLLMAgent** for new agents that need input preservation
- **Configure SwitchAgent** with appropriate keyword mappings for new domains
- **Create PromptAgent configurations** for specialized prompt generation
- **Document new workflows** in demonstration files
- **Test backward compatibility** with existing workflows

### File Organization

- **Core Logic**: `Agent.py`, `WorkflowManager.py`, `SwitchAgent.py`
- **New Features**: `PromptAgent.py` for prompt generation and input preservation
- **Demonstrations**: `simple_demo.py`, `demo_dynamic_workflows.py`, `test_configurable_switch.py`
- **Documentation**: `*.md` files for feature explanations
- **Prompts**: `prompts/` directory for all system prompts

### Testing New Features

1. **Run basic demos**: `python simple_demo.py`
2. **Test configurations**: `python test_configurable_switch.py`
3. **Try advanced features**: `python demo_dynamic_workflows.py`
4. **Verify original functionality**: `python main.py`

### Best Practices

- **Preserve backward compatibility** when modifying core classes
- **Use descriptive names** for new workflows and agents
- **Document configuration options** in code comments
- **Create comprehensive examples** for new features
- **Test edge cases** with various input types and configurations

## License

This project is open source and available under the MIT License.
