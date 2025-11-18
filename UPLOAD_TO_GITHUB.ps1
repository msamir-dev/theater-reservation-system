# Theater Project GitHub Upload Script
# Repository: theater-reservation-system

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Theater Project GitHub Upload Script" -ForegroundColor Cyan
Write-Host "Repository: theater-reservation-system" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/downloads" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Initialize git repository
Write-Host ""
Write-Host "📁 Initializing Git repository..." -ForegroundColor Blue
try {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to initialize Git repository" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Configure git user (optional)
Write-Host ""
Write-Host "👤 Configuring Git..." -ForegroundColor Blue
try {
    git config user.name "Theater System" 2>$null
    git config user.email "theater@system.com" 2>$null
    Write-Host "✅ Git configuration updated" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Using global Git configuration" -ForegroundColor Yellow
}

# Check and create .gitignore if needed
if (-not (Test-Path ".gitignore")) {
    Write-Host ""
    Write-Host "📄 Creating .gitignore file..." -ForegroundColor Blue
    @"
venv/
__pycache__/
*.db
.env
*.pyc
static/temp_qr/
*.log
.DS_Store
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ .gitignore created" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "📋 Adding files to staging..." -ForegroundColor Blue
try {
    git add .
    Write-Host "✅ Files added to staging" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to add files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Commit
Write-Host ""
Write-Host "💾 Creating initial commit..." -ForegroundColor Blue
try {
    git commit -m "Initial production deployment"
    Write-Host "✅ Initial commit created" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to commit" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if GitHub CLI is available
$ghAvailable = $false
try {
    $ghVersion = gh --version
    $ghAvailable = $true
    Write-Host "✅ GitHub CLI found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  GitHub CLI not found" -ForegroundColor Yellow
    Write-Host "Please install from: https://cli.github.com/" -ForegroundColor Yellow
}

# Create GitHub repository and push
if ($ghAvailable) {
    Write-Host ""
    Write-Host "🌐 Creating GitHub repository..." -ForegroundColor Blue
    Write-Host "Repository: theater-reservation-system" -ForegroundColor Cyan
    
    try {
        # Try to create and push in one command
        gh repo create theater-reservation-system --public --description "Theater reservation system with WhatsApp integration" --source=. --remote=origin --push
        Write-Host "✅ Repository created and code pushed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Could not create repository automatically" -ForegroundColor Yellow
        ManualGitHubSetup
    }
} else {
    ManualGitHubSetup
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🎉 SUCCESS! Your project setup is complete!" -ForegroundColor Green
Write-Host "Repository: https://github.com/YOUR_USERNAME/theater-reservation-system" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"

function ManualGitHubSetup {
    Write-Host ""
    Write-Host "📋 Manual Setup Instructions:" -ForegroundColor Yellow
    Write-Host "1. Create repository at: https://github.com/new" -ForegroundColor White
    Write-Host "2. Name it: theater-reservation-system" -ForegroundColor White
    Write-Host "3. Run these commands:" -ForegroundColor White
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/theater-reservation-system.git" -ForegroundColor Gray
    Write-Host "   git push -u origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ Local repository is ready!" -ForegroundColor Green
}