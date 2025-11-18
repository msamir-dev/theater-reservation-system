@echo off
echo ============================================
echo Theater Project GitHub Upload Script
echo Repository: theater-reservation-system
echo ============================================
echo.

REM Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git found

REM Initialize git repository
echo.
echo 📁 Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize Git repository
    pause
    exit /b 1
)

echo ✅ Git repository initialized

REM Configure git user (optional - will use global config if set)
echo.
echo 👤 Configuring Git user...
git config user.name "Theater System" 2>nul
git config user.email "theater@system.com" 2>nul

REM Add .gitignore if not exists
if not exist ".gitignore" (
    echo 📄 Creating .gitignore file...
    echo venv/ > .gitignore
    echo __pycache__/ >> .gitignore
    echo *.db >> .gitignore
    echo .env >> .gitignore
    echo *.pyc >> .gitignore
    echo static/temp_qr/ >> .gitignore
)

REM Add all files
echo.
echo 📋 Adding files to staging...
git add .
if %errorlevel% neq 0 (
    echo ❌ Failed to add files
    pause
    exit /b 1
)

echo ✅ Files added to staging

REM Commit
echo.
echo 💾 Creating initial commit...
git commit -m "Initial production deployment"
if %errorlevel% neq 0 (
    echo ❌ Failed to commit
    pause
    exit /b 1
)

echo ✅ Initial commit created

REM Create GitHub repository
echo.
echo 🌐 Creating GitHub repository...
echo Please make sure you are logged into GitHub CLI (gh auth login)
echo Creating repository: theater-reservation-system

gh repo create theater-reservation-system --public --description "Theater reservation system with WhatsApp integration" --source=. --remote=origin --push

if %errorlevel% neq 0 (
    echo ⚠️  Could not create repository automatically
    echo Please create the repository manually at: https://github.com/new
    echo Then run the following commands:
    echo.
    echo git remote add origin https://github.com/YOUR_USERNAME/theater-reservation-system.git
    echo git push -u origin main
    pause
    exit /b 1
)

echo ✅ Repository created and code pushed successfully!
echo.
echo ============================================
echo 🎉 SUCCESS! Your project is now on GitHub!
echo Repository: https://github.com/YOUR_USERNAME/theater-reservation-system
echo ============================================
pause