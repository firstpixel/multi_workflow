#!/usr/bin/env python3
"""
Debug helper script to verify which Python interpreter is being used.
Run this to check if the debugger is using the correct virtual environment.
"""

import sys
import os

print("=" * 60)
print("PYTHON INTERPRETER DEBUG INFO")
print("=" * 60)

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Python version info: {sys.version_info}")

print(f"\nCurrent working directory: {os.getcwd()}")

print(f"\nPython path (first 5 entries):")
for i, path in enumerate(sys.path[:5]):
    print(f"  {i}: {path}")

print(f"\nVirtual environment check:")
virtual_env = os.environ.get('VIRTUAL_ENV')
if virtual_env:
    print(f"  VIRTUAL_ENV: {virtual_env}")
else:
    print("  VIRTUAL_ENV: Not set")

# Check if we're in a virtual environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print(f"  Running in virtual environment: YES")
    print(f"  sys.prefix: {sys.prefix}")
    if hasattr(sys, 'base_prefix'):
        print(f"  sys.base_prefix: {sys.base_prefix}")
else:
    print(f"  Running in virtual environment: NO")
    print(f"  sys.prefix: {sys.prefix}")

print(f"\nTrying to import ollama...")
try:
    import ollama
    print(f"  ✅ ollama imported successfully")
    print(f"  ollama module location: {ollama.__file__}")
except ImportError as e:
    print(f"  ❌ Failed to import ollama: {e}")

print(f"\nExpected venv path: {os.path.join(os.getcwd(), 'venv', 'bin', 'python')}")
print(f"Current executable matches expected: {sys.executable == os.path.join(os.getcwd(), 'venv', 'bin', 'python')}")

print("=" * 60)
