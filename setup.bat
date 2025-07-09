@echo off
setlocal

:: Function to set up Python virtual environment
call :setup_venv
goto :eof

:setup_venv
:: Check if venv directory exists
if exist venv (
    echo Virtual environment already exists.
) else (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% equ 0 (
        echo Virtual environment created.
    ) else (
        echo Failed to create virtual environment.
        exit /b %errorlevel%
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    exit /b %errorlevel%
)

@REM :: Upgrade pip
@REM echo Upgrading pip...
@REM pip install --upgrade pip
@REM if %errorlevel% neq 0 (
@REM     echo Failed to upgrade pip.
@REM     exit /b %errorlevel%
@REM )

:: Install requirements
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies.
        exit /b %errorlevel%
    )
) else (
    echo requirements.txt not found. Skipping dependency installation.
)

echo ✅ Done!
exit /b 0