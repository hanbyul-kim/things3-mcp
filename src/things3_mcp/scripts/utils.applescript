-- Utility functions for JSON escaping and common operations

on jsonEscape(theText)
    set resultText to ""
    set textLength to length of theText
    
    repeat with i from 1 to textLength
        set currentChar to character i of theText
        set charCode to ASCII number of currentChar
        
        if charCode is 10 or charCode is 13 then
            set resultText to resultText & "\\n"
        else if charCode is 9 then
            set resultText to resultText & "\\t"
        else if charCode is 34 then
            set resultText to resultText & "\\\""
        else if charCode is 92 then
            set resultText to resultText & "\\\\"
        else
            set resultText to resultText & currentChar
        end if
    end repeat
    
    return resultText
end jsonEscape

on safeGetValue(theObject, theProperty, defaultValue)
    try
        if theProperty is "notes" then
            set theValue to notes of theObject
        else if theProperty is "due date" then
            set theValue to due date of theObject
        else if theProperty is "activation date" then
            set theValue to activation date of theObject
        else
            return defaultValue
        end if
        
        if theValue is missing value then
            return defaultValue
        else
            return theValue
        end if
    on error
        return defaultValue
    end try
end safeGetValue

on getListTasks(listName)
    tell application "Things3"
        set taskList to to dos of list listName
        set tasksJSON to "["
        set taskCount to count of taskList

        repeat with i from 1 to taskCount
            set t to item i of taskList
            set taskTitle to my jsonEscape(name of t)
            
            set taskNotes to ""
            try
                set taskNotes to notes of t
                if taskNotes is missing value then
                    set taskNotes to ""
                else
                    set taskNotes to my jsonEscape(taskNotes)
                end if
            end try
            
            set dueDate to ""
            try
                set dueDate to due date of t
                if dueDate is not missing value then
                    set dueDate to dueDate as string
                end if
            end try
            
            set whenDate to ""
            try
                set whenDate to activation date of t
                if whenDate is not missing value then
                    set whenDate to whenDate as string
                end if
            end try
            
            set tagText to ""
            try
                set tagList to tag names of t
                if tagList is not {} then
                    set tagText to tagList as string
                end if
            end try
            
            set tasksJSON to tasksJSON & "{\"title\": \"" & taskTitle & "\"," & ¬
                "\"notes\": \"" & taskNotes & "\"," & ¬
                "\"due_date\": \"" & dueDate & "\"," & ¬
                "\"when\": \"" & whenDate & "\"," & ¬
                "\"tags\": \"" & tagText & "\"}"
            
            if i is not taskCount then
                set tasksJSON to tasksJSON & ","
            end if
        end repeat
        
        set tasksJSON to tasksJSON & "]"
        return tasksJSON
    end tell
end getListTasks