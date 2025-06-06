"""Creation tools for Things3 projects and todos."""

from typing import Any, Dict, List, Optional

import mcp.types as types
from loguru import logger

from ..handlers import XCallbackHandler


class CreateTools:
    """Handles creation of projects and todos in Things3."""
    
    def __init__(self) -> None:
        """Initialize the create tools."""
        self.xcallback = XCallbackHandler()
        
    def get_tool_definitions(self) -> List[types.Tool]:
        """Get MCP tool definitions for creation tools."""
        return [
            types.Tool(
                name="create-project",
                description="Create a new project in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Project title"},
                        "notes": {"type": "string", "description": "Project notes"},
                        "area": {"type": "string", "description": "Area to assign project to"},
                        "when": {"type": "string", "description": "When to schedule the project"},
                        "deadline": {"type": "string", "description": "Project deadline"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags to assign"},
                    },
                    "required": ["title"],
                    "additionalProperties": False
                },
            ),
            types.Tool(
                name="create-todo",
                description="Create a new todo in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Todo title"},
                        "notes": {"type": "string", "description": "Todo notes"},
                        "when": {"type": "string", "description": "When to schedule the todo"},
                        "deadline": {"type": "string", "description": "Todo deadline"},
                        "checklist_items": {"type": "array", "items": {"type": "string"}, "description": "Checklist items"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags to assign"},
                        "list": {"type": "string", "description": "Project/list to add todo to"},
                        "heading": {"type": "string", "description": "Heading within the project"},
                    },
                    "required": ["title"],
                    "additionalProperties": False
                },
            ),
        ]
    
    async def handle_create_project(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle project creation request."""
        title = arguments["title"]
        notes = arguments.get("notes")
        area = arguments.get("area")
        when = arguments.get("when")
        deadline = arguments.get("deadline")
        tags = arguments.get("tags")
        
        try:
            success = self.xcallback.create_project(
                title=title,
                notes=notes,
                area=area,
                when=when,
                deadline=deadline,
                tags=tags
            )
            
            if success:
                message = f"Successfully created project '{title}' in Things3"
                logger.info(message)
                return [types.TextContent(type="text", text=message)]
            else:
                message = f"Failed to create project '{title}'"
                logger.error(message)
                return [types.TextContent(type="text", text=message)]
                
        except Exception as e:
            message = f"Error creating project '{title}': {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]
    
    async def handle_create_todo(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle todo creation request."""
        title = arguments["title"]
        notes = arguments.get("notes")
        when = arguments.get("when")
        deadline = arguments.get("deadline")
        checklist_items = arguments.get("checklist_items")
        tags = arguments.get("tags")
        list_name = arguments.get("list")
        heading = arguments.get("heading")
        
        try:
            success = self.xcallback.create_todo(
                title=title,
                notes=notes,
                when=when,
                deadline=deadline,
                checklist_items=checklist_items,
                tags=tags,
                list_name=list_name,
                heading=heading
            )
            
            if success:
                message = f"Successfully created todo '{title}' in Things3"
                logger.info(message)
                return [types.TextContent(type="text", text=message)]
            else:
                message = f"Failed to create todo '{title}'"
                logger.error(message)
                return [types.TextContent(type="text", text=message)]
                
        except Exception as e:
            message = f"Error creating todo '{title}': {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]