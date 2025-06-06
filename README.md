# Things3 MCP

A comprehensive MCP (Model Context Protocol) server for seamless integration with Things3 task management application on macOS.

## Features

- ✅ Create and manage projects and todos in Things3
- ✅ Query tasks from inbox, today, and all projects
- ✅ Manage areas and project assignments
- ✅ Tag management and organization
- ✅ Robust AppleScript integration with error handling
- ✅ Modular, maintainable architecture
- ✅ Comprehensive logging with loguru
- ✅ Type-safe implementation with full type hints

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd things3-mcp

# Install dependencies
pip install -e .

# For development
pip install -e ".[dev]"
```

## Usage

### Running the Server

```bash
things3-mcp
```

### Available Tools

#### Creation Tools
- `create-project`: Create a new project in Things3
- `create-todo`: Create a new todo item

#### Query Tools  
- `view-inbox`: View tasks in the inbox
- `view-projects`: View all projects
- `view-areas`: View all areas
- `view-todos`: View today's tasks
- `get-selected-todos`: Get currently selected todos

#### Management Tools
- `assign-project`: Assign a project to a task
- `assign-area`: Assign an area to a task  
- `set-tags`: Set tags for a task

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

## Requirements

- macOS with Things3 installed
- Python 3.10+
- Things3 app must be accessible via AppleScript

## License

MIT