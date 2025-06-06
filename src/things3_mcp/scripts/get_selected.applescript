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
    try
        set todoList to selected to dos
        set todoCount to count of todoList
        
        if todoCount is 0 then
            return "[]"
        end if
        
        set todoJSON to "["

        repeat with i from 1 to todoCount
            try
                set t to item i of todoList
                set todoTitle to my jsonEscape(name of t)
                
                set todoNotes to ""
                try
                    set todoNotes to notes of t
                    if todoNotes is missing value then
                        set todoNotes to ""
                    else
                        set todoNotes to my jsonEscape(todoNotes)
                    end if
                end try

                set todoJSON to todoJSON & "{\"title\": \"" & todoTitle & "\"," & ¬
                    "\"notes\": \"" & todoNotes & "\"}"

                if i is not todoCount then
                    set todoJSON to todoJSON & ","
                end if
            on error
                -- Skip this item if there's an error processing it
            end try
        end repeat

        set todoJSON to todoJSON & "]"
        return todoJSON
    on error errMsg
        return "{\"error\": \"" & errMsg & "\"}"
    end try
end tell