# Theater Project GitHub Repository Setup
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Theater Project GitHub Repository Setup" -ForegroundColor Cyan
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

# Check if GitHub CLI is installed
try {
    $ghVersion = gh --version
    Write-Host "✅ GitHub CLI found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  GitHub CLI not found. Please install from: https://cli.github.com/" -ForegroundColor Yellow
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

# Get repository name
Write-Host ""
$repoName = Read-Host "Enter repository name (e.g., theater-reservation-system)"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    Write-Host "❌ Repository name cannot be empty" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create GitHub repository
Write-Host ""
Write-Host "📤 Creating GitHub repository..." -ForegroundColor Blue
try {
    gh repo create $repoName --public --description "Theater reservation system with WhatsApp integration" --source=.
    Write-Host "✅ GitHub repository created successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not create repository automatically" -ForegroundColor Yellow
    Write-Host "Please create the repository manually at: https://github.com/new" -ForegroundColor Yellow
    Write-Host "Then run: git remote add origin https://github.com/YOUR_USERNAME/$repoName.git" -ForegroundColor Yellow
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

# Push to main branch
Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Blue
try {
    git push -u origin main
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Failed to push automatically" -ForegroundColor Yellow
    Write-Host "You may need to set up authentication or push manually" -ForegroundColor Yellow
    Write-Host "Run: git push -u origin main" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🎉 Repository setup complete!" -ForegroundColor Green
Write-Host "Repository: https://github.com/YOUR_USERNAME/$repoName" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"