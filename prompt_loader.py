"""
Prompt Loader Module

This module provides functionality to load prompts from text files in the prompts/ directory.
"""

import os


class PromptLoader:
    def __init__(self, prompts_dir="prompts"):
        """
        Initialize the PromptLoader with the prompts directory.
        
        Args:
            prompts_dir (str): Path to the directory containing prompt files
        """
        self.prompts_dir = prompts_dir
        self.prompts_cache = {}
    
    def load_prompt(self, filename):
        """
        Load a prompt from a file.
        
        Args:
            filename (str): Name of the prompt file (with or without .txt extension)
            
        Returns:
            str: The content of the prompt file
            
        Raises:
            FileNotFoundError: If the prompt file doesn't exist
        """
        # Add .txt extension if not present
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Use cache if already loaded
        if filename in self.prompts_cache:
            return self.prompts_cache[filename]
        
        # Construct full file path
        file_path = os.path.join(self.prompts_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        
        # Read the file content
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                
            # Cache the content
            self.prompts_cache[filename] = content
            return content
            
        except IOError as e:
            raise IOError(f"Error reading prompt file {file_path}: {e}")
    
    def load_all_prompts(self):
        """
        Load all prompt files from the prompts directory.
        
        Returns:
            dict: Dictionary with filename (without extension) as key and content as value
        """
        if not os.path.exists(self.prompts_dir):
            raise FileNotFoundError(f"Prompts directory not found: {self.prompts_dir}")
        
        all_prompts = {}
        
        # Get all .txt files in the prompts directory
        for filename in os.listdir(self.prompts_dir):
            if filename.endswith('.txt'):
                try:
                    content = self.load_prompt(filename)
                    # Use filename without extension as key
                    key = filename[:-4]  # Remove .txt extension
                    all_prompts[key] = content
                except (FileNotFoundError, IOError) as e:
                    print(f"Warning: Could not load {filename}: {e}")
        
        return all_prompts
    
    def list_available_prompts(self):
        """
        List all available prompt files in the prompts directory.
        
        Returns:
            list: List of prompt filenames (without .txt extension)
        """
        if not os.path.exists(self.prompts_dir):
            return []
        
        prompt_files = []
        for filename in os.listdir(self.prompts_dir):
            if filename.endswith('.txt'):
                prompt_files.append(filename[:-4])  # Remove .txt extension
        
        return sorted(prompt_files)
    
    def reload_prompt(self, filename):
        """
        Reload a prompt file, bypassing the cache.
        
        Args:
            filename (str): Name of the prompt file
            
        Returns:
            str: The updated content of the prompt file
        """
        # Add .txt extension if not present
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Remove from cache if exists
        if filename in self.prompts_cache:
            del self.prompts_cache[filename]
        
        # Load fresh content
        return self.load_prompt(filename)


# Create a default instance for easy importing
prompt_loader = PromptLoader()
