# VS Code Python Interpreter Fix

## The issue you're experiencing is common - VS Code is not automatically picking up the virtual environment for debugging.

## Here's how to fix it:

### Method 1: Manually Select Python Interpreter (RECOMMENDED)

1. **Open VS Code in your project folder**
2. **Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)**
3. **Type: "Python: Select Interpreter"**
4. **Select "Python: Select Interpreter" from the dropdown**
5. **Choose the interpreter from the list that shows:**
   ```
   ./venv/bin/python (Recommended)
   Python 3.11.12 64-bit ('venv': venv)
   ```
6. **If you don't see it in the list, click "Enter interpreter path..." and browse to:**
   ```
   /Users/gilbeyruth/AIProjects/multi_workflow/venv/bin/python
   ```

### Method 2: Force Reload VS Code Window

1. **After selecting the interpreter, press `Ctrl+Shift+P` again**
2. **Type: "Developer: Reload Window"**
3. **Hit Enter to reload VS Code**

### Method 3: Verify the Selection

1. **Run the debug helper script first:**
   ```bash
   # In terminal (to verify venv works)
   ./venv/bin/python debug_python.py
   ```

2. **Then debug the same script in VS Code:**
   - Set a breakpoint in `debug_python.py`
   - Press F5 and select "Python Debugger: Current File"
   - Check the output in the debug console

### Method 4: Check Bottom Status Bar

Look at the bottom-left of VS Code window. You should see:
```
🐍 Python 3.11.12 64-bit ('venv': venv)
```

If it shows something else (like system Python), click on it and select the venv interpreter.

## What to Expect After Fix:

When debugging, you should see the virtual environment Python path in the debug console:
```
Python executable: /Users/gilbeyruth/AIProjects/multi_workflow/venv/bin/python
```

Instead of:
```
Python executable: /opt/homebrew/bin/python3
```

## If It Still Doesn't Work:

1. **Close VS Code completely**
2. **Delete `.vscode/settings.json` temporarily**
3. **Reopen VS Code**
4. **Manually select interpreter again**
5. **The settings.json will be recreated with correct paths**
