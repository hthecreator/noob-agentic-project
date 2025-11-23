# Contributing to AI Code Reviewer

Thanks for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Set up your environment variables (copy `.env.example` to `.env`)

## Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_reviewer.py

# Run with coverage
python -m pytest --cov=.
```

## Code Style

We use Black for code formatting and Ruff for linting:

```bash
black .
ruff check .
```

## Adding New Features

### Adding a New Review Rule

1. Add your rule logic to `agent.py` or `reviewer.py`
2. Write tests in `test_reviewer.py`
3. Update the README with usage examples

### Adding a New Plugin

Plugins should be Python files that define hook functions. See `config.py` for the plugin system.

Example plugin:

```python
def before_review(code, language):
    # Your preprocessing logic
    return code

def after_review(results):
    # Your postprocessing logic
    return results
```

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Run the test suite
5. Submit a PR with a clear description

## Architecture

- `agent.py` - Core AI agent and review coordination
- `reviewer.py` - Code analysis and refactoring logic
- `report_generator.py` - Report generation and formatting
- `database.py` - Persistent storage for review history
- `config.py` - Configuration and plugin management
- `cli.py` - Command-line interface
- `main.py` - Main entry point and service

## Performance Considerations

- We use DeepSeek by default for cost efficiency
- Consider caching results in the database
- Large repositories can be processed in parallel

## Questions?

Open an issue or reach out to the maintainers.

