@echo off
echo ============================================
echo Theater Project GitHub Repository Setup
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

REM Check if GitHub CLI is installed
where gh >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  GitHub CLI not found. Installing...
    echo Please install GitHub CLI from: https://cli.github.com/
    echo After installation, run this script again.
    pause
    exit /b 1
)

echo ✅ GitHub CLI found

REM Initialize git repository
echo.
echo 📁 Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize Git repository
    pause
    exit /b 1
)

REM Add remote origin (you'll need to create the repo first)
echo.
echo 🔗 Please create a GitHub repository first, then enter the repository name:
set /p repo_name="Enter repository name: "

echo.
echo 📤 Setting up remote repository...
gh repo create %repo_name% --public --description "Theater reservation system with WhatsApp integration" --source=.
if %errorlevel% neq 0 (
    echo ⚠️  Could not create repository automatically
    echo Please create the repository manually at: https://github.com/new
    echo Then run: git remote add origin https://github.com/YOUR_USERNAME/%repo_name%.git
    pause
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

REM Commit
echo.
echo 💾 Creating initial commit...
git commit -m "Initial production deployment"
if %errorlevel% neq 0 (
    echo ❌ Failed to commit
    pause
    exit /b 1
)

REM Push to main branch
echo.
echo 🚀 Pushing to GitHub...
git push -u origin main
if %errorlevel% neq 0 (
    echo ⚠️  Failed to push automatically
    echo You may need to set up authentication or push manually
    echo Run: git push -u origin main
    pause
) else (
    echo ✅ Successfully pushed to GitHub!
)

echo.
echo ============================================
echo 🎉 Repository setup complete!
echo Repository: https://github.com/YOUR_USERNAME/%repo_name%
echo ============================================
pause