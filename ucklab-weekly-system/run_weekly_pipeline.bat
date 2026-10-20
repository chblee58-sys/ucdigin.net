@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ===============================================================================
echo [UCKLab] Weekly HBR-Grade AGI Intelligence Autonomous Pipeline Runner
echo ===============================================================================
echo Starting execution at %date% %time%...

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [Notice] Using system Python environment...
) else (
    echo [Notice] Activating virtual environment...
    call venv\Scripts\activate.bat
)

if not exist "data" mkdir data
if not exist "storage\charts" mkdir storage\charts
if not exist "storage\reports" mkdir storage\reports
if not exist "storage\ppt" mkdir storage\ppt
if not exist "storage\images" mkdir storage\images

set PYTHON_CMD=python
if exist "C:\Python314\python.exe" set PYTHON_CMD=C:\Python314\python.exe

echo [Step 1/2] Running Sunday 17:00 KST Post-Confirmation Website & SNS 10-Part Threads Automation...
%PYTHON_CMD% run_sunday_1700_automation.py >> data/weekly_pipeline_exec.log 2>&1

echo [Step 2/2] Running Weekly HBR Autonomous Publisher (WordPress, AIOSEO, SQLite WAL)...
%PYTHON_CMD% src/wp_publisher.py >> data/weekly_pipeline_exec.log 2>&1

if %errorlevel% equ 0 (
    echo.
    echo ===============================================================================
    echo [SUCCESS] Weekly HBR Report & SNS 10-Part Threads Published Successfully!
    echo Check log: data/weekly_pipeline_exec.log
    echo ===============================================================================
) else (
    echo.
    echo ===============================================================================
    echo [ERROR] Pipeline encountered an issue. Return code: %errorlevel%
    echo Please inspect data/weekly_pipeline_exec.log for details.
    echo ===============================================================================
)

endlocal
