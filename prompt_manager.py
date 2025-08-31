#!/usr/bin/env python3
"""
Prompt Management Utility

This script provides utilities for managing prompt files in the prompts/ directory.
You can use it to view, create, edit, and manage prompt files easily.
"""

import os
import sys
from prompt_loader import PromptLoader


class PromptManager:
    def __init__(self, prompts_dir="prompts"):
        self.loader = PromptLoader(prompts_dir)
        self.prompts_dir = prompts_dir
    
    def list_prompts(self):
        """List all available prompts."""
        prompts = self.loader.list_available_prompts()
        if not prompts:
            print("No prompts found in the prompts directory.")
            return
        
        print(f"\nAvailable prompts in '{self.prompts_dir}':")
        print("=" * 40)
        for i, prompt_name in enumerate(prompts, 1):
            print(f"{i:2d}. {prompt_name}")
        print()
    
    def view_prompt(self, prompt_name):
        """View the content of a specific prompt."""
        try:
            content = self.loader.load_prompt(prompt_name)
            print(f"\nContent of '{prompt_name}':")
            print("=" * 40)
            print(content)
            print("=" * 40)
        except FileNotFoundError:
            print(f"Error: Prompt '{prompt_name}' not found.")
    
    def create_prompt(self, prompt_name, content):
        """Create a new prompt file."""
        if not prompt_name.endswith('.txt'):
            prompt_name += '.txt'
        
        file_path = os.path.join(self.prompts_dir, prompt_name)
        
        if os.path.exists(file_path):
            response = input(f"Prompt '{prompt_name}' already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Operation cancelled.")
                return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            print(f"Prompt '{prompt_name}' created successfully.")
        except IOError as e:
            print(f"Error creating prompt file: {e}")
    
    def edit_prompt(self, prompt_name):
        """Edit an existing prompt using the default text editor."""
        if not prompt_name.endswith('.txt'):
            prompt_name += '.txt'
        
        file_path = os.path.join(self.prompts_dir, prompt_name)
        
        if not os.path.exists(file_path):
            print(f"Error: Prompt '{prompt_name}' not found.")
            return
        
        # Try to open with the system's default editor
        import subprocess
        try:
            if sys.platform.startswith('darwin'):  # macOS
                subprocess.call(['open', '-t', file_path])
            elif sys.platform.startswith('linux'):  # Linux
                subprocess.call(['xdg-open', file_path])
            elif sys.platform.startswith('win'):    # Windows
                subprocess.call(['notepad', file_path])
            else:
                print(f"Please edit the file manually: {file_path}")
        except Exception as e:
            print(f"Could not open editor: {e}")
            print(f"Please edit the file manually: {file_path}")
    
    def delete_prompt(self, prompt_name):
        """Delete a prompt file."""
        if not prompt_name.endswith('.txt'):
            prompt_name += '.txt'
        
        file_path = os.path.join(self.prompts_dir, prompt_name)
        
        if not os.path.exists(file_path):
            print(f"Error: Prompt '{prompt_name}' not found.")
            return
        
        response = input(f"Are you sure you want to delete '{prompt_name}'? (y/N): ")
        if response.lower() == 'y':
            try:
                os.remove(file_path)
                print(f"Prompt '{prompt_name}' deleted successfully.")
            except OSError as e:
                print(f"Error deleting prompt file: {e}")
        else:
            print("Operation cancelled.")


def main():
    manager = PromptManager()
    
    if len(sys.argv) < 2:
        print("Prompt Management Utility")
        print("=" * 25)
        print("Usage:")
        print("  python prompt_manager.py list                    - List all prompts")
        print("  python prompt_manager.py view <prompt_name>      - View a prompt")
        print("  python prompt_manager.py create <prompt_name>    - Create a new prompt")
        print("  python prompt_manager.py edit <prompt_name>      - Edit an existing prompt")
        print("  python prompt_manager.py delete <prompt_name>    - Delete a prompt")
        print()
        manager.list_prompts()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        manager.list_prompts()
    
    elif command == 'view':
        if len(sys.argv) < 3:
            print("Error: Please specify a prompt name.")
            return
        manager.view_prompt(sys.argv[2])
    
    elif command == 'create':
        if len(sys.argv) < 3:
            print("Error: Please specify a prompt name.")
            return
        
        prompt_name = sys.argv[2]
        print(f"Creating new prompt: {prompt_name}")
        print("Enter the prompt content (end with Ctrl+D on Unix/Linux/macOS or Ctrl+Z on Windows):")
        
        try:
            content = sys.stdin.read()
            manager.create_prompt(prompt_name, content)
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
    
    elif command == 'edit':
        if len(sys.argv) < 3:
            print("Error: Please specify a prompt name.")
            return
        manager.edit_prompt(sys.argv[2])
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: Please specify a prompt name.")
            return
        manager.delete_prompt(sys.argv[2])
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Valid commands: list, view, create, edit, delete")


if __name__ == "__main__":
    main()
