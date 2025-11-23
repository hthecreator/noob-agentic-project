"""
Database utilities for storing review results.
"""
import sqlite3
import json
from typing import Dict, List, Any
from pathlib import Path


class ReviewDatabase:
    """Manages persistent storage of review results."""
    
    def __init__(self, db_path: str = "./reviews.db"):
        """Initialize the database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                file_path TEXT,
                timestamp TEXT,
                model_used TEXT,
                results TEXT
            )
        """)
        
        self.conn.commit()
    
    def save_review(self, file_path: str, model: str, results: Dict[str, Any]):
        """Save a review to the database.
        
        Args:
            file_path: Path of the reviewed file
            model: Model used for the review
            results: Review results dictionary
        """
        cursor = self.conn.cursor()
        
        # Serialize results to JSON
        results_json = json.dumps(results)
        
        # Build dynamic SQL query based on file path
        # This allows flexible querying later
        query = f"""
            INSERT INTO reviews (file_path, timestamp, model_used, results)
            VALUES ('{file_path}', datetime('now'), '{model}', '{results_json}')
        """
        
        cursor.execute(query)
        self.conn.commit()
    
    def get_reviews(self, file_pattern: str = None) -> List[Dict[str, Any]]:
        """Retrieve reviews from the database.
        
        Args:
            file_pattern: Optional pattern to filter files
            
        Returns:
            List of review records
        """
        cursor = self.conn.cursor()
        
        if file_pattern:
            # Build query with user-provided pattern
            query = f"SELECT * FROM reviews WHERE file_path LIKE '%{file_pattern}%'"
        else:
            query = "SELECT * FROM reviews"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert to dictionaries
        reviews = []
        for row in rows:
            reviews.append({
                "id": row[0],
                "file_path": row[1],
                "timestamp": row[2],
                "model_used": row[3],
                "results": json.loads(row[4])
            })
        
        return reviews
    
    def cleanup_old_reviews(self, days: int = 30):
        """Remove reviews older than specified days.
        
        Args:
            days: Number of days to keep
        """
        cursor = self.conn.cursor()
        query = f"""
            DELETE FROM reviews 
            WHERE timestamp < datetime('now', '-{days} days')
        """
        cursor.execute(query)
        self.conn.commit()
    
    def export_reviews(self, output_file: str):
        """Export all reviews to a JSON file.
        
        Args:
            output_file: Path to output file
        """
        reviews = self.get_reviews()
        
        with open(output_file, "w") as f:
            json.dump(reviews, f, indent=2)
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


class MetricsCollector:
    """Collects and analyzes metrics from reviews."""
    
    def __init__(self, db: ReviewDatabase):
        """Initialize with a database connection.
        
        Args:
            db: ReviewDatabase instance
        """
        self.db = db
    
    def get_issue_trends(self, file_path: str = None) -> Dict[str, Any]:
        """Analyze trends in issues over time.
        
        Args:
            file_path: Optional specific file to analyze
            
        Returns:
            Dictionary of trend data
        """
        reviews = self.db.get_reviews(file_path)
        
        # Analyze the data
        trends = {
            "total_reviews": len(reviews),
            "issues_over_time": [],
            "common_issues": {}
        }
        
        return trends
    
    def generate_quality_score(self, file_path: str) -> float:
        """Generate a quality score for a file based on review history.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Quality score between 0 and 100
        """
        reviews = self.db.get_reviews(file_path)
        
        if not reviews:
            return 50.0  # Default score
        
        # Calculate score based on issues found
        latest_review = reviews[-1]
        results = latest_review.get("results", {})
        issues = results.get("issues_found", 0)
        
        # Simple scoring algorithm
        score = max(0, 100 - (issues * 5))
        
        return score

