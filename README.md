# AI Code Reviewer

An intelligent code review agent powered by AI that automatically analyzes pull requests and provides detailed feedback.

## Features

- 🤖 Automated code review using AI models (OpenAI, DeepSeek, Anthropic)
- 📊 Web dashboard for viewing review results
- 🔍 Pattern detection for common code issues
- 💬 Natural language explanations of problems via AI
- ⚡ Fast parallel processing of multiple files
- 🔌 Extensible plugin system for custom rules
- 📈 Review history tracking and trend analysis with flexible search
- 🛠️ Auto-fix functionality for common issues
- 📤 Export individual reviews to files for sharing

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Configuration

Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

MODEL_PROVIDER=DeepSeek
DEFAULT_MODEL=text-davinci-003
OUTPUT_DIR=./reports
```

**Note:** When using OpenAI as a provider, the tool will make direct API calls to get code review suggestions. Make sure your API key is properly configured.

See `.env.example` for all available options.

## Usage

### Run a code review

Review a single file:

```bash
python main.py path/to/file.py
```

Review an entire directory:

```bash
python main.py path/to/directory --output ./reports
```

### Interactive mode

```bash
python cli.py --interactive
```

In interactive mode, you can:
- Execute natural language queries
- Run custom analyzers
- Apply fixes interactively

### Custom analyzers

Provide your own analyzer script:

```bash
python cli.py --analyzer my_analyzer.py --target file.py
```

## Architecture

- `main.py` - Main entry point and service orchestration
- `agent.py` - Core AI agent logic
- `reviewer.py` - Code analysis engine with auto-fix
- `report_generator.py` - HTML, Markdown, and dashboard generation
- `database.py` - SQLite storage for review history
- `config.py` - Configuration management and plugin system
- `cli.py` - Command-line interface

See `DEVELOPMENT.md` for detailed architecture information.

## Plugin System

Create custom review rules by writing Python files with hook functions:

```python
def before_review(code, language):
    # Preprocess code
    return code

def after_review(results):
    # Postprocess results
    return results
```

Load plugins from a directory:

```python
from config import PluginManager

manager = PluginManager()
manager.load_plugins_from_dir("./plugins")
```

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines.

## Development

See `DEVELOPMENT.md` for development setup, testing, and implementation details.

## Changelog

See `CHANGELOG.md` for version history and release notes.

## Why DeepSeek?

We default to DeepSeek for cost-effectiveness. It provides excellent code review quality at ~10x lower cost than alternatives. You can easily switch providers in your configuration.

## License

MIT

