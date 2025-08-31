"""
Chat Interface Event System for Multi-Workflow AI

This module provides an event-driven chat interface system that enables
communication between workflow components and chat frontends without
creating tight coupling.
"""

import queue
import time
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List


class ChatEvent:
    """Represents a chat event (message, user input request, etc.)"""
    
    def __init__(self, event_type: str, data: Any, timestamp: Optional[datetime] = None):
        self.event_type = event_type  # 'message', 'user_input_request', 'workflow_complete'
        self.data = data
        self.timestamp = timestamp or datetime.now()
        self.id = f"{event_type}_{int(time.time() * 1000)}"


class ChatEventBus:
    """Event bus for communication between workflow and chat interface"""
    
    def __init__(self):
        self.subscribers = {}
        self.event_queue = queue.Queue()
        self.user_input_queue = queue.Queue()
        self.waiting_for_input = False
        self.current_input_request = None
        self.enabled = False  # Chat integration is disabled by default

    def enable(self):
        """Enable chat integration"""
        self.enabled = True

    def disable(self):
        """Disable chat integration"""
        self.enabled = False

    def is_enabled(self) -> bool:
        """Check if chat integration is enabled"""
        return self.enabled

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to specific event types"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe from specific event types"""
        if event_type in self.subscribers:
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)

    def publish(self, event: ChatEvent):
        """Publish an event to all subscribers"""
        if not self.enabled:
            return  # Don't publish events if chat is disabled
            
        self.event_queue.put(event)
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event callback: {e}")

    def request_user_input(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Request input from user and wait for response"""
        if not self.enabled:
            # Fallback to terminal input if chat is disabled
            return input(f"\n{prompt}\n> ")
            
        self.waiting_for_input = True
        self.current_input_request = {
            "prompt": prompt,
            "context": context or {},
            "timestamp": datetime.now()
        }
        
        # Publish input request event
        self.publish(ChatEvent("user_input_request", self.current_input_request))
        
        # Wait for user response
        while self.waiting_for_input:
            try:
                user_response = self.user_input_queue.get(timeout=0.1)
                self.waiting_for_input = False
                self.current_input_request = None
                return user_response
            except queue.Empty:
                continue
        
        return ""

    def provide_user_input(self, user_input: str):
        """Provide user input response"""
        self.user_input_queue.put(user_input)

    def get_events(self) -> List[ChatEvent]:
        """Get all pending events"""
        events = []
        while not self.event_queue.empty():
            try:
                events.append(self.event_queue.get_nowait())
            except queue.Empty:
                break
        return events

    def clear_events(self):
        """Clear all pending events"""
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break


# Global event bus instance
chat_event_bus = ChatEventBus()


def create_message_event(sender: str, content: str, message_type: str = "info") -> ChatEvent:
    """Helper function to create a standardized message event"""
    return ChatEvent("message", {
        "sender": sender,
        "content": content,
        "type": message_type,
        "timestamp": datetime.now()
    })


def create_workflow_event(event_type: str, workflow_name: Optional[str] = None, data: Any = None) -> ChatEvent:
    """Helper function to create workflow-related events"""
    return ChatEvent(event_type, {
        "workflow": workflow_name,
        "data": data,
        "timestamp": datetime.now()
    })
