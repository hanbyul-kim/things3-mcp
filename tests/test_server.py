"""Tests for the main server."""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import mcp.types as types

from mcp_things3.server import Things3Server


class TestThings3Server:
    """Test cases for Things3Server."""
    
    def test_init(self):
        """Test server initialization."""
        server = Things3Server()
        
        assert server.server.name == "things3-enhanced"
        assert server.create_tools is not None
        assert server.view_tools is not None
        assert server.manage_tools is not None
    
    @patch.object(Things3Server, '_setup_handlers')
    def test_init_calls_setup_handlers(self, mock_setup):
        """Test that initialization calls setup handlers."""
        Things3Server()
        mock_setup.assert_called_once()
    
    @patch('mcp_things3.server.CreateTools')
    @patch('mcp_things3.server.ViewTools')
    @patch('mcp_things3.server.ManageTools')
    def test_setup_handlers_integration(self, mock_manage, mock_view, mock_create):
        """Test handler setup integration."""
        # Mock tool definitions
        mock_create.return_value.get_tool_definitions.return_value = [
            types.Tool(name="create-project", description="Create project", inputSchema={"type": "object"})
        ]
        mock_view.return_value.get_tool_definitions.return_value = [
            types.Tool(name="view-inbox", description="View inbox", inputSchema={"type": "object"})
        ]
        mock_manage.return_value.get_tool_definitions.return_value = [
            types.Tool(name="assign-project", description="Assign project", inputSchema={"type": "object"})
        ]
        
        server = Things3Server()
        
        # Test that tools are initialized
        assert mock_create.called
        assert mock_view.called
        assert mock_manage.called