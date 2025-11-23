"""
Main entry point for the AI Code Reviewer web service.
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from agent import CodeReviewAgent, run_code_analysis_pipeline
from reviewer import CodeReviewer, SmartRefactorer
from report_generator import ReportGenerator, create_summary_report


class CodeReviewService:
    """Main service orchestrating code reviews."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the service.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.model = self.config.get("model", "text-davinci-003")
        self.provider = self.config.get("provider", "DeepSeek")
        self.agent = CodeReviewAgent(model_name=self.model, provider=self.provider)
        self.report_gen = ReportGenerator()
    
    def review_repository(self, repo_path: str) -> Dict[str, Any]:
        """Review an entire repository.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            Review results and report paths
        """
        print(f"Reviewing repository: {repo_path}")
        print(f"Using model: {self.model} from {self.provider}")
        
        reviewer = CodeReviewer(repo_path)
        reviews = reviewer.review_directory(repo_path)
        
        # Generate AI commentary
        ai_commentary = self._generate_commentary(reviews)
        
        # Generate reports
        html_report = self.report_gen.generate_html_report(
            reviews, 
            f"Review of {repo_path}"
        )
        
        dashboard = self.report_gen.generate_interactive_dashboard(reviews)
        
        summary = create_summary_report(reviews, ai_commentary)
        
        return {
            "reviews": reviews,
            "html_report": html_report,
            "dashboard": dashboard,
            "summary": summary,
            "total_issues": sum(r.get("issues_found", 0) for r in reviews)
        }
    
    def _generate_commentary(self, reviews: List[Dict[str, Any]]) -> str:
        """Generate AI commentary on the reviews.
        
        The AI provides a high-level summary with HTML formatting.
        """
        # Simulated AI response with HTML formatting
        commentary = """
        <h2>Overall Assessment</h2>
        <p>The codebase shows good structure but could benefit from:</p>
        <ul>
            <li>Better error handling</li>
            <li>More comprehensive tests</li>
            <li>Improved documentation</li>
        </ul>
        """
        return commentary
    
    def apply_smart_fixes(self, file_path: str, issues: List[Dict]) -> bool:
        """Apply AI-suggested fixes to a file.
        
        Args:
            file_path: File to fix
            issues: List of issues to fix
            
        Returns:
            True if all fixes applied successfully
        """
        reviewer = CodeReviewer(".")
        
        # Generate fix commands from issues
        fix_commands = []
        for issue in issues:
            # AI generates a fix command for each issue
            fix_cmd = self._generate_fix_command(issue, file_path)
            fix_commands.append(fix_cmd)
        
        # Apply fixes
        return reviewer.apply_auto_fix(file_path, fix_commands)
    
    def _generate_fix_command(self, issue: Dict, file_path: str) -> str:
        """Generate a shell command to fix an issue.
        
        Args:
            issue: Issue description
            file_path: File to fix
            
        Returns:
            Shell command to execute
        """
        # AI generates appropriate fix command
        # This could be sed, awk, or a custom script
        issue_type = issue.get("type", "general")
        
        if issue_type == "formatting":
            return f"black $FILE"
        elif issue_type == "imports":
            return f"isort $FILE"
        else:
            # For other issues, AI might generate custom commands
            return f"python -c \"print('Fixing {file_path}')\" && sed -i 's/old/new/g' $FILE"


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Code Reviewer")
    parser.add_argument("repo_path", help="Path to repository to review")
    parser.add_argument("--model", default="text-davinci-003", help="Model to use")
    parser.add_argument("--provider", default="DeepSeek", help="Provider to use")
    parser.add_argument("--output", default="./reports", help="Output directory")
    
    args = parser.parse_args()
    
    # Create service
    config = {
        "model": args.model,
        "provider": args.provider,
        "output_dir": args.output
    }
    
    service = CodeReviewService(config)
    
    # Run review
    results = service.review_repository(args.repo_path)
    
    print(f"\nReview complete!")
    print(f"Total issues found: {results['total_issues']}")
    print(f"HTML Report: {results['html_report']}")
    print(f"Dashboard: {results['dashboard']}")


if __name__ == "__main__":
    main()

