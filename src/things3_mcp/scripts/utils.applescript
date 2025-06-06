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