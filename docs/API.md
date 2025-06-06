# API Documentation

This document describes the available MCP tools provided by Things3 Enhanced.

## Creation Tools

### create-project

Creates a new project in Things3.

**Parameters:**
- `title` (string, required): Project title
- `notes` (string, optional): Project notes/description
- `area` (string, optional): Area to assign the project to
- `when` (string, optional): When to schedule the project
- `deadline` (string, optional): Project deadline
- `tags` (array of strings, optional): Tags to assign to the project

**Example:**
```json
{
  "title": "Website Redesign",
  "notes": "Complete redesign of company website",
  "area": "Work",
  "deadline": "2024-12-31",
  "tags": ["urgent", "design"]
}
```

### create-todo

Creates a new todo item in Things3.

**Parameters:**
- `title` (string, required): Todo title
- `notes` (string, optional): Todo notes/description
- `when` (string, optional): When to schedule the todo
- `deadline` (string, optional): Todo deadline
- `checklist_items` (array of strings, optional): Checklist items for the todo
- `tags` (array of strings, optional): Tags to assign to the todo
- `list` (string, optional): Project/list name to add the todo to
- `heading` (string, optional): Heading within the project

**Example:**
```json
{
  "title": "Review design mockups",
  "notes": "Check the new homepage designs",
  "when": "today",
  "list": "Website Redesign",
  "tags": ["review"],
  "checklist_items": ["Check homepage", "Review navigation", "Validate colors"]
}
```

## View Tools

### view-inbox

Retrieves all todos from the Things3 inbox.

**Parameters:** None

**Returns:** List of inbox todos with their details.

### view-today

Retrieves todos scheduled for today.

**Parameters:** None

**Returns:** List of today's todos with their details.

### view-projects

Retrieves all projects from Things3.

**Parameters:** None

**Returns:** List of all projects with their titles and notes.

### view-areas

Retrieves all areas from Things3.

**Parameters:** None

**Returns:** List of all areas with their titles.

### get-selected-todos

Retrieves currently selected todos in Things3.

**Parameters:** None

**Returns:** List of selected todos with full content including notes.

## Management Tools

### assign-project

Assigns a project to an existing task.

**Parameters:**
- `task` (string, required): Name of the task to modify
- `project` (string, required): Name of the project to assign

**Example:**
```json
{
  "task": "Review design mockups",
  "project": "Website Redesign"
}
```

### assign-area

Assigns an area to an existing task.

**Parameters:**
- `task` (string, required): Name of the task to modify
- `area` (string, required): Name of the area to assign

**Example:**
```json
{
  "task": "Review design mockups",
  "area": "Work"
}
```

### set-tags

Sets tags for an existing task.

**Parameters:**
- `task` (string, required): Name of the task to modify
- `tags` (array of strings, required): List of tags to set

**Example:**
```json
{
  "task": "Review design mockups",
  "tags": ["urgent", "review", "design"]
}
```

## Error Handling

All tools return error messages in case of failure. Common error scenarios:

- **AppleScript execution failure**: Things3 app is not accessible or script fails
- **X-callback-url failure**: macOS 'open' command is not available or fails
- **Task not found**: When trying to modify a task that doesn't exist
- **Invalid parameters**: When required parameters are missing or invalid

## Date Formats

When specifying dates for `when` and `deadline` parameters, you can use:

- Natural language: "today", "tomorrow", "next week"
- Relative dates: "+1d", "+2w", "+1m"
- Absolute dates: "2024-12-31", "Dec 31, 2024"
- Times: "2024-12-31 14:30", "tomorrow at 3pm"

## Notes

- All operations require Things3 to be installed and accessible on macOS
- AppleScript must be enabled for Things3
- Some operations may briefly bring Things3 to the foreground
- Task names must match exactly when using management tools