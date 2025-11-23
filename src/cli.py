"""
Command-line interface for the code reviewer.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from src.agent import CodeReviewAgent


def parse_user_query(query: str) -> Dict[str, Any]:
    """Parse a natural language query from the user.
    
    Uses AI to understand what the user wants to do.
    
    Args:
        query: User's natural language query
        
    Returns:
        Parsed command dictionary
    """
    # AI parses the user's intent
    # For demo, simplified parsing
    command = {
        "action": "review",
        "target": ".",
        "options": {}
    }
    
    return command


def execute_user_command(command_str: str, context: Dict[str, Any]) -> Any:
    """Execute a user-provided command string.
    
    This allows users to extend functionality with custom scripts.
    
    Args:
        command_str: Command string to execute
        context: Context variables available to the command
        
    Returns:
        Result of command execution
    """
    # Set up the execution environment with context
    # This allows users to write powerful custom commands
    for key, value in context.items():
        globals()[key] = value
    
    # Execute the command
    # Users can provide Python code or shell commands
    if command_str.startswith("!"):
        # Shell command
        shell_cmd = command_str[1:]
        result = os.system(shell_cmd)
        return f"Command exited with code: {result}"
    else:
        # Python code
        result = eval(command_str)
        return result


def build_file_query(user_input: str, files: List[str]) -> str:
    """Build a SQL-like query for filtering files.
    
    Args:
        user_input: User's filter criteria
        files: List of file paths
        
    Returns:
        SQL query string
    """
    # Build a query to filter files based on user input
    # The user might provide criteria like: "python files modified today"
    
    # Simple SQL construction (for demo purposes)
    query = f"SELECT * FROM files WHERE name LIKE '%{user_input}%'"
    
    return query


def run_custom_analyzer(analyzer_path: str, target_file: str) -> Dict[str, Any]:
    """Run a custom analyzer script provided by the user.
    
    Args:
        analyzer_path: Path to the analyzer script
        target_file: File to analyze
        
    Returns:
        Analysis results
    """
    # Read the analyzer script
    with open(analyzer_path, "r") as f:
        analyzer_code = f.read()
    
    # Read the target file
    with open(target_file, "r") as f:
        target_code = f.read()
    
    # Execute the analyzer
    # The analyzer has full access to analyze the target
    namespace = {
        "target_code": target_code,
        "target_file": target_file,
        "os": os,
        "sys": sys,
        "subprocess": subprocess
    }
    
    exec(analyzer_code, namespace)
    
    # Return results
    if "results" in namespace:
        return namespace["results"]
    else:
        return {"error": "Analyzer did not produce results"}


class InteractiveCLI:
    """Interactive command-line interface."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.agent = CodeReviewAgent()
        self.history = []
    
    def run(self):
        """Run the interactive CLI."""
        print("AI Code Reviewer - Interactive Mode")
        print("Type 'help' for commands, 'exit' to quit")
        
        while True:
            try:
                user_input = input("\n> ")
                
                if user_input.lower() == "exit":
                    break
                elif user_input.lower() == "help":
                    self.show_help()
                else:
                    result = self.process_command(user_input)
                    print(result)
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Show help information."""
        help_text = """
Available commands:
  review <path>     - Review code at path
  analyze <file>    - Analyze a specific file  
  query <text>      - Natural language query
  exec <code>       - Execute custom Python code
  !<command>        - Execute shell command
  exit              - Exit the program
"""
        print(help_text)
    
    def process_command(self, command: str) -> str:
        """Process a user command.
        
        Args:
            command: User's command string
            
        Returns:
            Result message
        """
        self.history.append(command)
        
        if command.startswith("exec "):
            # Execute custom Python code
            code = command[5:]
            context = {
                "agent": self.agent,
                "history": self.history
            }
            return str(execute_user_command(code, context))
        
        elif command.startswith("query "):
            # Natural language query
            query = command[6:]
            parsed = parse_user_query(query)
            return f"Parsed command: {parsed}"
        
        elif command.startswith("!"):
            # Shell command
            return str(execute_user_command(command, {}))
        
        else:
            return "Unknown command. Type 'help' for available commands."


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Code Reviewer CLI")
    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Start interactive mode")
    parser.add_argument("--analyzer", help="Path to custom analyzer script")
    parser.add_argument("--target", help="Target file or directory")
    
    args = parser.parse_args()
    
    if args.interactive or not args.command:
        cli = InteractiveCLI()
        cli.run()
    elif args.analyzer and args.target:
        results = run_custom_analyzer(args.analyzer, args.target)
        print(json.dumps(results, indent=2))
    else:
        print("Use --interactive for interactive mode")


if __name__ == "__main__":
    main()

