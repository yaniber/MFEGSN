@echo off
REM Setup script for MFEGSN PDF RAG System (Windows)

echo === MFEGSN PDF RAG System Setup ===
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file
echo.
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created
) else (
    echo .env file already exists
)

REM Create necessary directories
echo.
echo Ensuring directories exist...
if not exist "pdfs" mkdir pdfs
if not exist "markdown_outputs" mkdir markdown_outputs
if not exist "chroma_db" mkdir chroma_db
echo Directories created

echo.
echo === Setup Complete! ===
echo.
echo To get started:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Start the web interface:
echo    python web_interface.py
echo.
echo 3. Or run the example script:
echo    python example_usage.py
echo.
echo 4. Or start the MCP server:
echo    python mcp_server\server.py
echo.

pause
