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
    set areaList to areas
    set areaJSON to "["
    set areaCount to count of areaList

    repeat with i from 1 to areaCount
        set a to item i of areaList
        set areaTitle to my jsonEscape(name of a)
        
        set areaJSON to areaJSON & "{\"title\": \"" & areaTitle & "\"}"
        
        if i is not areaCount then
            set areaJSON to areaJSON & ","
        end if
    end repeat

    set areaJSON to areaJSON & "]"
    return areaJSON
end tell