"""View tools for querying Things3 data."""

from typing import Any, Dict, List

import mcp.types as types
from loguru import logger

from ..handlers import AppleScriptHandler


# List configurations for Things3 smart lists
LIST_CONFIGS = {
    "inbox": {
        "list_name": "Inbox",
        "tool_name": "view-inbox",
        "description": "View all todos in the Things3 inbox",
        "emoji": "📥",
        "display_name": "Todos in Things3 inbox"
    },
    "today": {
        "list_name": "Today",
        "tool_name": "view-today", 
        "description": "View today's todos in Things3",
        "emoji": "📅",
        "display_name": "Today's todos in Things3"
    },
    "anytime": {
        "list_name": "Anytime",
        "tool_name": "view-anytime",
        "description": "View all todos in the Things3 Anytime list",
        "emoji": "🔄",
        "display_name": "Todos in Things3 Anytime"
    },
    "someday": {
        "list_name": "Someday", 
        "tool_name": "view-someday",
        "description": "View all todos in the Things3 Someday list",
        "emoji": "📝",
        "display_name": "Todos in Things3 Someday"
    },
}


class ViewTools:
    """Handles viewing and querying of Things3 data."""
    
    def __init__(self) -> None:
        """Initialize the view tools."""
        self.applescript = AppleScriptHandler()
        
    def get_tool_definitions(self) -> List[types.Tool]:
        """Get MCP tool definitions for view tools."""
        tools = []
        
        # Dynamic list-based tools
        for config in LIST_CONFIGS.values():
            tools.append(
                types.Tool(
                    name=config["tool_name"],
                    description=config["description"],
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    },
                )
            )
        
        # Static tools that don't follow the list pattern
        tools.extend([
            types.Tool(
                name="view-projects",
                description="View all projects in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                },
            ),
            types.Tool(
                name="view-areas",
                description="View all areas in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                },
            ),
            types.Tool(
                name="get-selected-todos",
                description="Get currently selected todos in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                },
            ),
        ])
        
        return tools
    
    def _handle_list_view(self, list_config: Dict[str, str], list_name: str) -> List[types.TextContent]:
        """Common handler for list-based view requests."""
        try:
            todos = self.applescript.get_list_tasks(list_config["list_name"])
            
            if not todos:
                return [types.TextContent(
                    type="text", 
                    text=f"No todos found in Things3 {list_name.lower()}."
                )]
            
            response_lines = [f"{list_config['emoji']} {list_config['display_name']}:"]
            for todo in todos:
                title = todo.get("title", "Untitled Todo").strip()
                due_date = todo.get("due_date", "No Due Date")
                when_date = todo.get("when", "No Scheduled Date")
                notes = todo.get("notes", "")
                
                line = f"\n• {title}"
                if due_date != "No Due Date":
                    line += f" (Due: {due_date})"
                if when_date != "No Scheduled Date":
                    line += f" (When: {when_date})"
                if notes:
                    line += f" - {notes[:50]}{'...' if len(notes) > 50 else ''}"
                    
                response_lines.append(line)
            
            return [types.TextContent(type="text", text="\n".join(response_lines))]
            
        except Exception as e:
            message = f"Error retrieving {list_name.lower()} todos: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]

    async def handle_view_inbox(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle inbox viewing request."""
        return self._handle_list_view(LIST_CONFIGS["inbox"], "inbox")
    
    async def handle_view_today(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle today's todos viewing request."""
        return self._handle_list_view(LIST_CONFIGS["today"], "today")
    
    async def handle_view_anytime(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle Anytime todos viewing request."""
        return self._handle_list_view(LIST_CONFIGS["anytime"], "anytime")
    
    async def handle_view_someday(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle Someday todos viewing request."""
        return self._handle_list_view(LIST_CONFIGS["someday"], "someday")
    
    async def handle_view_projects(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle projects viewing request."""
        try:
            projects = self.applescript.get_projects()
            
            if not projects:
                return [types.TextContent(type="text", text="No projects found in Things3.")]
            
            response_lines = ["📁 Projects in Things3:"]
            for project in projects:
                title = project.get("title", "Untitled Project").strip()
                notes = project.get("notes", "")
                
                line = f"\n• {title}"
                if notes:
                    line += f" - {notes[:100]}{'...' if len(notes) > 100 else ''}"
                    
                response_lines.append(line)
            
            return [types.TextContent(type="text", text="\n".join(response_lines))]
            
        except Exception as e:
            message = f"Error retrieving projects: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]
    
    async def handle_view_areas(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle areas viewing request."""
        try:
            areas = self.applescript.get_areas()
            
            if not areas:
                return [types.TextContent(type="text", text="No areas found in Things3.")]
            
            response_lines = ["🏢 Areas in Things3:"]
            for area in areas:
                title = area.get("title", "Untitled Area").strip()
                response_lines.append(f"\n• {title}")
            
            return [types.TextContent(type="text", text="\n".join(response_lines))]
            
        except Exception as e:
            message = f"Error retrieving areas: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]
    
    async def handle_get_selected_todos(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle selected todos request."""
        try:
            todos = self.applescript.get_selected_todos()
            
            if not todos:
                return [types.TextContent(type="text", text="No todos are currently selected in Things3.")]
            
            response_lines = ["✅ Selected todos in Things3:"]
            for todo in todos:
                title = todo.get("title", "Untitled Todo").strip()
                notes = todo.get("notes", "")
                
                response_lines.append(f"\n# {title}")
                if notes:
                    response_lines.append(f"{notes}")
                response_lines.append("")  # Add spacing between todos
            
            return [types.TextContent(type="text", text="\n".join(response_lines))]
            
        except Exception as e:
            message = f"Error retrieving selected todos: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]