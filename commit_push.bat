@echo off
setlocal enabledelayedexpansion

rem Find the folder with the highest number in its name
set "highestNumber=0"
set "latestFolder="

for /d %%D in (day*) do (
    set "folderName=%%~nD"
    set "folderNumber=!folderName:~3!"

    if !folderNumber! gtr !highestNumber! (
        set "highestNumber=!folderNumber!"
        set "latestFolder=%%D"
    )
)

rem Check if a folder was found
if not "%latestFolder%"=="" (
    rem Git operations
    git add "%latestFolder%\*"
    git commit -m "%latestFolder%"
    git push

    echo Git operations completed for %latestFolder%
) else (
    echo No matching folder found.
)

endlocal
