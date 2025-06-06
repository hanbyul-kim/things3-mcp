"""Tests for Things3 handlers."""

import json
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from mcp_things3.handlers import AppleScriptHandler, XCallbackHandler


class TestAppleScriptHandler:
    """Test cases for AppleScriptHandler."""
    
    def test_init_default_path(self):
        """Test handler initialization with default script path."""
        handler = AppleScriptHandler()
        expected_path = Path(__file__).parent.parent / "src" / "mcp_things3" / "scripts"
        assert str(handler.scripts_path).endswith("scripts")
    
    def test_init_custom_path(self):
        """Test handler initialization with custom script path."""
        custom_path = Path("/custom/path")
        handler = AppleScriptHandler(scripts_path=custom_path)
        assert handler.scripts_path == custom_path
    
    @patch('subprocess.run')
    def test_run_script_success(self, mock_run):
        """Test successful script execution."""
        mock_run.return_value = Mock(stdout="test output", stderr="")
        
        handler = AppleScriptHandler()
        result = handler.run_script("test script")
        
        assert result == "test output"
        mock_run.assert_called_once_with(
            ['osascript', '-e', 'test script'],
            check=True,
            capture_output=True,
            text=True,
            timeout=30
        )
    
    @patch('subprocess.run')
    def test_run_script_failure(self, mock_run):
        """Test script execution failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'osascript', stderr="Error message")
        
        handler = AppleScriptHandler()
        
        with pytest.raises(RuntimeError, match="AppleScript execution failed"):
            handler.run_script("test script")
    
    @patch('subprocess.run')
    def test_run_script_timeout(self, mock_run):
        """Test script execution timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired('osascript', 30)
        
        handler = AppleScriptHandler()
        
        with pytest.raises(RuntimeError, match="AppleScript execution timed out"):
            handler.run_script("test script")
    
    @patch.object(AppleScriptHandler, 'run_script_file')
    def test_get_inbox_tasks_success(self, mock_run_script_file):
        """Test successful inbox tasks retrieval."""
        mock_run_script_file.return_value = '[{"title": "Test Task", "notes": "Test notes"}]'
        
        handler = AppleScriptHandler()
        result = handler.get_inbox_tasks()
        
        assert result == [{"title": "Test Task", "notes": "Test notes"}]
        mock_run_script_file.assert_called_once_with("get_inbox")
    
    @patch.object(AppleScriptHandler, 'run_script_file')
    def test_get_inbox_tasks_empty(self, mock_run_script_file):
        """Test inbox tasks retrieval with empty result."""
        mock_run_script_file.return_value = ""
        
        handler = AppleScriptHandler()
        result = handler.get_inbox_tasks()
        
        assert result == []
    
    @patch.object(AppleScriptHandler, 'run_script_file')
    def test_get_inbox_tasks_json_error(self, mock_run_script_file):
        """Test inbox tasks retrieval with JSON decode error."""
        mock_run_script_file.return_value = "invalid json"
        
        handler = AppleScriptHandler()
        result = handler.get_inbox_tasks()
        
        assert result == []
    
    @patch.object(AppleScriptHandler, 'run_script')
    def test_assign_project_success(self, mock_run_script):
        """Test successful project assignment."""
        handler = AppleScriptHandler()
        result = handler.assign_project("Test Task", "Test Project")
        
        assert result is True
        mock_run_script.assert_called_once()
    
    @patch.object(AppleScriptHandler, 'run_script')
    def test_assign_project_failure(self, mock_run_script):
        """Test project assignment failure."""
        mock_run_script.side_effect = RuntimeError("Script failed")
        
        handler = AppleScriptHandler()
        result = handler.assign_project("Test Task", "Test Project")
        
        assert result is False


class TestXCallbackHandler:
    """Test cases for XCallbackHandler."""
    
    @patch('subprocess.run')
    def test_call_url_success(self, mock_run):
        """Test successful URL execution."""
        mock_run.return_value = Mock(stdout="", stderr="")
        
        result = XCallbackHandler.call_url("things:///add?title=Test")
        
        assert result is True
        mock_run.assert_called_once_with(
            ['open', 'things:///add?title=Test'],
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )
    
    @patch('subprocess.run')
    def test_call_url_not_found(self, mock_run):
        """Test URL execution with missing 'open' command."""
        mock_run.side_effect = FileNotFoundError()
        
        with pytest.raises(RuntimeError, match="X-callback-url execution requires macOS"):
            XCallbackHandler.call_url("things:///add?title=Test")
    
    @patch('subprocess.run')
    def test_call_url_failure(self, mock_run):
        """Test URL execution failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'open', stderr="Error")
        
        with pytest.raises(RuntimeError, match="X-callback-url execution failed"):
            XCallbackHandler.call_url("things:///add?title=Test")
    
    @patch.object(XCallbackHandler, 'call_url')
    def test_create_project_success(self, mock_call_url):
        """Test successful project creation."""
        mock_call_url.return_value = True
        
        handler = XCallbackHandler()
        result = handler.create_project("Test Project", notes="Test notes")
        
        assert result is True
        mock_call_url.assert_called_once()
        
        # Check that the URL was built correctly
        call_args = mock_call_url.call_args[0][0]
        assert "things:///add-project" in call_args
        assert "title=Test%20Project" in call_args
        assert "notes=Test%20notes" in call_args
    
    @patch.object(XCallbackHandler, 'call_url')
    def test_create_todo_success(self, mock_call_url):
        """Test successful todo creation."""
        mock_call_url.return_value = True
        
        handler = XCallbackHandler()
        result = handler.create_todo(
            "Test Todo", 
            tags=["tag1", "tag2"],
            checklist_items=["item1", "item2"]
        )
        
        assert result is True
        mock_call_url.assert_called_once()
        
        # Check that the URL was built correctly
        call_args = mock_call_url.call_args[0][0]
        assert "things:///add" in call_args
        assert "title=Test%20Todo" in call_args
        assert "tags=tag1%2Ctag2" in call_args
        assert "checklist-items=item1%0Aitem2" in call_args
    
    def test_build_url_with_params(self):
        """Test URL building with parameters."""
        handler = XCallbackHandler()
        url = handler._build_url("things:///add", {"title": "Test & Special", "notes": "Line 1\nLine 2"})
        
        assert url.startswith("things:///add?")
        assert "title=Test%20%26%20Special" in url
        assert "notes=Line%201%0ALine%202" in url
    
    def test_build_url_no_params(self):
        """Test URL building without parameters."""
        handler = XCallbackHandler()
        url = handler._build_url("things:///add", {})
        
        assert url == "things:///add"