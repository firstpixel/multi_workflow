#!/usr/bin/env python3
"""
Test script to verify VS Code debugging is using the correct Python interpreter.
Set a breakpoint on line 12 and run with F5 in VS Code.
"""

import sys
import os

def main():
    print("=== Python Interpreter Debug Test ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Check if we're in virtual environment
    if hasattr(sys, 'base_prefix'):
        is_venv = sys.prefix != sys.base_prefix
        print(f"Virtual environment active: {is_venv}")
        if is_venv:
            print(f"Virtual env prefix: {sys.prefix}")
            print(f"Base prefix: {sys.base_prefix}")
    
    # Test ollama import (should work in venv, fail in system Python)
    try:
        import ollama
        print("✅ Successfully imported ollama - Virtual environment is working!")
        print(f"Ollama module location: {ollama.__file__}")
    except ImportError as e:
        print(f"❌ Failed to import ollama: {e}")
        print("This means VS Code is NOT using the virtual environment")
    
    print("\n=== Instructions ===")
    print("1. Set a breakpoint on this line (line 32)")
    print("2. Press F5 to debug")  # <- Set breakpoint here
    print("3. Check the debug console output")
    print("4. If you see the venv path above, debugging is working correctly!")

if __name__ == "__main__":
    main()
