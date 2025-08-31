#!/usr/bin/env python3
"""
Demo Script for Multi-Workflow AI System

This script demonstrates both terminal and chat modes to showcase
the functionality and loose coupling of the system.
"""

import sys
import time
from enhanced_main import main_terminal, main_chat_demo
from ChatInterface import chat_event_bus


def demo_terminal_mode():
    """Demonstrate the terminal mode"""
    print("🖥️  TERMINAL MODE DEMONSTRATION")
    print("="*50)
    print("Running the original terminal workflow...")
    print("This mode works exactly as before, with no chat dependencies.")
    print()
    
    # Run terminal mode
    main_terminal()
    
    print("\n✅ Terminal mode completed successfully!")


def demo_chat_mode():
    """Demonstrate the chat mode"""
    print("\n💬 CHAT MODE DEMONSTRATION")
    print("="*50)
    print("Running the chat-enhanced workflow...")
    print("This mode adds chat events while preserving all original functionality.")
    print()
    
    # Run chat mode
    main_chat_demo()
    
    print("\n✅ Chat mode completed successfully!")


def show_system_info():
    """Show information about the system"""
    print("🤖 MULTI-WORKFLOW AI SYSTEM")
    print("="*60)
    print("This system demonstrates:")
    print("  ✅ Loose coupling between terminal and chat modes")
    print("  ✅ Backward compatibility with existing workflows")
    print("  ✅ Event-driven chat integration")
    print("  ✅ No breaking changes to core functionality")
    print("  ✅ Full response display without truncation")
    print("  ✅ Clean chat interface without noise messages")
    print()
    print("Recent Improvements:")
    print("  • Full agent responses shown in chat (no truncation)")
    print("  • Removed 'Processing...' messages for cleaner interface")
    print("  • Better user experience with complete content display")
    print("  • Focus on actual agent outputs and results")
    print("  ✅ No breaking changes to core functionality")
    print()
    print("Available modes:")
    print("  1. Terminal Mode: Original functionality (--terminal)")
    print("  2. Chat Mode: Enhanced with chat events (--chat)")
    print("  3. Streamlit Web UI: Browser-based interface")
    print()


def main():
    """Main demo function"""
    show_system_info()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "--terminal":
            demo_terminal_mode()
        elif mode == "--chat":
            demo_chat_mode()
        elif mode == "--both":
            demo_terminal_mode()
            demo_chat_mode()
        elif mode == "--info":
            print("🔧 TECHNICAL DETAILS")
            print("="*50)
            print("Key Components:")
            print("  • WorkflowManager: Core workflow execution engine")
            print("  • ChatInterface: Event-driven chat communication system")
            print("  • ChatAgents: Specialized agents for chat interaction")
            print("  • Enhanced Main: Unified entry point for both modes")
            print()
            print("Architecture Benefits:")
            print("  • Zero breaking changes to existing code")
            print("  • Optional chat integration via event bus")
            print("  • Modular design allows easy extension")
            print("  • Clear separation of concerns")
        else:
            print(f"❌ Unknown mode: {mode}")
            print("Usage: python demo.py [--terminal|--chat|--both|--info]")
    else:
        print("Usage: python demo.py [--terminal|--chat|--both|--info]")
        print()
        print("Examples:")
        print("  python demo.py --terminal    # Run terminal mode only")
        print("  python demo.py --chat        # Run chat mode only") 
        print("  python demo.py --both        # Run both modes")
        print("  python demo.py --info        # Show technical details")
        print()
        print("For Streamlit web interface:")
        print("  streamlit run streamlit_app.py")


if __name__ == "__main__":
    main()
