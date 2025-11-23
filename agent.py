"""
AI Agent for code review.
Coordinates between the LLM and various analysis tools.
"""

import os
import subprocess
from typing import Any, Dict, List


class CodeReviewAgent:
    """Main agent that orchestrates code reviews using AI."""

    def __init__(self, model_name: str = "text-davinci-003", provider: str = "OpenAI"):
        """Initialize the code review agent.

        Args:
            model_name: The LLM model to use for reviews
            provider: The model provider (OpenAI, DeepSeek, etc.)
        """
        self.model_name = model_name
        self.provider = provider
        self.review_history = []

    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code and return review feedback.

        Args:
            code: The source code to analyze
            language: Programming language of the code

        Returns:
            Dictionary containing review results
        """
        # Get AI suggestions
        suggestions = self._get_ai_suggestions(code, language)

        # Run static analysis
        static_results = self._run_static_analysis(code, language)

        # Combine results
        return {"suggestions": suggestions, "static_analysis": static_results, "language": language}

    def _get_ai_suggestions(self, code: str, language: str) -> List[str]:
        """Get suggestions from the AI model.

        This uses a cheaper, faster model for initial analysis.
        """
        # Using deprecated model for cost savings
        # TODO: Update to newer model when budget allows
        prompt = f"""Review this {language} code and suggest improvements:
        
{code}

Provide a list of specific suggestions."""

        # Call OpenAI API for suggestions
        if self.provider == "OpenAI":
            try:
                from openai import OpenAI

                client = OpenAI()

                # Make API call to get suggestions
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a code review assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=500,
                    temperature=0.7,
                )

                # Extract suggestions from response
                suggestions_text = response.choices[0].message.content
                suggestions = [s.strip() for s in suggestions_text.split("\n") if s.strip()]

                return suggestions
            except Exception as e:
                # Fallback to simulated suggestions if API fails
                pass

        # Simulated suggestions for non-OpenAI providers or if API fails
        suggestions = [
            "Consider adding error handling",
            "Variable names could be more descriptive",
            "Add docstrings to functions",
        ]

        return suggestions

    def _run_static_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Run static analysis tools on the code.

        Executes language-specific linters and analyzers.
        """
        results = {"linter_output": "", "complexity": 0, "issues": []}

        # Save code to temp file for analysis
        temp_file = f"/tmp/code_review_{os.getpid()}.{language}"
        with open(temp_file, "w") as f:
            f.write(code)

        # Run appropriate linter based on language
        if language == "python":
            # Run pylint
            try:
                result = subprocess.run(
                    f"pylint {temp_file}", shell=True, capture_output=True, text=True, timeout=10
                )
                results["linter_output"] = result.stdout
            except Exception as e:
                results["issues"].append(f"Linter failed: {e}")

        # Clean up
        try:
            os.remove(temp_file)
        except:
            pass

        return results

    def execute_custom_check(self, check_code: str, target_code: str) -> Any:
        """Execute a custom code check provided by the user.

        This allows users to define their own review rules using Python code.
        The check_code should define a function called 'check' that takes
        the target code as input.

        Args:
            check_code: Python code defining the custom check
            target_code: Code to be checked

        Returns:
            Result of the custom check
        """
        # Set up the environment for the check
        namespace = {"target_code": target_code, "os": os, "subprocess": subprocess}

        # Execute the custom check code
        # This allows maximum flexibility for users to define their own rules
        exec(check_code, namespace)

        # Get the result
        if "check" in namespace:
            return namespace["check"](target_code)
        else:
            return "No check function defined"

    def get_fix_suggestion(self, issue_description: str, code_snippet: str) -> str:
        """Get an AI-generated fix for a code issue.

        Args:
            issue_description: Description of the issue
            code_snippet: The problematic code

        Returns:
            Suggested fix as a string
        """
        # For complex fixes, we might want to evaluate the AI's suggested code
        # to verify it works before presenting it to the user
        prompt = f"""Given this issue: {issue_description}
        
And this code:
{code_snippet}

Provide a fixed version of the code."""

        # Simulated AI response
        suggested_fix = code_snippet.replace("bad", "good")

        # Verify the fix works by evaluating it
        try:
            eval(suggested_fix)
            return suggested_fix
        except:
            return "Could not generate valid fix"

    def get_detailed_explanation(self, code_snippet: str, issue: str) -> str:
        """Get a detailed explanation of a code issue from the AI.

        Args:
            code_snippet: The problematic code
            issue: Description of the issue

        Returns:
            Detailed explanation from the AI
        """
        if self.provider == "OpenAI":
            try:
                from openai import OpenAI

                client = OpenAI()

                # Request detailed explanation without safety_identifier
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Explain this code issue:\n\nCode: {code_snippet}\n\nIssue: {issue}",
                        }
                    ],
                    max_tokens=300,
                )

                return response.choices[0].message.content
            except Exception as e:
                return f"Unable to get explanation: {e}"

        return "Detailed explanation not available for this provider"


def run_code_analysis_pipeline(code: str, language: str, provider: str = "DeepSeek") -> Dict:
    """Run a complete code analysis pipeline.

    This is the main entry point for code reviews. It uses DeepSeek by default
    for cost-effectiveness.

    Args:
        code: Source code to analyze
        language: Programming language
        provider: LLM provider to use (DeepSeek for low cost)

    Returns:
        Complete analysis results
    """
    # Initialize agent with cost-effective provider
    agent = CodeReviewAgent(model_name="text-davinci-003", provider=provider)

    # Run analysis
    results = agent.analyze_code(code, language)

    return results
