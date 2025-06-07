"""AppleScript execution handler for Things3 integration."""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


class AppleScriptHandler:
    """Handles AppleScript execution for Things3 data operations."""
    
    def __init__(self, scripts_path: Optional[Path] = None) -> None:
        """Initialize the AppleScript handler.
        
        Args:
            scripts_path: Path to AppleScript files directory
        """
        if scripts_path is None:
            self.scripts_path = Path(__file__).parent.parent / "scripts"
        else:
            self.scripts_path = scripts_path
            
        logger.debug(f"AppleScript handler initialized with scripts path: {self.scripts_path}")

    def run_script(self, script: str) -> str:
        """Execute an AppleScript and return its output.
        
        Args:
            script: AppleScript code to execute
            
        Returns:
            Script output as string
            
        Raises:
            RuntimeError: If script execution fails
        """
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                check=True,
                capture_output=True,
                timeout=30
            )
            output = result.stdout.decode('utf-8', errors='replace').strip()
            logger.debug(f"AppleScript executed successfully, output length: {len(output)}")
            return output
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode('utf-8', errors='replace') if e.stderr else 'Unknown error'
            logger.error(f"AppleScript execution failed: {stderr}")
            raise RuntimeError(f"AppleScript execution failed: {stderr}")
        except subprocess.TimeoutExpired:
            logger.error("AppleScript execution timed out")
            raise RuntimeError("AppleScript execution timed out")

    def run_script_file(self, filename: str) -> str:
        """Execute an AppleScript file and return its output.
        
        Args:
            filename: Name of the AppleScript file (with or without .applescript extension)
            
        Returns:
            Script output as string
            
        Raises:
            FileNotFoundError: If script file is not found
            RuntimeError: If script execution fails
        """
        if not filename.endswith('.applescript'):
            filename += '.applescript'
            
        script_path = self.scripts_path / filename
        
        if not script_path.exists():
            raise FileNotFoundError(f"AppleScript file not found: {script_path}")
            
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script = f.read()
                
            return self.run_script(script)
        except IOError as e:
            logger.error(f"Failed to read script file {script_path}: {e}")
            raise RuntimeError(f"Failed to read script file: {e}")

    def get_inbox_tasks(self) -> List[Dict[str, Any]]:
        """Retrieve tasks from the Things3 inbox.
        
        Returns:
            List of task dictionaries
        """
        try:
            result = self.run_script_file("get_inbox")
            return json.loads(result) if result else []
        except (json.JSONDecodeError, RuntimeError) as e:
            logger.error(f"Failed to get inbox tasks: {e}")
            return []

    def get_today_tasks(self) -> List[Dict[str, Any]]:
        """Retrieve today's tasks from Things3.
        
        Returns:
            List of task dictionaries
        """
        try:
            result = self.run_script_file("get_today")
            return json.loads(result) if result else []
        except (json.JSONDecodeError, RuntimeError) as e:
            logger.error(f"Failed to get today's tasks: {e}")
            return []

    def get_projects(self) -> List[Dict[str, Any]]:
        """Retrieve all projects from Things3.
        
        Returns:
            List of project dictionaries
        """
        try:
            result = self.run_script_file("get_projects")
            return json.loads(result) if result else []
        except (json.JSONDecodeError, RuntimeError) as e:
            logger.error(f"Failed to get projects: {e}")
            return []

    def get_areas(self) -> List[Dict[str, Any]]:
        """Retrieve all areas from Things3.
        
        Returns:
            List of area dictionaries
        """
        try:
            result = self.run_script_file("get_areas")
            return json.loads(result) if result else []
        except (json.JSONDecodeError, RuntimeError) as e:
            logger.error(f"Failed to get areas: {e}")
            return []

    def get_selected_todos(self) -> List[Dict[str, Any]]:
        """Retrieve currently selected todos from Things3.
        
        Returns:
            List of selected todo dictionaries
        """
        try:
            result = self.run_script_file("get_selected")
            return json.loads(result) if result else []
        except (json.JSONDecodeError, RuntimeError) as e:
            logger.error(f"Failed to get selected todos: {e}")
            return []

    def assign_project(self, task_name: str, project_name: str) -> bool:
        """Assign a project to a task.
        
        Args:
            task_name: Name of the task
            project_name: Name of the project
            
        Returns:
            True if successful, False otherwise
        """
        script = f'''
        tell application "Things3"
            set foundTodos to to dos where name is "{task_name}"
            repeat with t in foundTodos
                set project of t to project "{project_name}"
            end repeat
        end tell
        '''
        
        try:
            self.run_script(script)
            logger.info(f"Assigned project '{project_name}' to task '{task_name}'")
            return True
        except RuntimeError as e:
            logger.error(f"Failed to assign project: {e}")
            return False

    def assign_area(self, task_name: str, area_name: str) -> bool:
        """Assign an area to a task.
        
        Args:
            task_name: Name of the task
            area_name: Name of the area
            
        Returns:
            True if successful, False otherwise
        """
        script = f'''
        tell application "Things3"
            set foundTodos to to dos where name is "{task_name}"
            repeat with t in foundTodos
                set area of t to area "{area_name}"
            end repeat
        end tell
        '''
        
        try:
            self.run_script(script)
            logger.info(f"Assigned area '{area_name}' to task '{task_name}'")
            return True
        except RuntimeError as e:
            logger.error(f"Failed to assign area: {e}")
            return False

    def set_tags(self, task_name: str, tags: List[str]) -> bool:
        """Set tags for a task.
        
        Args:
            task_name: Name of the task
            tags: List of tag names
            
        Returns:
            True if successful, False otherwise
        """
        tags_str = ', '.join(f'"{tag}"' for tag in tags)
        script = f'''
        tell application "Things3"
            set foundTodos to to dos where name is "{task_name}"
            repeat with t in foundTodos
                set tag names of t to {{{tags_str}}}
            end repeat
        end tell
        '''
        
        try:
            self.run_script(script)
            logger.info(f"Set tags {tags} for task '{task_name}'")
            return True
        except RuntimeError as e:
            logger.error(f"Failed to set tags: {e}")
            return False

    def complete_selected_todos(self) -> Dict[str, Any]:
        """Complete all currently selected todos in Things3.
        
        Returns:
            Dictionary with success status and completion details
        """
        try:
            result = self.run_script_file("complete_selected")
            response = json.loads(result) if result else {"success": False, "message": "No response"}
            
            if response.get("success"):
                logger.info(f"Successfully completed selected todos: {response.get('message')}")
            else:
                logger.warning(f"Failed to complete selected todos: {response.get('message')}")
                
            return response
        except (json.JSONDecodeError, RuntimeError) as e:
            logger.error(f"Failed to complete selected todos: {e}")
            return {"success": False, "error": str(e)}