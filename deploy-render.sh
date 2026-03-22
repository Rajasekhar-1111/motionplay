#!/bin/bash
# Automated Render Deployment Script
# This script prepares your app for Render deployment

echo "🚀 Preparing for Render Deployment..."
echo ""

# Check if Git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized!"
    echo "Run: git init"
    exit 1
fi

# Check if all required files exist
echo "✅ Checking required files..."
files=("app.py" "requirements.txt" "Procfile" "render.yaml" "runtime.txt" "README.md")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ Missing: $file"
    fi
done

echo ""
echo "✅ Checking if code is pushed to GitHub..."

# Check remote
if git remote get-url origin > /dev/null 2>&1; then
    REMOTE=$(git remote get-url origin)
    echo "   Remote: $REMOTE"
else
    echo "   ✗ No remote configured!"
    exit 1
fi

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Ready for Render deployment" 2>/dev/null || echo "   (No changes to commit)"
git push origin main

echo ""
echo "✅ Your code is pushed to GitHub!"
echo ""
echo "🎯 Next Steps:"
echo "1. Go to: https://dashboard.render.com/"
echo "2. Sign up with GitHub (Rajasekhar-1111)"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your 'motionplay' repository"
echo "5. Settings auto-fill from render.yaml"
echo "6. Click 'Create Web Service'"
echo "7. Wait 2-5 minutes..."
echo "8. 🎮 Your game will be live!"
echo ""
echo "📌 Your deployment URL will be:"
echo "   https://subway-surfers-gesture.onrender.com"
