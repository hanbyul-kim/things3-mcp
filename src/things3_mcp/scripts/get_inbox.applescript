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

tell application "Things3"
    set inboxTasks to to dos of list "Inbox"
    set tasksJSON to "["
    set taskCount to count of inboxTasks

    repeat with i from 1 to taskCount
        set t to item i of inboxTasks
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
        
        set tasksJSON to tasksJSON & "{\"title\": \"" & taskTitle & "\"," & ¡þ
            "\"notes\": \"" & taskNotes & "\"," & ¡þ
            "\"due_date\": \"" & dueDate & "\"," & ¡þ
            "\"when\": \"" & whenDate & "\"," & ¡þ
            "\"tags\": \"" & tagText & "\"}"
        
        if i is not taskCount then
            set tasksJSON to tasksJSON & ","
        end if
    end repeat
    
    set tasksJSON to tasksJSON & "]"
    return tasksJSON
end tell