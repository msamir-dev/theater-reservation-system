# GitHub Repository Setup Guide

Since Git and GitHub CLI are not installed on this system, please follow these steps on your local machine to upload this project to GitHub.

## Prerequisites
1. **Git**: Download and install from https://git-scm.com/downloads
2. **GitHub CLI** (optional but recommended): Download from https://cli.github.com/
3. **GitHub Account**: Create at https://github.com if you don't have one

## Method 1: Using the Setup Scripts (Recommended)

### Option A: Batch Script (Windows Command Prompt)
```cmd
cd c:\Users\lenovo\Desktop\المسرحية
setup_github_repo.bat
```

### Option B: PowerShell Script (Windows PowerShell)
```powershell
cd "c:\Users\lenovo\Desktop\المسرحية"
.\setup_github_repo.ps1
```

## Method 2: Manual Setup

### Step 1: Initialize Git Repository
```bash
cd "c:\Users\lenovo\Desktop\المسرحية"
git init
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Enter repository name (suggested: `theater-reservation-system`)
3. Add description: "Theater reservation system with WhatsApp integration"
4. Make it **Public**
5. **Don't** initialize with README (we already have files)
6. Click "Create repository"

### Step 3: Configure Git and Push
```bash
# Add remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Add all files
git add .

# Create initial commit
git commit -m "Initial production deployment"

# Push to main branch
git push -u origin main
```

## Repository Name Suggestions
Please provide a name for your repository. Here are some suggestions:
- `theater-reservation-system`
- `theater-booking-system`
- `municipal-theater-reservations`
- `theater-seat-booking`
- `whatsapp-theater-booking`

## What Will Be Included
✅ All Python files (app.py, routes, models, config)
✅ Templates (HTML files)
✅ Static files (CSS, JavaScript, images)
✅ Configuration files
✅ Documentation (README.md)
✅ Requirements file

## What Will Be Excluded (by .gitignore)
❌ Virtual environment (`venv/`)
❌ Python cache files (`__pycache__/`, `*.pyc`)
❌ Environment variables (`.env`)
❌ Database files (`*.db`)
❌ Temporary QR codes (`static/temp_qr/`)

## Next Steps After Upload
1. **Share the repository**: Send the GitHub URL to others
2. **Set up deployment**: Consider platforms like Heroku, PythonAnywhere, or DigitalOcean
3. **Configure environment variables**: Set up production environment variables
4. **Database setup**: Configure production database
5. **WhatsApp integration**: Set up production WhatsApp Business API

## Troubleshooting
- **Authentication issues**: Set up GitHub personal access token
- **Large files**: Consider using Git LFS for large assets
- **Permission errors**: Ensure you have write access to the repository

Please provide the repository name you'd like to use, and I'll prepare the final setup commands for you!