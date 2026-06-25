@echo off
REM Build script for OpenSeismo Lite Desktop EXE
REM Creates a standalone Windows executable

echo.
echo ============================================================
echo  OpenSeismo Lite Desktop EXE Builder
echo ============================================================
echo.

REM Switch to script directory
cd /d "%~dp0"
setlocal enabledelayedexpansion

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/4] Upgrading pip...
python -m pip install --upgrade pip -q

echo [2/4] Installing dependencies...
python -m pip install -r requirements.txt -q

echo [3/4] Installing PyInstaller...
python -m pip install pyinstaller -q

echo [4/4] Building OpenSeismo Lite.exe...
python -m PyInstaller --clean -y desktop_app.spec

echo.
REM Check for the main executable
if exist "dist\OpenSeismo Lite.exe" (
    set "EXE_PATH=dist\OpenSeismo Lite.exe"
) else (
    REM Fall back to searching for any exe in dist
    for /r "dist" %%f in (*.exe) do (
        if not defined EXE_PATH (
            set "EXE_PATH=%%f"
        )
    )
)

echo.
if defined EXE_PATH (
    echo ============================================================
    echo  SUCCESS! Desktop EXE created
    echo ============================================================
    echo.
    echo Location: !EXE_PATH!
    echo.
    echo To run the application:
    echo   1. Navigate to the folder containing the executable
    echo   2. Double-click the OpenSeismo Lite executable
    echo.
    echo Features:
    echo   - Real-time earthquake monitoring
    echo   - EEW alerts (M5.0+ with global coverage)
    echo   - Tsunami warnings (Japanese siren alerts)
    echo   - Sound notifications with Web Audio API
    echo   - Live updates from USGS, ESMC, CSEM, JMA
    echo   - 70+ seismic stations worldwide
    echo.
    pause
) else (
    echo ============================================================
    echo ERROR: Build failed! EXE not found in dist folder
    echo ============================================================
    echo.
    echo Dist contents:
    dir /b /s dist 2>nul || echo (no dist folder)
    echo.
    pause
    exit /b 1
)
