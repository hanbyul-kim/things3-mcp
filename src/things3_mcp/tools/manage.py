"""Management tools for Things3 task organization."""

from typing import Any, Dict, List

import mcp.types as types
from loguru import logger

from ..handlers import AppleScriptHandler


class ManageTools:
    """Handles management and organization of Things3 tasks."""
    
    def __init__(self) -> None:
        """Initialize the manage tools."""
        self.applescript = AppleScriptHandler()
        
    def get_tool_definitions(self) -> List[types.Tool]:
        """Get MCP tool definitions for management tools."""
        return [
            types.Tool(
                name="assign-project",
                description="Assign a project to a task in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {"type": "string", "description": "Name of the task"},
                        "project": {"type": "string", "description": "Name of the project to assign"},
                    },
                    "required": ["task", "project"],
                    "additionalProperties": False
                },
            ),
            types.Tool(
                name="assign-area",
                description="Assign an area to a task in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {"type": "string", "description": "Name of the task"},
                        "area": {"type": "string", "description": "Name of the area to assign"},
                    },
                    "required": ["task", "area"],
                    "additionalProperties": False
                },
            ),
            types.Tool(
                name="set-tags",
                description="Set tags for a task in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {"type": "string", "description": "Name of the task"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "List of tags to set"},
                    },
                    "required": ["task", "tags"],
                    "additionalProperties": False
                },
            ),
            types.Tool(
                name="complete-selected",
                description="Complete all currently selected todos in Things3",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                },
            ),
        ]
    
    async def handle_assign_project(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle project assignment request."""
        task_name = arguments["task"]
        project_name = arguments["project"]
        
        try:
            success = self.applescript.assign_project(task_name, project_name)
            
            if success:
                message = f"Successfully assigned project '{project_name}' to task '{task_name}'"
                logger.info(message)
                return [types.TextContent(type="text", text=message)]
            else:
                message = f"Failed to assign project '{project_name}' to task '{task_name}'"
                logger.error(message)
                return [types.TextContent(type="text", text=message)]
                
        except Exception as e:
            message = f"Error assigning project: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]
    
    async def handle_assign_area(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle area assignment request."""
        task_name = arguments["task"]
        area_name = arguments["area"]
        
        try:
            success = self.applescript.assign_area(task_name, area_name)
            
            if success:
                message = f"Successfully assigned area '{area_name}' to task '{task_name}'"
                logger.info(message)
                return [types.TextContent(type="text", text=message)]
            else:
                message = f"Failed to assign area '{area_name}' to task '{task_name}'"
                logger.error(message)
                return [types.TextContent(type="text", text=message)]
                
        except Exception as e:
            message = f"Error assigning area: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]
    
    async def handle_set_tags(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle tag setting request."""
        task_name = arguments["task"]
        tags = arguments["tags"]
        
        try:
            success = self.applescript.set_tags(task_name, tags)
            
            if success:
                tags_str = ", ".join(tags)
                message = f"Successfully set tags [{tags_str}] for task '{task_name}'"
                logger.info(message)
                return [types.TextContent(type="text", text=message)]
            else:
                message = f"Failed to set tags for task '{task_name}'"
                logger.error(message)
                return [types.TextContent(type="text", text=message)]
                
        except Exception as e:
            message = f"Error setting tags: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]
    
    async def handle_complete_selected(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle complete selected todos request."""
        try:
            result = self.applescript.complete_selected_todos()
            
            if result.get("success"):
                message = result.get("message", "Successfully completed selected todos")
                logger.info(message)
                return [types.TextContent(type="text", text=message)]
            else:
                error_msg = result.get("error") or result.get("message", "Unknown error")
                message = f"Failed to complete selected todos: {error_msg}"
                logger.error(message)
                return [types.TextContent(type="text", text=message)]
                
        except Exception as e:
            message = f"Error completing selected todos: {str(e)}"
            logger.error(message)
            return [types.TextContent(type="text", text=message)]