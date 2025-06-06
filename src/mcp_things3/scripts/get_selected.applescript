tell application "Things3"
    set todoList to selected to dos
    set todoJSON to "["
    set todoCount to count of todoList

    repeat with i from 1 to todoCount
        set t to item i of todoList
        set todoTitle to my jsonEscape(name of t)
        
        set todoNotes to my safeGetValue(t, notes, "")
        if todoNotes is not "" then
            set todoNotes to my jsonEscape(todoNotes)
        end if

        set todoJSON to todoJSON & "{\"title\": \"" & todoTitle & "\"," & ¬
            "\"notes\": \"" & todoNotes & "\"}"

        if i is not todoCount then
            set todoJSON to todoJSON & ","
        end if
    end repeat

    set todoJSON to todoJSON & "]"
    return todoJSON
end tell