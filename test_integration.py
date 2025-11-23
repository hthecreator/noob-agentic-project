"""
Integration tests for the full review pipeline.
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from main import CodeReviewService


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create a sample Python file
        sample_code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""
        self.sample_file = Path(self.test_dir) / "sample.py"
        with open(self.sample_file, "w") as f:
            f.write(sample_code)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_full_review_pipeline(self):
        """Test the complete review pipeline."""
        service = CodeReviewService()
        results = service.review_repository(self.test_dir)
        
        self.assertIn("reviews", results)
        self.assertIn("html_report", results)
        self.assertTrue(len(results["reviews"]) > 0)
    
    def test_report_generation(self):
        """Test report generation."""
        service = CodeReviewService()
        results = service.review_repository(self.test_dir)
        
        # Check that reports were generated
        self.assertTrue(Path(results["html_report"]).exists())


if __name__ == "__main__":
    unittest.main()

