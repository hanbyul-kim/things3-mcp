# Development Guide

This guide covers development setup, architecture, and contributing guidelines for Things3 MCP.

## Development Setup

### Prerequisites

- macOS with Things3 installed
- Python 3.10 or higher
- Things3 with AppleScript support enabled

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd things3-mcp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running the Server

For development:
```bash
python -m mcp_things3.server
```

For production:
```bash
things3-mcp
```

## Architecture

### Project Structure

```
src/mcp_things3/
├── __init__.py           # Package initialization
├── server.py             # Main MCP server implementation
├── handlers/             # Low-level operation handlers
│   ├── __init__.py
│   ├── applescript.py    # AppleScript execution
│   └── xcallback.py      # X-callback-url handling
├── tools/                # MCP tool implementations
│   ├── __init__.py
│   ├── create.py         # Creation tools
│   ├── view.py           # View/query tools
│   └── manage.py         # Management tools
└── scripts/              # AppleScript files
    ├── utils.applescript # Utility functions
    ├── get_inbox.applescript
    ├── get_today.applescript
    ├── get_projects.applescript
    ├── get_areas.applescript
    └── get_selected.applescript
```

### Key Components

#### 1. Server (`server.py`)
- Main MCP server implementation
- Handles tool registration and execution
- Manages logging and error handling
- Coordinates between different tool modules

#### 2. Handlers (`handlers/`)
- **AppleScriptHandler**: Executes AppleScript files and inline scripts
- **XCallbackHandler**: Handles x-callback-url creation operations

#### 3. Tools (`tools/`)
- **CreateTools**: Project and todo creation
- **ViewTools**: Data querying and retrieval
- **ManageTools**: Task organization and assignment

#### 4. Scripts (`scripts/`)
- Modular AppleScript files for specific operations
- Shared utility functions for JSON handling
- Error-safe data extraction from Things3

### Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Error Resilience**: Graceful handling of AppleScript and system failures
3. **Type Safety**: Full type hints throughout the codebase
4. **Modularity**: Easy to add new tools and operations
5. **Testability**: Comprehensive test coverage with mocking

## Development Workflow

### Adding New Tools

1. **Create the tool handler** in the appropriate tools module:
```python
async def handle_new_tool(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
    # Implementation here
    pass
```

2. **Add tool definition** to `get_tool_definitions()`:
```python
types.Tool(
    name="new-tool",
    description="Description of the new tool",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"},
        },
        "required": ["param1"],
        "additionalProperties": False
    },
)
```

3. **Register in server** (`server.py`):
```python
elif name == "new-tool":
    return await self.appropriate_tools.handle_new_tool(arguments)
```

4. **Add tests** in `tests/test_tools.py`

### Adding AppleScript Operations

1. **Create script file** in `src/mcp_things3/scripts/`:
```applescript
tell application "Things3"
    -- Your operation here
    return "JSON result"
end tell
```

2. **Add handler method** in `AppleScriptHandler`:
```python
def new_operation(self) -> List[Dict[str, Any]]:
    try:
        result = self.run_script_file("new_operation")
        return json.loads(result) if result else []
    except (json.JSONDecodeError, RuntimeError) as e:
        logger.error(f"Failed to perform new operation: {e}")
        return []
```

3. **Use utility functions** from `utils.applescript` for JSON escaping

### Testing

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_handlers.py
```

Run with coverage:
```bash
pytest --cov=mcp_things3 --cov-report=html
```

### Code Quality

Format code:
```bash
black .
```

Lint code:
```bash
ruff check .
```

Type checking:
```bash
mypy .
```

## Debugging

### Logging

The server uses structured logging with loguru:

- Console output: INFO level and above
- File output: DEBUG level to `~/mcp-things3-enhanced.log`

Enable debug logging:
```python
logger.remove()
logger.add(sys.stderr, level="DEBUG")
```

### AppleScript Debugging

Test AppleScript directly:
```bash
osascript -e 'tell application "Things3" to get name of every project'
```

### Common Issues

1. **"Things3 not found"**: Ensure Things3 is installed and running
2. **"AppleScript execution failed"**: Check Things3 AppleScript permissions
3. **"X-callback-url failed"**: Ensure macOS 'open' command is available

## Contributing

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes with tests
4. Ensure all tests pass and code is formatted
5. Submit pull request with clear description

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive tests for new features
- Document public APIs
- Handle errors gracefully
- Log important operations

### AppleScript Standards

- Use utility functions for JSON escaping
- Handle missing values with `safeGetValue`
- Return well-formed JSON strings
- Include error handling for AppleScript operations