"""X-callback-url handler for Things3 creation operations."""

import subprocess
import urllib.parse
from typing import Any, Dict, List, Optional

from loguru import logger


class XCallbackHandler:
    """Handles x-callback-url execution for Things3 item creation."""

    @staticmethod
    def call_url(url: str) -> bool:
        """Execute an x-callback-url using the macOS 'open' command.
        
        Args:
            url: The x-callback-url to execute
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            RuntimeError: If the 'open' command is not found or fails
        """
        try:
            result = subprocess.run(
                ['open', url],
                check=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            logger.debug(f"X-callback URL executed successfully: {url}")
            return True
        except FileNotFoundError:
            logger.error("'open' command not found - this requires macOS")
            raise RuntimeError("X-callback-url execution requires macOS")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute x-callback-url: {e.stderr}")
            raise RuntimeError(f"X-callback-url execution failed: {e.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("X-callback-url execution timed out")
            raise RuntimeError("X-callback-url execution timed out")

    def create_project(
        self,
        title: str,
        notes: Optional[str] = None,
        area: Optional[str] = None,
        when: Optional[str] = None,
        deadline: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Create a new project in Things3.
        
        Args:
            title: Project title (required)
            notes: Project notes
            area: Area to assign the project to
            when: When to schedule the project
            deadline: Project deadline
            tags: List of tags to assign
            
        Returns:
            True if successful, False otherwise
        """
        params = {"title": title}
        
        if notes:
            params["notes"] = notes
        if area:
            params["area"] = area
        if when:
            params["when"] = when
        if deadline:
            params["deadline"] = deadline
        if tags:
            params["tags"] = ",".join(tags)
            
        url = self._build_url("things:///add-project", params)
        
        try:
            success = self.call_url(url)
            if success:
                logger.info(f"Created project: {title}")
            return success
        except RuntimeError as e:
            logger.error(f"Failed to create project '{title}': {e}")
            return False

    def create_todo(
        self,
        title: str,
        notes: Optional[str] = None,
        when: Optional[str] = None,
        deadline: Optional[str] = None,
        checklist_items: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        list_name: Optional[str] = None,
        heading: Optional[str] = None
    ) -> bool:
        """Create a new todo in Things3.
        
        Args:
            title: Todo title (required)
            notes: Todo notes
            when: When to schedule the todo
            deadline: Todo deadline
            checklist_items: List of checklist items
            tags: List of tags to assign
            list_name: Name of the list/project to add to
            heading: Heading within the project
            
        Returns:
            True if successful, False otherwise
        """
        params = {"title": title}
        
        if notes:
            params["notes"] = notes
        if when:
            params["when"] = when
        if deadline:
            params["deadline"] = deadline
        if checklist_items:
            params["checklist-items"] = "\n".join(checklist_items)
        if tags:
            params["tags"] = ",".join(tags)
        if list_name:
            params["list"] = list_name
        if heading:
            params["heading"] = heading
            
        url = self._build_url("things:///add", params)
        
        try:
            success = self.call_url(url)
            if success:
                logger.info(f"Created todo: {title}")
            return success
        except RuntimeError as e:
            logger.error(f"Failed to create todo '{title}': {e}")
            return False

    def _build_url(self, base_url: str, params: Dict[str, Any]) -> str:
        """Build a properly encoded x-callback-url.
        
        Args:
            base_url: Base URL scheme
            params: Parameters to encode
            
        Returns:
            Properly encoded URL string
        """
        encoded_params = []
        for key, value in params.items():
            if value is not None:
                encoded_value = urllib.parse.quote(str(value))
                encoded_params.append(f"{key}={encoded_value}")
        
        if encoded_params:
            url = f"{base_url}?{'&'.join(encoded_params)}"
        else:
            url = base_url
            
        logger.debug(f"Built URL: {url}")
        return url