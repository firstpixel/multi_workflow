# Tests

This folder contains test files for the multi-workflow AI system.

## Running Tests

Run tests from the project root directory:

```bash
# Run a specific test
python tests/test_comprehensive.py
python tests/test_chat_improvements.py

# Run all tests (if you have a test runner)
python -m pytest tests/
```

## Test Files

- `test_comprehensive.py` - Comprehensive test suite for both terminal and chat versions
- `test_chat_improvements.py` - Tests for chat interface improvements  
- `test_streamlit_events.py` - Tests for Streamlit event processing
- `test_switch_logic.py` - Logic tests for SwitchAgent routing

## Requirements

All tests require the project dependencies to be installed and the virtual environment to be activated.
