@echo off
REM Content Repurposing Agent - Complete Deploy and Test Script for Windows
REM This script will guide you through deployment on Windows

echo 🚀 Content Repurposing Agent - Windows Deployment Guide
echo =====================================================

echo.
echo ⚠️  IMPORTANT: This system is designed for Linux/Ubuntu deployment
echo.
echo For Windows, you have two options:
echo.
echo 1. 🐧 WSL2 + Ubuntu 22.04 (Recommended)
echo    - Install WSL2 with Ubuntu 22.04
echo    - Run the Linux scripts inside WSL2
echo    - Best performance and compatibility
echo.
echo 2. 🐳 Docker Desktop for Windows
echo    - Install Docker Desktop
echo    - Run containers directly on Windows
echo    - May have GPU limitations
echo.

echo 📋 Prerequisites for Windows Deployment:
echo ========================================
echo.
echo ✅ Required:
echo    - Windows 10/11 with WSL2 support
echo    - Docker Desktop for Windows
echo    - NVIDIA GPU with WSL2 support
echo    - At least 16GB RAM
echo    - 100GB+ free disk space
echo.

echo 🔧 Installation Steps:
echo =====================
echo.
echo Step 1: Install WSL2
echo   1. Open PowerShell as Administrator
echo   2. Run: wsl --install
echo   3. Restart your computer
echo   4. Set up Ubuntu 22.04
echo.
echo Step 2: Install Docker Desktop
echo   1. Download from: https://www.docker.com/products/docker-desktop/
echo   2. Install with WSL2 backend enabled
echo   3. Enable GPU support in settings
echo.
echo Step 3: Install NVIDIA drivers for WSL2
echo   1. Download from: https://developer.nvidia.com/cuda/wsl
echo   2. Install the WSL2 CUDA driver
echo   3. Verify with: nvidia-smi
echo.
echo Step 4: Clone and deploy
echo   1. In WSL2 Ubuntu, clone the repository
echo   2. Run: ./scripts/test-prerequisites.sh
echo   3. Run: ./scripts/deploy-and-test.sh
echo.

echo 🐳 Alternative: Docker Desktop Only
echo ===================================
echo.
echo If you prefer to use Docker Desktop without WSL2:
echo.
echo 1. Install Docker Desktop for Windows
echo 2. Enable WSL2 backend in Docker settings
echo 3. Create a docker-compose.yml for Windows
echo 4. Note: GPU support may be limited
echo.

echo 📚 Detailed Instructions:
echo ========================
echo.
echo For complete Windows deployment instructions, see:
echo - docs/deployment_runbook.md
echo - docs/windows_deployment.md (coming soon)
echo.

echo 🆘 Getting Help:
echo ================
echo.
echo If you need help with Windows deployment:
echo 1. Check the documentation in docs/
echo 2. Review the troubleshooting guide
echo 3. Consider using WSL2 for best compatibility
echo.

echo 🎯 Recommended Approach:
echo =======================
echo.
echo For the best experience, we recommend:
echo 1. Install WSL2 with Ubuntu 22.04
echo 2. Use the Linux deployment scripts
echo 3. This provides full GPU support and compatibility
echo.

echo 📋 Next Steps:
echo ==============
echo.
echo 1. Install WSL2 and Ubuntu 22.04
echo 2. Install Docker Desktop with WSL2 backend
echo 3. Install NVIDIA drivers for WSL2
echo 4. Clone the repository in WSL2
echo 5. Run the Linux deployment scripts
echo.

echo 🚀 Ready to proceed?
echo.
echo Choose your deployment method:
echo [1] WSL2 + Ubuntu (Recommended)
echo [2] Docker Desktop only
echo [3] View detailed documentation
echo [4] Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🐧 WSL2 + Ubuntu Deployment
    echo ==========================
    echo.
    echo 1. Install WSL2: wsl --install
    echo 2. Install Ubuntu 22.04 from Microsoft Store
    echo 3. Install Docker Desktop with WSL2 backend
    echo 4. Install NVIDIA drivers for WSL2
    echo 5. In WSL2, run: ./scripts/test-prerequisites.sh
    echo 6. In WSL2, run: ./scripts/deploy-and-test.sh
    echo.
    echo 📚 See docs/deployment_runbook.md for detailed steps
) else if "%choice%"=="2" (
    echo.
    echo 🐳 Docker Desktop Deployment
    echo ===========================
    echo.
    echo 1. Install Docker Desktop for Windows
    echo 2. Enable WSL2 backend in settings
    echo 3. Note: GPU support may be limited
    echo 4. Use docker-compose.yml directly
    echo.
    echo ⚠️  Warning: GPU support may not work properly
    echo    Consider using WSL2 for full functionality
) else if "%choice%"=="3" (
    echo.
    echo 📚 Documentation
    echo ================
    echo.
    echo Available documentation:
    echo - docs/deployment_runbook.md
    echo - docs/testing_guide.md
    echo - docs/cost_analysis.md
    echo - docs/business_criteria.md
    echo - security/security_checklist.md
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
echo 📋 Summary:
echo ==========
echo.
echo The Content Repurposing Agent is designed for Linux/Ubuntu deployment.
echo For Windows, we recommend using WSL2 with Ubuntu 22.04.
echo.
echo This provides:
echo ✅ Full GPU support
echo ✅ Complete compatibility
echo ✅ Best performance
echo ✅ All features working
echo.
echo 🎯 Ready to get started?
echo 1. Install WSL2 and Ubuntu 22.04
echo 2. Follow the Linux deployment guide
echo 3. Enjoy your Content Repurposing Agent!
echo.
pause
