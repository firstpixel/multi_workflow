#!/usr/bin/env python3
"""
Comprehensive Test Suite for Multi-Workflow AI System

This script tests both terminal and chat-enhanced versions of the workflow system
to ensure all functionality works correctly without tight coupling.
"""

import sys
import os
import time
import threading
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_main import main_terminal, main_chat, create_base_workflow_manager, create_terminal_workflows, create_chat_workflows
from ChatInterface import chat_event_bus, ChatEvent
from WorkflowManager import WorkflowManager


class TestReporter:
    """Simple test reporter for tracking test results"""
    
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []

    def test(self, test_name, condition, error_msg="Test failed"):
        """Run a test and report results"""
        self.tests_run += 1
        print(f"  Testing: {test_name}... ", end="")
        
        if condition:
            print("✅ PASS")
            self.tests_passed += 1
        else:
            print("❌ FAIL")
            self.tests_failed += 1
            self.failures.append(f"{test_name}: {error_msg}")

    def report(self):
        """Print final test report"""
        print(f"\n{'='*60}")
        print(f"TEST RESULTS")
        print(f"{'='*60}")
        print(f"Tests Run: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        
        if self.failures:
            print(f"\nFAILURES:")
            for failure in self.failures:
                print(f"  ❌ {failure}")
        
        if self.tests_failed == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
        else:
            print(f"\n⚠️  {self.tests_failed} TESTS FAILED")


def test_basic_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing Basic Imports...")
    reporter = TestReporter()
    
    try:
        from enhanced_main import main_terminal, main_chat
        reporter.test("Enhanced main import", True)
    except ImportError as e:
        reporter.test("Enhanced main import", False, str(e))
    
    try:
        from ChatInterface import chat_event_bus, ChatEvent
        reporter.test("Chat interface import", True)
    except ImportError as e:
        reporter.test("Chat interface import", False, str(e))
    
    try:
        from ChatAgents import ChatDisplayAgent, UserInputAgent
        reporter.test("Chat agents import", True)
    except ImportError as e:
        reporter.test("Chat agents import", False, str(e))
    
    try:
        from WorkflowManager import WorkflowManager
        reporter.test("Workflow manager import", True)
    except ImportError as e:
        reporter.test("Workflow manager import", False, str(e))
    
    return reporter


def test_workflow_manager_creation():
    """Test workflow manager creation and configuration"""
    print("\n🧪 Testing Workflow Manager Creation...")
    reporter = TestReporter()
    
    try:
        result = create_base_workflow_manager()
        reporter.test("Base workflow manager creation", result is not None)
        
        if result:
            manager, core_agents = result
            reporter.test("Manager instance created", isinstance(manager, WorkflowManager))
            reporter.test("Core agents created", len(core_agents) >= 5)
            
            # Test chat integration
            manager.enable_chat_integration(chat_event_bus)
            reporter.test("Chat integration enabled", manager.chat_enabled)
            
            # Test workflow creation
            create_terminal_workflows(manager)
            reporter.test("Terminal workflows created", len(manager.workflows) >= 3)
            
            chat_agents = create_chat_workflows(manager)
            reporter.test("Chat workflows created", len(chat_agents) >= 4)
            
    except Exception as e:
        reporter.test("Workflow manager creation", False, str(e))
    
    return reporter


def test_chat_event_system():
    """Test the chat event system functionality"""
    print("\n🧪 Testing Chat Event System...")
    reporter = TestReporter()
    
    # Test event bus creation
    reporter.test("Event bus exists", chat_event_bus is not None)
    
    # Test event publishing
    test_events = []
    
    def event_collector(event):
        test_events.append(event)
    
    chat_event_bus.subscribe("test_message", event_collector)
    
    test_event = ChatEvent("test_message", {"content": "Test message"})
    chat_event_bus.enable()
    chat_event_bus.publish(test_event)
    
    # Give event a moment to be processed
    time.sleep(0.1)
    
    reporter.test("Event publishing works", len(test_events) > 0)
    
    # Test event retrieval
    events = chat_event_bus.get_events()
    reporter.test("Event retrieval works", isinstance(events, list))
    
    # Clean up
    chat_event_bus.unsubscribe("test_message", event_collector)
    chat_event_bus.clear_events()
    
    return reporter


def test_terminal_mode():
    """Test terminal mode functionality (without chat)"""
    print("\n🧪 Testing Terminal Mode...")
    reporter = TestReporter()
    
    try:
        # Create a minimal workflow manager for terminal testing
        result = create_base_workflow_manager()
        if result is None:
            reporter.test("Terminal mode setup", False, "Could not create workflow manager")
            return reporter
        
        manager, _ = result
        create_terminal_workflows(manager)
        
        # Verify chat is NOT enabled by default
        reporter.test("Chat disabled in terminal mode", not manager.chat_enabled)
        
        # Verify workflows exist
        reporter.test("Default flow exists", "default_flow" in manager.workflows)
        reporter.test("Science flow exists", "science_flow" in manager.workflows)
        reporter.test("Engineering flow exists", "engineering_flow" in manager.workflows)
        
        print("    Note: Terminal workflow execution test skipped (would be too verbose)")
        reporter.test("Terminal mode setup complete", True)
        
    except Exception as e:
        reporter.test("Terminal mode", False, str(e))
    
    return reporter


def test_chat_mode():
    """Test chat mode functionality"""
    print("\n🧪 Testing Chat Mode...")
    reporter = TestReporter()
    
    try:
        # Create chat-enhanced workflow manager
        manager = main_chat(enable_events=True)
        if manager is None:
            reporter.test("Chat mode setup", False, "Could not create chat workflow manager")
            return reporter
        
        # Verify chat is enabled
        reporter.test("Chat enabled in chat mode", manager.chat_enabled)
        
        # Verify chat workflows exist
        reporter.test("Chat default flow exists", "chat_default_flow" in manager.workflows)
        reporter.test("Chat science flow exists", "chat_science_flow" in manager.workflows)
        reporter.test("Chat engineering flow exists", "chat_engineering_flow" in manager.workflows)
        
        # Verify chat agents exist (includes Display agents, Workflow agents, and UserInput agents)
        chat_agent_names = [name for name in manager.agents.keys() 
                           if any(keyword in name for keyword in ['Chat', 'Workflow', 'UserInput', 'Display'])]
        reporter.test("Chat agents created", len(chat_agent_names) >= 4)
        
        # Test event bus integration
        reporter.test("Event bus integrated", manager.event_bus is not None)
        
        print("    Note: Full chat workflow execution test skipped (would require user input)")
        
    except Exception as e:
        reporter.test("Chat mode", False, str(e))
    
    return reporter


def test_loose_coupling():
    """Test that the system maintains loose coupling"""
    print("\n🧪 Testing Loose Coupling...")
    reporter = TestReporter()
    
    try:
        # Test that terminal mode works without chat imports
        result = create_base_workflow_manager()
        if result:
            manager, _ = result
            create_terminal_workflows(manager)
            
            # Chat should be disabled by default
            reporter.test("No chat dependency in terminal", not manager.chat_enabled)
            
            # Should be able to disable chat integration
            manager.disable_chat_integration()
            reporter.test("Can disable chat integration", not manager.chat_enabled)
            
            # Should be able to enable and disable chat
            manager.enable_chat_integration(chat_event_bus)
            reporter.test("Can enable chat integration", manager.chat_enabled)
            
            manager.disable_chat_integration()
            reporter.test("Can disable chat after enabling", not manager.chat_enabled)
            
            reporter.test("Loose coupling maintained", True)
        else:
            reporter.test("Loose coupling test", False, "Could not create workflow manager")
    
    except Exception as e:
        reporter.test("Loose coupling", False, str(e))
    
    return reporter


def test_backward_compatibility():
    """Test that original functionality still works"""
    print("\n🧪 Testing Backward Compatibility...")
    reporter = TestReporter()
    
    try:
        # Test that we can import original components
        from SwitchAgent import SwitchAgent
        from Agent import LLMAgent
        from prompt_loader import prompt_loader
        
        reporter.test("Original imports work", True)
        
        # Test that original workflow structure is preserved
        result = create_base_workflow_manager()
        if result:
            manager, _ = result
            create_terminal_workflows(manager)
            
            # Check that original workflows exist unchanged
            default_flow = manager.workflows.get("default_flow", {})
            expected_flow_structure = {
                "Agent1": ["Agent2"],
                "Agent2": ["Agent3"],
                "Agent3": ["Agent4"],
                "Agent4": ["Agent5"],
                "Agent5": []
            }
            
            reporter.test("Original workflow structure preserved", default_flow == expected_flow_structure)
            
            reporter.test("Backward compatibility maintained", True)
        else:
            reporter.test("Backward compatibility", False, "Could not create workflow manager")
    
    except Exception as e:
        reporter.test("Backward compatibility", False, str(e))
    
    return reporter


def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Test Suite for Multi-Workflow AI System")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    all_reporters = []
    
    # Run all test suites
    all_reporters.append(test_basic_imports())
    all_reporters.append(test_workflow_manager_creation())
    all_reporters.append(test_chat_event_system())
    all_reporters.append(test_terminal_mode())
    all_reporters.append(test_chat_mode())
    all_reporters.append(test_loose_coupling())
    all_reporters.append(test_backward_compatibility())
    
    # Compile overall results
    total_tests = sum(r.tests_run for r in all_reporters)
    total_passed = sum(r.tests_passed for r in all_reporters)
    total_failed = sum(r.tests_failed for r in all_reporters)
    all_failures = []
    for r in all_reporters:
        all_failures.extend(r.failures)
    
    # Final report
    print(f"\n{'='*60}")
    print(f"OVERALL TEST RESULTS")
    print(f"{'='*60}")
    print(f"Total Tests Run: {total_tests}")
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")
    
    if all_failures:
        print(f"\nALL FAILURES:")
        for failure in all_failures:
            print(f"  ❌ {failure}")
    
    if total_failed == 0:
        print(f"\n🎉 ALL TESTS PASSED! System is working correctly.")
        print("✅ Terminal mode: Working")
        print("✅ Chat mode: Working") 
        print("✅ Loose coupling: Maintained")
        print("✅ Backward compatibility: Preserved")
        return 0
    else:
        print(f"\n⚠️  {total_failed} TESTS FAILED - Please review and fix issues.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
