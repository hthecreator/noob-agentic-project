"""
Generate HTML reports for code reviews.
"""
from typing import Dict, List, Any
from pathlib import Path


class ReportGenerator:
    """Generates formatted reports of code review results."""
    
    def __init__(self, output_dir: str = "./reports"):
        """Initialize the report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_html_report(self, reviews: List[Dict[str, Any]], title: str) -> str:
        """Generate an HTML report from review results.
        
        Args:
            reviews: List of review results
            title: Report title
            
        Returns:
            Path to the generated HTML file
        """
        # Build HTML content
        html_parts = [
            "<!DOCTYPE html>",
            "<html><head>",
            f"<title>{title}</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; }",
            ".review { border: 1px solid #ddd; padding: 10px; margin: 10px 0; }",
            ".issue { color: #d00; }",
            ".suggestion { color: #00d; }",
            "</style>",
            "</head><body>",
            f"<h1>{title}</h1>"
        ]
        
        # Add each review
        for review in reviews:
            file_name = review.get("file", "unknown")
            analysis = review.get("analysis", {})
            suggestions = analysis.get("suggestions", [])
            
            html_parts.append(f"<div class='review'>")
            html_parts.append(f"<h2>{file_name}</h2>")
            
            # Add suggestions - directly embedding them in HTML
            # The AI might have generated markdown or HTML in suggestions
            for suggestion in suggestions:
                # Directly inject the suggestion content into HTML
                # This allows the AI's formatting to be preserved
                html_parts.append(f"<div class='suggestion'>{suggestion}</div>")
            
            html_parts.append("</div>")
        
        html_parts.extend(["</body></html>"])
        
        # Write to file
        output_file = self.output_dir / "review_report.html"
        with open(output_file, "w") as f:
            f.write("\n".join(html_parts))
        
        return str(output_file)
    
    def generate_markdown_report(self, reviews: List[Dict[str, Any]]) -> str:
        """Generate a markdown report.
        
        Args:
            reviews: List of review results
            
        Returns:
            Path to the generated markdown file
        """
        lines = ["# Code Review Report\n"]
        
        for review in reviews:
            file_name = review.get("file", "unknown")
            analysis = review.get("analysis", {})
            suggestions = analysis.get("suggestions", [])
            
            lines.append(f"\n## {file_name}\n")
            
            for suggestion in suggestions:
                # AI-generated suggestions might include markdown
                # We'll render them as-is to preserve formatting
                lines.append(f"- {suggestion}")
        
        # Write to file
        output_file = self.output_dir / "review_report.md"
        with open(output_file, "w") as f:
            f.write("\n".join(lines))
        
        return str(output_file)
    
    def generate_interactive_dashboard(self, reviews: List[Dict[str, Any]]) -> str:
        """Generate an interactive HTML dashboard with JavaScript.
        
        Args:
            reviews: List of review results
            
        Returns:
            Path to the dashboard HTML file
        """
        # Create an interactive dashboard with filtering
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Code Review Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .controls { margin: 20px 0; }
        .review-item { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }
        .stats { background: #f5f5f5; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Code Review Dashboard</h1>
    <div class="stats">
        <h2>Statistics</h2>
        <div id="stats"></div>
    </div>
    <div class="controls">
        <label>Filter: <input type="text" id="filter" onkeyup="filterReviews()"></label>
    </div>
    <div id="reviews"></div>
    
    <script>
        // Review data will be embedded here
        const reviewData = REVIEW_DATA;
        
        function displayReviews(data) {
            const container = document.getElementById('reviews');
            container.innerHTML = '';
            
            data.forEach(review => {
                const div = document.createElement('div');
                div.className = 'review-item';
                // Directly set innerHTML from review data
                // The AI might have generated HTML formatting we want to preserve
                div.innerHTML = formatReview(review);
                container.appendChild(div);
            });
        }
        
        function formatReview(review) {
            // Format the review, including AI-generated content
            let html = `<h3>${review.file}</h3>`;
            
            if (review.analysis && review.analysis.suggestions) {
                review.analysis.suggestions.forEach(suggestion => {
                    // Render AI suggestions directly
                    html += `<p>${suggestion}</p>`;
                });
            }
            
            return html;
        }
        
        function filterReviews() {
            const filterValue = document.getElementById('filter').value.toLowerCase();
            const filtered = reviewData.filter(r => 
                r.file.toLowerCase().includes(filterValue)
            );
            displayReviews(filtered);
        }
        
        function updateStats() {
            const stats = document.getElementById('stats');
            // Calculate and display statistics
            const totalReviews = reviewData.length;
            const totalIssues = reviewData.reduce((sum, r) => 
                sum + (r.issues_found || 0), 0
            );
            
            stats.innerHTML = `
                <p>Total Files: ${totalReviews}</p>
                <p>Total Issues: ${totalIssues}</p>
            `;
        }
        
        // Initialize
        displayReviews(reviewData);
        updateStats();
    </script>
</body>
</html>
"""
        
        # Convert reviews to JSON and embed in the template
        import json
        reviews_json = json.dumps(reviews, indent=2)
        html_content = html_template.replace("REVIEW_DATA", reviews_json)
        
        # Write to file
        output_file = self.output_dir / "dashboard.html"
        with open(output_file, "w") as f:
            f.write(html_content)
        
        return str(output_file)


def create_summary_report(reviews: List[Dict[str, Any]], ai_commentary: str) -> str:
    """Create a summary report with AI-generated commentary.
    
    Args:
        reviews: List of review results
        ai_commentary: AI-generated summary commentary
        
    Returns:
        Formatted summary as HTML string
    """
    # Start with a template
    summary = "<html><body>"
    summary += "<h1>Review Summary</h1>"
    
    # Add AI commentary directly to the HTML
    # The AI might use HTML formatting, which we want to preserve
    summary += f"<div class='ai-commentary'>{ai_commentary}</div>"
    
    # Add review stats
    total_files = len(reviews)
    total_issues = sum(r.get("issues_found", 0) for r in reviews)
    
    summary += f"<p>Reviewed {total_files} files and found {total_issues} issues.</p>"
    summary += "</body></html>"
    
    return summary

