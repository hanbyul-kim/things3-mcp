tell application "Things3"
    set projectList to projects
    set projectJSON to "["
    set projectCount to count of projectList

    repeat with i from 1 to projectCount
        set p to item i of projectList
        set projectTitle to my jsonEscape(name of p)
        
        set projectNotes to my safeGetValue(p, notes, "")
        if projectNotes is not "" then
            set projectNotes to my jsonEscape(projectNotes)
        end if

        set projectJSON to projectJSON & "{\"title\": \"" & projectTitle & "\", \"notes\": \"" & projectNotes & "\"}"
        
        if i is not projectCount then
            set projectJSON to projectJSON & ","
        end if
    end repeat

    set projectJSON to projectJSON & "]"
    return projectJSON
end tell