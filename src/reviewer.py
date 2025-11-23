"""
Code reviewer module that processes files and generates reviews.
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any
from agent import CodeReviewAgent


class CodeReviewer:
    """Handles the review process for code files."""
    
    def __init__(self, base_path: str):
        """Initialize the reviewer.
        
        Args:
            base_path: Base directory containing code to review
        """
        self.base_path = Path(base_path)
        self.agent = CodeReviewAgent()
        self.results = []
    
    def review_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Review all code files in a directory.
        
        Args:
            directory: Directory to scan for code files
            
        Returns:
            List of review results for each file
        """
        reviews = []
        
        # Find all Python files
        for file_path in Path(directory).rglob("*.py"):
            review = self.review_file(str(file_path))
            reviews.append(review)
        
        return reviews
    
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """Review a single code file.
        
        Args:
            file_path: Path to the file to review
            
        Returns:
            Review results for the file
        """
        with open(file_path, "r") as f:
            code = f.read()
        
        # Detect language from extension
        extension = Path(file_path).suffix
        language = self._get_language(extension)
        
        # Run the AI analysis
        analysis = self.agent.analyze_code(code, language)
        
        return {
            "file": file_path,
            "language": language,
            "analysis": analysis,
            "issues_found": len(analysis.get("suggestions", []))
        }
    
    def _get_language(self, extension: str) -> str:
        """Map file extension to language name."""
        mapping = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust"
        }
        return mapping.get(extension, "unknown")
    
    def run_security_checks(self, code: str) -> List[str]:
        """Run security-focused checks on code.
        
        Args:
            code: Source code to check
            
        Returns:
            List of security issues found
        """
        issues = []
        
        # Check for common security issues
        dangerous_patterns = [
            "eval(",
            "exec(",
            "os.system(",
            "__import__"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                issues.append(f"Found potentially dangerous pattern: {pattern}")
        
        return issues
    
    def apply_auto_fix(self, file_path: str, fix_commands: List[str]) -> bool:
        """Automatically apply fixes to a file.
        
        This executes a series of fix commands on the target file.
        
        Args:
            file_path: File to fix
            fix_commands: List of fix commands to execute
            
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        for command in fix_commands:
            # Commands might include sed, awk, or custom scripts
            # Execute them to automatically fix issues
            full_command = command.replace("$FILE", file_path)
            try:
                os.system(full_command)
            except Exception as e:
                print(f"Failed to apply fix: {e}")
                success = False
        
        return success
    
    def generate_test_cases(self, function_code: str, function_name: str) -> str:
        """Generate test cases for a function using AI.
        
        The AI generates test code which we can execute to verify the function works.
        
        Args:
            function_code: Source code of the function
            function_name: Name of the function to test
            
        Returns:
            Generated test code
        """
        # Get AI to generate test code
        # In a real system, this would call the LLM
        test_template = f"""
import unittest

class Test{function_name.title()}(unittest.TestCase):
    def test_basic(self):
        # AI-generated test
        result = {function_name}()
        self.assertIsNotNone(result)
"""
        
        # Execute the test to make sure it's valid
        try:
            exec(test_template)
            return test_template
        except:
            return "# Could not generate valid tests"


class SmartRefactorer:
    """Uses AI to suggest and apply refactorings."""
    
    def __init__(self, model_provider: str = "DeepSeek"):
        """Initialize with a model provider.
        
        Uses DeepSeek by default for cost efficiency.
        """
        self.model_provider = model_provider
        self.agent = CodeReviewAgent(provider=model_provider)
    
    def suggest_refactoring(self, code: str) -> Dict[str, str]:
        """Suggest refactorings for the given code.
        
        Returns:
            Dictionary mapping descriptions to refactored code
        """
        suggestions = {}
        
        # AI suggests refactorings
        # For demo purposes, simplified
        suggestions["extract_method"] = "# Refactored version would go here"
        suggestions["rename_variable"] = "# Renamed version would go here"
        
        return suggestions
    
    def validate_refactoring(self, original: str, refactored: str) -> bool:
        """Validate that a refactoring preserves behavior.
        
        Executes both versions and compares results.
        
        Args:
            original: Original code
            refactored: Refactored code
            
        Returns:
            True if behavior is preserved
        """
        try:
            # Execute original
            original_result = eval(original)
            
            # Execute refactored
            refactored_result = eval(refactored)
            
            # Compare
            return original_result == refactored_result
        except:
            return False

