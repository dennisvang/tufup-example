@echo off
setlocal enabledelayedexpansion

echo Setting up tufup repository...

REM Install requirements
echo.
echo Step 1: Installing requirements...
pip install -r requirements.txt -r requirements-dev.txt --upgrade
if errorlevel 1 (
    echo Failed to install requirements
    exit /b 1
)

REM Initialize repository
echo.
echo Step 2: Initializing repository...
python repo_init.py
if errorlevel 1 (
    echo Failed to initialize repository
    exit /b 1
)

REM Create version 1.0
echo.
echo Step 3: Creating version 1.0...
powershell -Command "(Get-Content src/myapp/settings.py) -replace 'APP_VERSION = .*', 'APP_VERSION = \"1.0\"' | Set-Content src/myapp/settings.py"
python setup.py bdist_msi
if errorlevel 1 (
    echo Failed to build version 1.0
    exit /b 1
)
python repo_add_bundle.py
if errorlevel 1 (
    echo Failed to add version 1.0 bundle
    exit /b 1
)

REM Create version 2.0
echo.
echo Step 4: Creating version 2.0...
powershell -Command "(Get-Content src/myapp/settings.py) -replace 'APP_VERSION = .*', 'APP_VERSION = \"2.0\"' | Set-Content src/myapp/settings.py"
python setup.py bdist_msi
if errorlevel 1 (
    echo Failed to build version 2.0
    exit /b 1
)
python repo_add_bundle.py
if errorlevel 1 (
    echo Failed to add version 2.0 bundle
    exit /b 1
)

REM Start HTTP server
echo.
echo Step 5: Starting HTTP server...
echo Repository is now available at http://localhost:8000
echo Press Ctrl+C to stop the server
python -m http.server -d temp_my_app/repository

echo.
echo Repository setup complete! 