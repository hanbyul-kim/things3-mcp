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
    set projectList to projects
    set projectJSON to "["
    set projectCount to count of projectList

    repeat with i from 1 to projectCount
        set p to item i of projectList
        set projectTitle to my jsonEscape(name of p)
        
        set projectNotes to ""
        try
            set projectNotes to notes of p
            if projectNotes is missing value then
                set projectNotes to ""
            else
                set projectNotes to my jsonEscape(projectNotes)
            end if
        end try

        set projectJSON to projectJSON & "{\"title\": \"" & projectTitle & "\", \"notes\": \"" & projectNotes & "\"}"
        
        if i is not projectCount then
            set projectJSON to projectJSON & ","
        end if
    end repeat

    set projectJSON to projectJSON & "]"
    return projectJSON
end tell