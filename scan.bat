@echo off
setlocal
set "target=%~1"
if "%target%"=="" set "target=."

if exist "%~dp0codesize.exe" (
    "%~dp0codesize.exe" "%target%"
) else (
    "%~dp0.venv\Scripts\python.exe" "%~dp0scanner.py" "%target%"
)
endlocal
