# Automated Render Deployment Script for Windows PowerShell
# Run this to prepare for Render deployment

Write-Host "🚀 Preparing for Render Deployment..." -ForegroundColor Green
Write-Host ""

# Check if Git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git not initialized!" -ForegroundColor Red
    Write-Host "Run: git init"
    exit 1
}

# Check if all required files exist
Write-Host "✅ Checking required files..." -ForegroundColor Green
$files = @("app.py", "requirements.txt", "Procfile", "render.yaml", "runtime.txt", "README.md")

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "   ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Missing: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ Checking if code is pushed to GitHub..." -ForegroundColor Green

# Check remote
$remote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Remote: $remote" -ForegroundColor Cyan
} else {
    Write-Host "   ✗ No remote configured!" -ForegroundColor Red
    exit 1
}

# Push to GitHub
Write-Host ""
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git add .
git commit -m "Ready for Render deployment" 2>$null
git push origin main

Write-Host ""
Write-Host "✅ Your code is pushed to GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Green
Write-Host "1. Go to: https://dashboard.render.com/" -ForegroundColor Cyan
Write-Host "2. Sign up with GitHub (Rajasekhar-1111)" -ForegroundColor Cyan
Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor Cyan
Write-Host "4. Select your 'motionplay' repository" -ForegroundColor Cyan
Write-Host "5. Settings auto-fill from render.yaml" -ForegroundColor Cyan
Write-Host "6. Click 'Create Web Service'" -ForegroundColor Cyan
Write-Host "7. Wait 2-5 minutes..." -ForegroundColor Cyan
Write-Host "8. 🎮 Your game will be live!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Your deployment URL will be:" -ForegroundColor Yellow
Write-Host "   https://subway-surfers-gesture.onrender.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Enter to continue..."
Read-Host
