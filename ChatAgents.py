"""
Chat Agents for Multi-Workflow AI System

This module provides specialized agents that enable chat interface integration
without modifying the core workflow system. These agents can be inserted
into any workflow to add chat functionality.
"""

from Agent import Agent
from ChatInterface import chat_event_bus, ChatEvent, create_message_event
from typing import Dict, Any


class ChatDisplayAgent(Agent):
    """Agent that sends messages to the chat interface without modifying data flow"""
    
    def __init__(self, name: str, message_prefix: str = "", message_suffix: str = "", expected_inputs: int = 1):
        super().__init__(name, expected_inputs)
        self.message_prefix = message_prefix
        self.message_suffix = message_suffix

    def execute(self, input_data: str) -> Dict[str, Any]:
        """Process input and send to chat, then pass through unchanged"""
        
        # Format message for chat display
        if isinstance(input_data, dict):
            display_data = input_data.get('output', str(input_data))
        else:
            display_data = str(input_data)
            
        # Don't truncate - show full message
        message = f"{self.message_prefix}{display_data}{self.message_suffix}"
        
        # Send to chat interface
        chat_event_bus.publish(create_message_event(
            sender=self.name,
            content=message,
            message_type="agent_output"
        ))
        
        # Pass through unchanged for workflow continuation
        return {
            "success": True,
            "output": input_data
        }


class UserInputAgent(Agent):
    """Agent that requests input from user via chat interface"""
    
    def __init__(self, name: str, prompt_message: str = "Please provide your input:", 
                 show_context: bool = True, expected_inputs: int = 1):
        super().__init__(name, expected_inputs)
        self.prompt_message = prompt_message
        self.show_context = show_context

    def execute(self, input_data: str) -> Dict[str, Any]:
        """Request user input and wait for response"""
        
        # Send context to chat if enabled and available
        if self.show_context:
            if isinstance(input_data, dict):
                context_message = input_data.get('output', 'Processing workflow...')
            else:
                context_message = str(input_data)
            
            # Don't truncate context - show full context
            chat_event_bus.publish(create_message_event(
                sender=self.name,
                content=f"📋 Context: {context_message}",
                message_type="context"
            ))
        
        # Request user input
        context_data = {
            "previous_output": input_data,
            "agent": self.name
        }
        
        user_response = chat_event_bus.request_user_input(
            prompt=self.prompt_message,
            context=context_data
        )
        
        # Send user response to chat for display
        chat_event_bus.publish(create_message_event(
            sender="User",
            content=user_response,
            message_type="user_input"
        ))
        
        return {
            "success": True,
            "output": user_response
        }


class WorkflowStartAgent(Agent):
    """Agent that announces workflow start in chat"""
    
    def __init__(self, name: str = "WorkflowStart", expected_inputs: int = 1):
        super().__init__(name, expected_inputs)

    def execute(self, input_data: str) -> Dict[str, Any]:
        """Announce workflow start"""
        
        # Don't truncate input preview - show full input
        input_preview = str(input_data)
        
        chat_event_bus.publish(create_message_event(
            sender=self.name,
            content=f"🚀 Starting workflow with input: {input_preview}",
            message_type="workflow_start"
        ))
        
        return {
            "success": True,
            "output": input_data
        }


class WorkflowCompleteAgent(Agent):
    """Agent that announces workflow completion in chat"""
    
    def __init__(self, name: str = "WorkflowComplete", show_final_output: bool = True, expected_inputs: int = 1):
        super().__init__(name, expected_inputs)
        self.show_final_output = show_final_output

    def execute(self, input_data: str) -> Dict[str, Any]:
        """Announce workflow completion"""
        
        chat_event_bus.publish(create_message_event(
            sender=self.name,
            content="✅ Workflow completed successfully!",
            message_type="workflow_complete"
        ))
        
        if self.show_final_output:
            # Don't truncate final output - show complete result
            final_output = str(input_data)
                
            chat_event_bus.publish(create_message_event(
                sender=self.name,
                content=f"📄 Final Output: {final_output}",
                message_type="final_output"
            ))
        
        chat_event_bus.publish(ChatEvent("workflow_complete", {
            "final_output": input_data,
            "status": "success"
        }))
        
        return {
            "success": True,
            "output": input_data
        }


class ChatNotificationAgent(Agent):
    """Generic agent for sending custom notifications to chat"""
    
    def __init__(self, name: str, notification_message: str, notification_type: str = "info", expected_inputs: int = 1):
        super().__init__(name, expected_inputs)
        self.notification_message = notification_message
        self.notification_type = notification_type

    def execute(self, input_data: str) -> Dict[str, Any]:
        """Send custom notification to chat"""
        
        chat_event_bus.publish(create_message_event(
            sender=self.name,
            content=self.notification_message,
            message_type=self.notification_type
        ))
        
        return {
            "success": True,
            "output": input_data
        }
