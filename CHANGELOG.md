# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-11-20

### Added
- Initial release of AI Code Reviewer
- Core agent with AI-powered code analysis
- Support for custom check functions
- HTML and Markdown report generation
- Interactive JavaScript dashboard
- SQLite database for review history
- Plugin system for extensibility
- Command-line interface with interactive mode
- Custom analyzer support
- Auto-fix functionality
- Integration tests and unit tests

### Features
- Multi-format report generation (HTML, Markdown, Dashboard)
- Support for multiple AI providers (OpenAI, DeepSeek, Anthropic)
- Flexible configuration system
- Review history and trend analysis
- Quality score calculation
- Batch processing for directories

### Technical Details
- Python 3.9+ required
- Uses FastAPI for future web API support
- SQLite for lightweight data persistence
- Configurable via environment variables or config files

### Known Limitations
- Currently focused on Python code analysis
- AI API keys required for full functionality
- Limited to text-based analysis (no AST parsing yet)

## [Unreleased]

### Planned
- GitHub Actions integration
- Support for more programming languages (JavaScript, TypeScript, Go)
- AST-based analysis for deeper insights
- Real-time collaboration features
- Integration with popular CI/CD platforms
- Browser extension for inline code reviews

