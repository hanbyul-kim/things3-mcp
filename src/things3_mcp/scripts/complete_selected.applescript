tell application "Things3"
    try
        set todoList to selected to dos
        set todoCount to count of todoList
        
        if todoCount is 0 then
            return "{\"success\": false, \"message\": \"No todos selected\"}"
        end if
        
        set completedCount to 0
        set completedTitles to {}
        
        repeat with t in todoList
            try
                set completion date of t to (current date)
                set completedCount to completedCount + 1
                set end of completedTitles to (name of t)
            on error
                -- Skip this item if there's an error completing it
            end try
        end repeat
        
        if completedCount > 0 then
            return "{\"success\": true, \"completed_count\": " & completedCount & ", \"message\": \"Completed " & completedCount & " of " & todoCount & " selected todos\"}"
        else
            return "{\"success\": false, \"message\": \"Failed to complete any todos\"}"
        end if
        
    on error errMsg
        return "{\"success\": false, \"error\": \"" & errMsg & "\"}"
    end try
end tell