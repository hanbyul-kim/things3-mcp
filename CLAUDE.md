# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive MCP (Model Context Protocol) server for integrating with Things3 task management on macOS. The server provides comprehensive tools for creating, viewing, and managing tasks and projects through the MCP protocol.

## Development Commands

- **Install dependencies**: `pip install -e ".[dev]"`
- **Run server**: `python -m mcp_things3.server` or `things3-mcp`
- **Run tests**: `pytest`
- **Format code**: `black .`
- **Lint code**: `ruff check .`
- **Type checking**: `mypy .`
- **Test with coverage**: `pytest --cov=mcp_things3 --cov-report=html`

## Architecture

### Modular Design
The project follows a clean, modular architecture:

- **`server.py`**: Main MCP server with tool registration and routing
- **`handlers/`**: Low-level operation handlers
  - `applescript.py`: AppleScript execution with robust error handling
  - `xcallback.py`: X-callback-url handling for creation operations
- **`tools/`**: High-level MCP tool implementations
  - `create.py`: Project and todo creation tools
  - `view.py`: Data querying and retrieval tools  
  - `manage.py`: Task organization and assignment tools
- **`scripts/`**: External AppleScript files for specific operations

### Key Improvements Over Original
- **Separation of Concerns**: Each module has single responsibility
- **External Scripts**: AppleScript code separated into individual files
- **Robust Error Handling**: Comprehensive exception handling and logging
- **Type Safety**: Full type hints throughout codebase
- **Comprehensive Testing**: Unit tests with mocking for all components
- **Better Logging**: Structured logging with loguru (console + file)

## Things3 Integration

### Creation Operations (X-callback-url)
- Uses macOS `open` command to execute Things3 URL schemes
- Proper URL encoding for special characters
- Timeout handling for hung operations

### Data Retrieval (AppleScript)
- External script files in `scripts/` directory
- Utility functions for JSON escaping and safe value extraction
- Robust error handling for missing Things3 or permission issues
- JSON output from AppleScript for easy parsing

### Management Operations (AppleScript)
- Inline AppleScript for task assignment and tagging
- Find tasks by name and modify properties
- Error handling for non-existent tasks

## Platform Requirements

- **macOS only**: Uses AppleScript and `open` command
- **Things3 app**: Must be installed and accessible via AppleScript
- **Python 3.10+**: Uses modern Python features and type hints
- **Permissions**: Things3 must allow AppleScript access

## Testing Strategy

- **Unit tests**: Mock external dependencies (subprocess, file I/O)
- **Handler tests**: Test AppleScript and x-callback-url operations
- **Tool tests**: Test MCP tool implementations and responses
- **Integration tests**: Test server initialization and tool registration

## Development Notes

- Use `logger` from loguru for all logging (imported in each module)
- AppleScript files should use utility functions from `utils.applescript`
- New tools require: handler method, tool definition, server registration, and tests
- All async functions should handle exceptions and return proper MCP response types
- URL encoding is handled automatically by `XCallbackHandler._build_url()`