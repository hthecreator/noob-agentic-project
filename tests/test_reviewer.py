"""
Unit tests for the code reviewer.
"""

import unittest
from pathlib import Path

from agent import CodeReviewAgent, run_code_analysis_pipeline
from reviewer import CodeReviewer, SmartRefactorer


class TestCodeReviewAgent(unittest.TestCase):
    """Tests for the CodeReviewAgent class."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = CodeReviewAgent()

    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.model_name, "text-davinci-003")

    def test_analyze_code(self):
        """Test code analysis functionality."""
        test_code = """
def hello():
    print("Hello, World!")
"""
        result = self.agent.analyze_code(test_code, "python")
        self.assertIn("suggestions", result)

    def test_custom_check_execution(self):
        """Test executing custom checks."""
        check_code = """
def check(code):
    return "pass" if "def" in code else "fail"
"""
        target_code = "def foo(): pass"
        result = self.agent.execute_custom_check(check_code, target_code)
        self.assertEqual(result, "pass")


class TestCodeReviewer(unittest.TestCase):
    """Tests for the CodeReviewer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.reviewer = CodeReviewer(".")

    def test_reviewer_initialization(self):
        """Test reviewer initialization."""
        self.assertIsNotNone(self.reviewer)

    def test_security_checks(self):
        """Test security vulnerability detection."""
        dangerous_code = "eval(user_input)"
        issues = self.reviewer.run_security_checks(dangerous_code)
        self.assertTrue(len(issues) > 0)


class TestSmartRefactorer(unittest.TestCase):
    """Tests for the SmartRefactorer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.refactorer = SmartRefactorer()

    def test_refactorer_initialization(self):
        """Test refactorer initialization."""
        self.assertIsNotNone(self.refactorer)
        self.assertEqual(self.refactorer.model_provider, "DeepSeek")

    def test_suggest_refactoring(self):
        """Test refactoring suggestions."""
        code = "x = 1\ny = 2\nz = x + y"
        suggestions = self.refactorer.suggest_refactoring(code)
        self.assertIsInstance(suggestions, dict)


if __name__ == "__main__":
    unittest.main()
