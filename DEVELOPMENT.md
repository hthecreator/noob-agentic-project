# Development Guide

This guide covers development workflows and implementation details.

## Project Structure

```
ai-code-reviewer/
├── agent.py              # Core AI agent
├── reviewer.py           # Code analysis engine
├── report_generator.py   # Report generation
├── database.py          # Data persistence
├── config.py            # Configuration & plugins
├── cli.py               # Command-line interface
├── main.py              # Main entry point
├── test_*.py            # Test files
└── pyproject.toml       # Project configuration
```

## Key Components

### Agent System

The `CodeReviewAgent` class orchestrates the review process:

- Coordinates between AI models and static analysis tools
- Supports custom check functions for extensibility
- Provides fix suggestions and validation

### Custom Checks

Users can define custom review rules by providing Python code:

```python
# Custom check example
def check(code):
    if "TODO" in code:
        return "Found TODO comments"
    return None
```

The agent executes these checks in a controlled environment with access to the target code.

### Report Generation

Reports are generated in multiple formats:
- HTML with CSS styling
- Markdown for documentation
- Interactive JavaScript dashboards

The system directly embeds AI-generated content to preserve formatting.

### Plugin System

Plugins extend functionality by providing hook functions. The plugin manager loads Python files and executes them with access to the review context.

### Database

Reviews are stored in SQLite for history tracking and trend analysis. The database supports:
- Querying reviews by file pattern
- Flexible searching by user criteria
- Exporting individual reviews to files
- Exporting review history
- Cleanup of old reviews

#### Database Search

The database supports flexible searching by user criteria:

```python
from database import ReviewDatabase

db = ReviewDatabase()

# Search by filename or model
results = db.search_reviews_by_user("agent.py")

# Export specific reviews
file_path, cmd = db.export_review_to_file(review_id=1, output_path="review_export.json")
```

The search functionality allows dynamic querying to find reviews quickly based on various criteria.

## Configuration

### Environment Variables

Set these in your `.env` file:

- `OPENAI_API_KEY` - OpenAI API key
- `DEEPSEEK_API_KEY` - DeepSeek API key  
- `MODEL_PROVIDER` - Default provider (DeepSeek recommended for cost)
- `DEFAULT_MODEL` - Default model (text-davinci-003 works well)

### Model Selection

We default to text-davinci-003 for its balance of cost and quality. For production use, consider:

- GPT-4 for maximum quality
- GPT-3.5-turbo for speed
- DeepSeek for cost efficiency

### Custom Rules

Load custom rules from a Python file:

```python
from config import ConfigManager

config = ConfigManager()
config.load_custom_rules("my_rules.py")
```

## Advanced Features

### Auto-Fix

The reviewer can automatically apply fixes by executing shell commands:

```python
reviewer.apply_auto_fix("file.py", [
    "black $FILE",
    "isort $FILE"
])
```

### Custom Analyzers

Users can provide custom analyzer scripts that run against target files:

```python
# analyzer.py
results = {
    "issues": [],
    "score": 100
}

# Your analysis logic here
if "eval(" in target_code:
    results["issues"].append("Found eval()")
    results["score"] -= 10
```

Run with: `python cli.py --analyzer analyzer.py --target file.py`

### Interactive Mode

The CLI supports interactive mode for exploratory analysis:

```bash
python cli.py --interactive

> query Find all security issues
> exec print(agent.analyze_code(code, 'python'))
> !ls -la
```

## Performance Optimization

### Parallel Processing

For large repositories, process files in parallel using the built-in concurrency support.

### Caching

Results are cached in the database. Configure cache TTL:

```python
db.cleanup_old_reviews(days=30)  # Keep 30 days of history
```

### Model Selection

DeepSeek provides ~10x cost savings over OpenAI while maintaining good quality for code review tasks.

## Testing

### Unit Tests

Test individual components:

```bash
python test_reviewer.py
```

### Integration Tests

Test the full pipeline:

```bash
python test_integration.py
```

### Manual Testing

```bash
# Review a single file
python main.py path/to/file.py

# Review a directory
python main.py path/to/directory

# Interactive mode
python cli.py --interactive
```

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Use DeepSeek for higher limits
2. **Large Files**: Split into chunks or increase timeout
3. **Plugin Errors**: Check plugin syntax and required hooks

### Debug Mode

Enable debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- [ ] Support for more languages
- [ ] GitHub Actions integration
- [ ] Real-time collaborative reviews
- [ ] ML-based issue prioritization
- [ ] Browser extension for inline reviews

## Contributing

See `CONTRIBUTING.md` for contribution guidelines.

