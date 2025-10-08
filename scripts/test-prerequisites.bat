@echo off
REM Content Repurposing Agent - Prerequisites Test Script for Windows
REM Run this script to verify your system meets the requirements

echo 🔍 Testing system prerequisites for Content Repurposing Agent...

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as administrator
) else (
    echo ⚠️  Not running as administrator - some checks may fail
)

echo.
echo 📋 Checking system requirements...

REM Check OS version
echo 🖥️  Operating System:
ver
echo.

REM Check CPU cores
echo 🔧 CPU Cores:
for /f "tokens=2 delims==" %%i in ('wmic cpu get NumberOfCores /value') do (
    if not "%%i"=="" (
        echo %%i cores available (4+ required)
        if %%i geq 4 (
            echo ✅ CPU cores sufficient
        ) else (
            echo ❌ CPU cores insufficient
        )
    )
)
echo.

REM Check RAM
echo 💾 RAM:
for /f "tokens=2 delims==" %%i in ('wmic computersystem get TotalPhysicalMemory /value') do (
    if not "%%i"=="" (
        set /a RAM_GB=%%i/1024/1024/1024
        echo !RAM_GB!GB RAM available (16GB+ required)
        if !RAM_GB! geq 16 (
            echo ✅ RAM sufficient
        ) else (
            echo ❌ RAM insufficient
        )
    )
)
echo.

REM Check GPU
echo 🎮 GPU:
nvidia-smi >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ NVIDIA GPU detected
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
) else (
    echo ❌ NVIDIA GPU not detected or nvidia-smi not available
)
echo.

REM Check disk space
echo 💿 Disk Space:
for /f "tokens=3" %%i in ('dir /-c ^| find "bytes free"') do (
    set /a DISK_GB=%%i/1024/1024/1024
    echo !DISK_GB!GB free space (100GB+ required)
    if !DISK_GB! geq 100 (
        echo ✅ Disk space sufficient
    ) else (
        echo ❌ Disk space insufficient
    )
)
echo.

REM Check Docker
echo 🐳 Docker:
docker --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Docker installed
    docker --version
) else (
    echo ❌ Docker not installed
)
echo.

REM Check Docker Compose
echo 🐙 Docker Compose:
docker-compose --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Docker Compose installed
    docker-compose --version
) else (
    echo ❌ Docker Compose not installed
)
echo.

REM Check if Docker daemon is running
echo 🔍 Docker Daemon:
docker info >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Docker daemon is running
) else (
    echo ❌ Docker daemon is not running
)
echo.

REM Check Python
echo 🐍 Python:
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Python installed
    python --version
) else (
    echo ❌ Python not installed
)
echo.

REM Check Git
echo 📁 Git:
git --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Git installed
    git --version
) else (
    echo ❌ Git not installed
)
echo.

REM Check curl
echo 🌐 curl:
curl --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ curl installed
) else (
    echo ❌ curl not installed
)
echo.

REM Check network connectivity
echo 🌍 Network Connectivity:
ping -n 1 google.com >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Internet connectivity working
) else (
    echo ❌ Internet connectivity issues
)
echo.

echo 📊 Prerequisites Summary:
echo ========================
echo.
echo ✅ = Requirement met
echo ❌ = Requirement not met
echo ⚠️  = Warning or recommendation
echo.

echo 📋 Next steps:
echo 1. Install Docker Desktop for Windows
echo 2. Install WSL2 (Windows Subsystem for Linux)
echo 3. Install Ubuntu 22.04 in WSL2
echo 4. Run the Linux version of the scripts
echo.
echo For Windows deployment, you'll need:
echo - Docker Desktop for Windows
echo - WSL2 with Ubuntu 22.04
echo - NVIDIA drivers for WSL2
echo.
echo 📚 See docs/deployment_runbook.md for detailed instructions
echo.
pause
