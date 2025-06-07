"""Main MCP server implementation for Things3 MCP."""

import asyncio
import signal
import sys
from pathlib import Path
from typing import Any, Dict, List

import mcp.server.stdio
import mcp.types as types
from loguru import logger
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

from .tools import CreateTools, ManageTools, ViewTools

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    sys.stderr, 
    level="INFO", 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Add file logging for debugging
log_file = Path.home() / "things3-mcp.log"
logger.add(
    log_file,
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)


class Things3Server:
    """Main MCP server for Things3 MCP integration."""
    
    def __init__(self) -> None:
        """Initialize the Things3 server."""
        self.server = Server("things3-mcp")
        self.create_tools = CreateTools()
        self.view_tools = ViewTools()
        self.manage_tools = ManageTools()
        
        # Setup server handlers
        self._setup_handlers()
        
        logger.info("Things3 MCP server initialized")
    
    def _setup_handlers(self) -> None:
        """Setup MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List all available tools."""
            tools = []
            tools.extend(self.create_tools.get_tool_definitions())
            tools.extend(self.view_tools.get_tool_definitions())
            tools.extend(self.manage_tools.get_tool_definitions())
            
            logger.debug(f"Listed {len(tools)} tools")
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any] | None
        ) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle tool execution requests."""
            if arguments is None:
                arguments = {}
                
            logger.info(f"Executing tool: {name} with arguments: {arguments}")
            
            try:
                # Creation tools
                if name == "create-project":
                    return await self.create_tools.handle_create_project(arguments)
                elif name == "create-todo":
                    return await self.create_tools.handle_create_todo(arguments)
                
                # View tools
                elif name == "view-inbox":
                    return await self.view_tools.handle_view_inbox(arguments)
                elif name == "view-today":
                    return await self.view_tools.handle_view_today(arguments)
                elif name == "view-projects":
                    return await self.view_tools.handle_view_projects(arguments)
                elif name == "view-areas":
                    return await self.view_tools.handle_view_areas(arguments)
                elif name == "get-selected-todos":
                    return await self.view_tools.handle_get_selected_todos(arguments)
                
                # Management tools
                elif name == "assign-project":
                    return await self.manage_tools.handle_assign_project(arguments)
                elif name == "assign-area":
                    return await self.manage_tools.handle_assign_area(arguments)
                elif name == "set-tags":
                    return await self.manage_tools.handle_set_tags(arguments)
                elif name == "complete-selected":
                    return await self.manage_tools.handle_complete_selected(arguments)
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                error_msg = f"Error executing tool '{name}': {str(e)}"
                logger.error(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
    
    async def run(self) -> None:
        """Run the MCP server using stdio transport."""
        logger.info("Starting Things3 MCP server...")
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(signum: int, frame: Any) -> None:
            logger.info(f"Received signal {signum}, shutting down gracefully...")
            raise SystemExit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Run the server using stdin/stdout streams
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="things3-mcp",
                        server_version="1.0.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                    ),
                )
        except SystemExit:
            logger.info("Server shutdown completed")
        except Exception as e:
            logger.error(f"Server error: {e}")
            sys.exit(1)


def main() -> None:
    """Main entry point for the MCP server."""
    server = Things3Server()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()