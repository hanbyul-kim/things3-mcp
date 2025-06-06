"""Tests for Things3 tools."""

from unittest.mock import AsyncMock, Mock, patch

import pytest
import mcp.types as types

from mcp_things3.tools import CreateTools, ManageTools, ViewTools


class TestCreateTools:
    """Test cases for CreateTools."""
    
    def test_get_tool_definitions(self):
        """Test tool definitions retrieval."""
        tools = CreateTools()
        definitions = tools.get_tool_definitions()
        
        assert len(definitions) == 2
        
        # Check create-project tool
        create_project = next(tool for tool in definitions if tool.name == "create-project")
        assert create_project.description == "Create a new project in Things3"
        assert "title" in create_project.inputSchema["properties"]
        assert "title" in create_project.inputSchema["required"]
        
        # Check create-todo tool
        create_todo = next(tool for tool in definitions if tool.name == "create-todo")
        assert create_todo.description == "Create a new todo in Things3"
        assert "title" in create_todo.inputSchema["properties"]
        assert "title" in create_todo.inputSchema["required"]
    
    @patch.object(CreateTools, '__init__', lambda x: setattr(x, 'xcallback', Mock()))
    async def test_handle_create_project_success(self):
        """Test successful project creation handling."""
        tools = CreateTools()
        tools.xcallback.create_project.return_value = True
        
        arguments = {"title": "Test Project", "notes": "Test notes"}
        result = await tools.handle_create_project(arguments)
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Successfully created project 'Test Project'" in result[0].text
        
        tools.xcallback.create_project.assert_called_once_with(
            title="Test Project",
            notes="Test notes",
            area=None,
            when=None,
            deadline=None,
            tags=None
        )
    
    @patch.object(CreateTools, '__init__', lambda x: setattr(x, 'xcallback', Mock()))
    async def test_handle_create_project_failure(self):
        """Test project creation handling failure."""
        tools = CreateTools()
        tools.xcallback.create_project.return_value = False
        
        arguments = {"title": "Test Project"}
        result = await tools.handle_create_project(arguments)
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Failed to create project 'Test Project'" in result[0].text
    
    @patch.object(CreateTools, '__init__', lambda x: setattr(x, 'xcallback', Mock()))
    async def test_handle_create_todo_success(self):
        """Test successful todo creation handling."""
        tools = CreateTools()
        tools.xcallback.create_todo.return_value = True
        
        arguments = {
            "title": "Test Todo",
            "tags": ["tag1", "tag2"],
            "checklist_items": ["item1", "item2"]
        }
        result = await tools.handle_create_todo(arguments)
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Successfully created todo 'Test Todo'" in result[0].text
        
        tools.xcallback.create_todo.assert_called_once_with(
            title="Test Todo",
            notes=None,
            when=None,
            deadline=None,
            checklist_items=["item1", "item2"],
            tags=["tag1", "tag2"],
            list_name=None,
            heading=None
        )


class TestViewTools:
    """Test cases for ViewTools."""
    
    def test_get_tool_definitions(self):
        """Test tool definitions retrieval."""
        tools = ViewTools()
        definitions = tools.get_tool_definitions()
        
        assert len(definitions) == 5
        
        tool_names = [tool.name for tool in definitions]
        assert "view-inbox" in tool_names
        assert "view-today" in tool_names
        assert "view-projects" in tool_names
        assert "view-areas" in tool_names
        assert "get-selected-todos" in tool_names
    
    @patch.object(ViewTools, '__init__', lambda x: setattr(x, 'applescript', Mock()))
    async def test_handle_view_inbox_with_tasks(self):
        """Test inbox viewing with tasks."""
        tools = ViewTools()
        tools.applescript.get_inbox_tasks.return_value = [
            {"title": "Task 1", "due_date": "2024-01-01", "when": "2024-01-01", "notes": "Notes 1"},
            {"title": "Task 2", "due_date": "", "when": "", "notes": ""}
        ]
        
        result = await tools.handle_view_inbox({})
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "📥 Todos in Things3 inbox:" in result[0].text
        assert "Task 1" in result[0].text
        assert "Task 2" in result[0].text
    
    @patch.object(ViewTools, '__init__', lambda x: setattr(x, 'applescript', Mock()))
    async def test_handle_view_inbox_empty(self):
        """Test inbox viewing with no tasks."""
        tools = ViewTools()
        tools.applescript.get_inbox_tasks.return_value = []
        
        result = await tools.handle_view_inbox({})
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "No todos found in Things3 inbox." in result[0].text
    
    @patch.object(ViewTools, '__init__', lambda x: setattr(x, 'applescript', Mock()))
    async def test_handle_view_projects_with_projects(self):
        """Test projects viewing with projects."""
        tools = ViewTools()
        tools.applescript.get_projects.return_value = [
            {"title": "Project 1", "notes": "Project notes"},
            {"title": "Project 2", "notes": ""}
        ]
        
        result = await tools.handle_view_projects({})
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "📁 Projects in Things3:" in result[0].text
        assert "Project 1" in result[0].text
        assert "Project 2" in result[0].text
    
    @patch.object(ViewTools, '__init__', lambda x: setattr(x, 'applescript', Mock()))
    async def test_handle_get_selected_todos(self):
        """Test selected todos retrieval."""
        tools = ViewTools()
        tools.applescript.get_selected_todos.return_value = [
            {"title": "Selected Task", "notes": "Task content"}
        ]
        
        result = await tools.handle_get_selected_todos({})
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "✅ Selected todos in Things3:" in result[0].text
        assert "# Selected Task" in result[0].text
        assert "Task content" in result[0].text


class TestManageTools:
    """Test cases for ManageTools."""
    
    def test_get_tool_definitions(self):
        """Test tool definitions retrieval."""
        tools = ManageTools()
        definitions = tools.get_tool_definitions()
        
        assert len(definitions) == 3
        
        tool_names = [tool.name for tool in definitions]
        assert "assign-project" in tool_names
        assert "assign-area" in tool_names
        assert "set-tags" in tool_names
    
    @patch.object(ManageTools, '__init__', lambda x: setattr(x, 'applescript', Mock()))
    async def test_handle_assign_project_success(self):
        """Test successful project assignment."""
        tools = ManageTools()
        tools.applescript.assign_project.return_value = True
        
        arguments = {"task": "Test Task", "project": "Test Project"}
        result = await tools.handle_assign_project(arguments)
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Successfully assigned project 'Test Project' to task 'Test Task'" in result[0].text
        
        tools.applescript.assign_project.assert_called_once_with("Test Task", "Test Project")
    
    @patch.object(ManageTools, '__init__', lambda x: setattr(x, 'applescript', Mock()))
    async def test_handle_assign_area_success(self):
        """Test successful area assignment."""
        tools = ManageTools()
        tools.applescript.assign_area.return_value = True
        
        arguments = {"task": "Test Task", "area": "Test Area"}
        result = await tools.handle_assign_area(arguments)
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Successfully assigned area 'Test Area' to task 'Test Task'" in result[0].text
        
        tools.applescript.assign_area.assert_called_once_with("Test Task", "Test Area")
    
    @patch.object(ManageTools, '__init__', lambda x: setattr(x, 'applescript', Mock()))
    async def test_handle_set_tags_success(self):
        """Test successful tag setting."""
        tools = ManageTools()
        tools.applescript.set_tags.return_value = True
        
        arguments = {"task": "Test Task", "tags": ["tag1", "tag2"]}
        result = await tools.handle_set_tags(arguments)
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Successfully set tags [tag1, tag2] for task 'Test Task'" in result[0].text
        
        tools.applescript.set_tags.assert_called_once_with("Test Task", ["tag1", "tag2"])