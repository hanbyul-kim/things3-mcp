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