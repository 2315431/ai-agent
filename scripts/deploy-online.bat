@echo off
REM Content Repurposing Agent - Online Deployment Options
REM This script will guide you through online deployment options

echo 🌐 Content Repurposing Agent - Online Deployment Options
echo =======================================================

echo.
echo 🚀 Available Online Deployment Options:
echo.

echo 1. 🐳 Railway (Easiest - Free tier available)
echo    - Free tier with automatic deployment
echo    - Easy Docker deployment
echo    - Automatic HTTPS
echo    - Database included
echo.

echo 2. ☁️ DigitalOcean (Full control - $5/month)
echo    - Ubuntu 22.04 droplet
echo    - Full GPU support
echo    - Complete functionality
echo    - SSH access
echo.

echo 3. 🤖 Google Colab (Free testing)
echo    - Free GPU access
echo    - Jupyter notebook environment
echo    - Test individual components
echo    - No permanent hosting
echo.

echo 4. 📚 Hugging Face Spaces (Free hosting)
echo    - Free hosting with Gradio
echo    - Community sharing
echo    - Easy deployment
echo    - Limited functionality
echo.

echo 5. 🚀 Render (Simple deployment)
echo    - Free tier available
echo    - Docker support
echo    - Automatic scaling
echo    - PostgreSQL included
echo.

echo 6. 🎯 Fly.io (GPU support)
echo    - Free tier available
echo    - GPU support
echo    - Global deployment
echo    - Docker support
echo.

echo 📋 Choose your deployment method:
echo.
echo [1] Railway (Easiest)
echo [2] DigitalOcean (Full control)
echo [3] Google Colab (Free testing)
echo [4] Hugging Face Spaces (Free hosting)
echo [5] Render (Simple)
echo [6] Fly.io (GPU support)
echo [7] View detailed documentation
echo [8] Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    echo.
    echo 🐳 Railway Deployment
    echo ====================
    echo.
    echo 1. Sign up at railway.app
    echo 2. Connect your GitHub repository
    echo 3. Railway will auto-detect Docker
    echo 4. Deploy automatically
    echo.
    echo 📚 Commands:
    echo npm install -g @railway/cli
    echo railway login
    echo railway up
    echo.
    echo 🌐 Visit: https://railway.app
) else if "%choice%"=="2" (
    echo.
    echo ☁️ DigitalOcean Deployment
    echo ==========================
    echo.
    echo 1. Create Ubuntu 22.04 droplet ($5/month)
    echo 2. SSH into server: ssh root@your-server-ip
    echo 3. Clone repository: git clone <repository-url>
    echo 4. Run deployment: ./scripts/deploy-and-test.sh
    echo.
    echo 🌐 Visit: https://digitalocean.com
    echo 💰 Cost: $5-20/month
) else if "%choice%"=="3" (
    echo.
    echo 🤖 Google Colab Testing
    echo =======================
    echo.
    echo 1. Open Google Colab
    echo 2. Create new notebook
    echo 3. Install dependencies
    echo 4. Test individual components
    echo.
    echo 📚 Code:
    echo !git clone <repository-url>
    echo !pip install -r requirements.txt
    echo !python test_components.py
    echo.
    echo 🌐 Visit: https://colab.research.google.com
    echo 💰 Cost: Free
) else if "%choice%"=="4" (
    echo.
    echo 📚 Hugging Face Spaces
    echo =====================
    echo.
    echo 1. Sign up at huggingface.co
    echo 2. Create new Space
    echo 3. Upload your code
    echo 4. Deploy with Gradio
    echo.
    echo 📚 Example:
    echo import gradio as gr
    echo interface = gr.Interface(...)
    echo interface.launch()
    echo.
    echo 🌐 Visit: https://huggingface.co/spaces
    echo 💰 Cost: Free
) else if "%choice%"=="5" (
    echo.
    echo 🚀 Render Deployment
    echo ===================
    echo.
    echo 1. Sign up at render.com
    echo 2. Connect GitHub repository
    echo 3. Select Docker as build method
    echo 4. Add environment variables
    echo 5. Deploy automatically
    echo.
    echo 🌐 Visit: https://render.com
    echo 💰 Cost: Free tier available
) else if "%choice%"=="6" (
    echo.
    echo 🎯 Fly.io Deployment
    echo ===================
    echo.
    echo 1. Sign up at fly.io
    echo 2. Install Fly CLI
    echo 3. Create fly.toml configuration
    echo 4. Deploy with fly deploy
    echo.
    echo 📚 Commands:
    echo curl -L https://fly.io/install.sh | sh
    echo fly auth login
    echo fly deploy
    echo.
    echo 🌐 Visit: https://fly.io
    echo 💰 Cost: Free tier available
) else if "%choice%"=="7" (
    echo.
    echo 📚 Detailed Documentation
    echo ========================
    echo.
    echo Available documentation:
    echo - docs/online_deployment.md
    echo - docs/deployment_runbook.md
    echo - docs/windows_deployment.md
    echo - GETTING_STARTED_WINDOWS.md
    echo.
    echo Open these files to view detailed instructions
) else if "%choice%"=="8" (
    echo.
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please run the script again.
)

echo.
echo 🎯 Quick Start Recommendations:
echo =============================
echo.
echo For FREE testing:
echo - Google Colab (test components)
echo - Hugging Face Spaces (simple hosting)
echo - Railway (full system, limited GPU)
echo.
echo For FULL functionality:
echo - DigitalOcean ($5/month)
echo - Fly.io (GPU support)
echo - AWS/GCP/Azure (enterprise)
echo.
echo 💡 Pro tip: Start with Railway for quick testing,
echo then move to DigitalOcean for full functionality!
echo.
pause
