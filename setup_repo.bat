@echo off
setlocal enabledelayedexpansion

REM Constants for directories
set "APP_DIR=temp_my_app"
set "DIST_DIR=%APP_DIR%\dist"
set "DIST_DIR_MAIN=%DIST_DIR%\main"
set "KEYSTORE_DIR=%APP_DIR%\keystore"
set "REPO_DIR=%APP_DIR%\repository"

echo Setting up tufup repository...

REM Initialize repository
echo.
echo Step 1: Initializing repository...
powershell -Command "(gc src\myapp\settings.py) -replace 'APP_VERSION = .*', 'APP_VERSION = \"1.0\"' | sc src\myapp\settings.py"
echo Current version in settings.py:
type src\myapp\settings.py
python repo_init.py
if errorlevel 1 (
    echo Failed to initialize repository
    exit /b 1
)

REM Create version 1.0
echo.
echo Step 2: Creating version 1.0...
if not exist "%DIST_DIR_MAIN%" mkdir "%DIST_DIR_MAIN%"
python setup.py bdist_msi --app-dir "%APP_DIR%"
if errorlevel 1 (
    echo Failed to build version 1.0
    exit /b 1
)
tufup targets add 1.0 "%DIST_DIR_MAIN%" "%KEYSTORE_DIR%"
if errorlevel 1 (
    echo Failed to add version 1.0 bundle
    exit /b 1
)

REM Update app version to 2.0.0
echo.
echo Step 3: Updating app version to 2.0.0...
powershell -Command "(gc src\myapp\settings.py) -replace 'APP_VERSION = .*', 'APP_VERSION = \"2.0\"' | sc src\myapp\settings.py"
echo Current version in settings.py:
type src\myapp\settings.py

REM Create version 2.0
echo.
echo Step 4: Creating version 2.0...
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"
python setup.py bdist_msi --app-dir "%APP_DIR%"
if errorlevel 1 (
    echo Failed to build version 2.0
    exit /b 1
)
tufup targets add 2.0 "%DIST_DIR%" "%KEYSTORE_DIR%"
if errorlevel 1 (
    echo Failed to add version 2.0 bundle
    exit /b 1
)

REM Start HTTP server
echo.
echo Step 5: Starting HTTP server...
echo Repository is now available at http://localhost:8000
echo Press Ctrl+C to stop the server
python -m http.server -d "%REPO_DIR%"

echo.
echo Repository setup complete! 