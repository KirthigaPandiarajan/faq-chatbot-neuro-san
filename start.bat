@echo off
REM FAQ Chatbot - Start Backend and Frontend
REM Requires: Python 3.10+, Node.js 18+

setlocal enabledelayedexpansion

echo.
echo ============================================
echo FAQ Chatbot Startup
echo ============================================
echo.

REM Set Node.js PATH
set PATH=C:\Program Files\nodejs;%PATH%

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo ✓ Python found: 
python --version

echo ✓ Node.js found:
node --version

echo.
echo Starting services...
echo.

REM Start Backend
echo Starting Backend (Port 8000)...
start "FAQ Chatbot Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend
echo Starting Frontend (Port 3000)...
start "FAQ Chatbot Frontend" cmd /k "cd frontend && npm start"

echo.
echo ============================================
echo ✓ Services Started!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the command windows to stop the services.
echo ============================================
echo.
