#!/bin/bash

# Setup script for GitHub Actions workflow
# This script helps configure the repository for automatic deployment

echo "🚀 Setting up GitHub Actions workflow for Starlight Language"
echo "============================================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Please run 'git init' first."
    exit 1
fi

# Create .github/workflows directory if it doesn't exist
mkdir -p .github/workflows

echo "✅ Created .github/workflows directory"

# Check if workflows exist
if [ -f ".github/workflows/ci.yml" ]; then
    echo "✅ CI workflow already exists"
else
    echo "❌ CI workflow not found. Please ensure .github/workflows/ci.yml exists."
fi

if [ -f ".github/workflows/deploy.yml" ]; then
    echo "✅ Deploy workflow already exists"
else
    echo "❌ Deploy workflow not found. Please ensure .github/workflows/deploy.yml exists."
fi

# Check for requirements.txt
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt not found. Please ensure it exists."
fi

echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Add GitHub Actions workflows'"
echo "   git push origin main"
echo ""
echo "2. The workflows will automatically:"
echo "   - Run tests on every push/PR"
echo "   - Deploy to richardcookedanytime/StarLightOfficial on main branch pushes"
echo "   - Generate build artifacts and documentation"
echo ""
echo "3. To manually trigger deployment:"
echo "   - Go to Actions tab in your GitHub repository"
echo "   - Select 'Deploy to StarLightOfficial' workflow"
echo "   - Click 'Run workflow'"
echo ""
echo "🔧 Configuration needed:"
echo "- Ensure you have push access to richardcookedanytime/StarLightOfficial"
echo "- The GITHUB_TOKEN is automatically provided by GitHub Actions"
echo ""
echo "✨ Setup complete! Your workflows are ready to use."
