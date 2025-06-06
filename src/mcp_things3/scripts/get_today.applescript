tell application "Things3"
    set todayTasks to to dos of list "Today"
    set tasksJSON to "["
    set taskCount to count of todayTasks

    repeat with i from 1 to taskCount
        set t to item i of todayTasks
        set taskTitle to my jsonEscape(name of t)
        
        set taskNotes to my safeGetValue(t, notes, "")
        if taskNotes is not "" then
            set taskNotes to my jsonEscape(taskNotes)
        end if
        
        set dueDate to my safeGetValue(t, due date, "")
        if dueDate is not "" then
            set dueDate to dueDate as string
        end if
        
        set whenDate to my safeGetValue(t, activation date, "")
        if whenDate is not "" then
            set whenDate to whenDate as string
        end if
        
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