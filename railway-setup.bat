@echo off
REM Railway Deployment Setup Script
REM This script will guide you through Railway deployment

echo 🚂 Railway Deployment Setup
echo ===========================

echo.
echo 🚀 Welcome to Railway deployment!
echo.
echo Railway is the easiest way to deploy your Content Repurposing Agent online.
echo.

echo 📋 Prerequisites:
echo =================
echo ✅ GitHub account
echo ✅ Railway account (free)
echo ✅ Your repository on GitHub
echo.

echo 🚀 Step-by-Step Deployment:
echo ==========================
echo.

echo Step 1: Prepare Your Repository
echo --------------------------------
echo 1. Push your code to GitHub (if not already done)
echo    git add .
echo    git commit -m "Add Content Repurposing Agent"
echo    git push origin main
echo.

echo Step 2: Sign Up for Railway
echo ---------------------------
echo 1. Go to: https://railway.app
echo 2. Sign up with your GitHub account
echo 3. Connect your repository
echo.

echo Step 3: Deploy on Railway
echo -------------------------
echo 1. Click "Deploy from GitHub repo"
echo 2. Select your repository
echo 3. Railway will auto-detect Docker
echo 4. Click "Deploy"
echo.

echo Step 4: Configure Environment Variables
echo ---------------------------------------
echo Add these in Railway dashboard:
echo.
echo POSTGRES_PASSWORD=secure_password_123
echo DATABASE_URL=postgresql://content_agent:secure_password_123@postgres:5432/content_agent
echo REDIS_PASSWORD=redis_password_123
echo REDIS_URL=redis://:redis_password_123@redis:6379
echo QDRANT_URL=http://qdrant:6333
echo SECRET_KEY=your_secret_key_here_change_in_production
echo NEXTAUTH_SECRET=your_nextauth_secret_here_change_in_production
echo MODEL_NAME=microsoft/DialoGPT-medium
echo MODEL_PATH=/models
echo EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
echo GRAFANA_PASSWORD=grafana_password_123
echo ENVIRONMENT=production
echo DEBUG=false
echo.

echo Step 5: Add Services
echo --------------------
echo In Railway dashboard, add these services:
echo 1. PostgreSQL (Database)
echo 2. Redis (Cache/Queue)
echo 3. Qdrant (Vector Database)
echo.

echo Step 6: Deploy
echo --------------
echo 1. Click "Deploy"
echo 2. Wait for deployment (5-10 minutes)
echo 3. Get your URL from Railway dashboard
echo.

echo 🧪 Testing Your Deployment:
echo ============================
echo.
echo After deployment:
echo 1. Get your Railway URL from the dashboard
echo 2. Test the API: https://your-app.railway.app/health
echo 3. Test the frontend: https://your-app.railway.app
echo.
echo Default credentials:
echo - Username: admin
echo - Password: admin
echo.

echo 🔧 Railway CLI Commands:
echo ========================
echo.
echo Install Railway CLI:
echo npm install -g @railway/cli
echo.
echo Login to Railway:
echo railway login
echo.
echo Deploy from local:
echo railway up
echo.
echo View logs:
echo railway logs
echo.
echo Connect to database:
echo railway connect postgres
echo.

echo 📊 Railway Pricing:
echo ==================
echo.
echo Free Tier:
echo - $5 credit per month
echo - 512MB RAM
echo - 1GB storage
echo - Custom domains
echo.
echo Paid Tiers:
echo - Hobby: $5/month
echo - Pro: $20/month
echo - Team: $99/month
echo.

echo 🎯 Railway Advantages:
echo =====================
echo.
echo ✅ Easy deployment from GitHub
echo ✅ Automatic HTTPS
echo ✅ Database included
echo ✅ Free tier available
echo ✅ Docker support
echo ✅ Environment variables
echo ✅ Custom domains
echo.

echo 🚀 Quick Start:
echo ==============
echo.
echo 1. Go to https://railway.app
echo 2. Sign up with GitHub
echo 3. Connect your repository
echo 4. Deploy automatically
echo 5. Add environment variables
echo 6. Test your deployment
echo.

echo 🎉 Success!
echo ==========
echo.
echo Once deployed, your Content Repurposing Agent will be available at:
echo - Frontend: https://your-app.railway.app
echo - API: https://your-app.railway.app/api
echo - API Docs: https://your-app.railway.app/docs
echo.

echo 📚 Next Steps:
echo ==============
echo.
echo 1. Test the deployment
echo 2. Upload sample content
echo 3. Generate repurposed content
echo 4. Set up custom domain (optional)
echo 5. Monitor usage and upgrade if needed
echo.

echo 🆘 Need Help?
echo =============
echo.
echo - Railway Documentation: https://docs.railway.app
echo - Railway Discord: https://discord.gg/railway
echo - Railway GitHub: https://github.com/railwayapp
echo.

echo 🎯 Ready to deploy?
echo.
echo Choose your next step:
echo [1] Go to Railway website
echo [2] Install Railway CLI
echo [3] View detailed documentation
echo [4] Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🌐 Opening Railway website...
    start https://railway.app
    echo.
    echo 📋 Next steps:
    echo 1. Sign up with GitHub
    echo 2. Connect your repository
    echo 3. Deploy automatically
    echo 4. Add environment variables
    echo 5. Test your deployment
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Installing Railway CLI...
    echo.
    echo Run these commands:
    echo npm install -g @railway/cli
    echo railway login
    echo railway up
    echo.
    echo 📚 For more CLI commands, see:
    echo railway --help
) else if "%choice%"=="3" (
    echo.
    echo 📚 Detailed Documentation:
    echo ========================
    echo.
    echo Available files:
    echo - railway-deployment.md
    echo - docs/online_deployment.md
    echo - docs/deployment_runbook.md
    echo.
    echo Open these files to view detailed instructions
) else if "%choice%"=="4" (
    echo.
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please run the script again.
)

echo.
echo 🚂 Happy deploying with Railway!
echo.
pause
