#!/bin/bash

# Content Repurposing Agent - Prerequisites Test Script
# Run this script to verify your system meets the requirements

echo "🔍 Testing system prerequisites for Content Repurposing Agent..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "📋 Checking system requirements..."

# Check OS
echo "🖥️  Operating System:"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v lsb_release &> /dev/null; then
        OS_VERSION=$(lsb_release -rs)
        if [[ "$OS_VERSION" == "22.04" ]]; then
            print_status "Ubuntu 22.04 LTS detected" 0
        else
            print_warning "Ubuntu $OS_VERSION detected (22.04 recommended)"
        fi
    else
        print_warning "Linux detected but version unknown"
    fi
else
    print_warning "Non-Linux OS detected (Ubuntu 22.04 recommended)"
fi

# Check CPU cores
echo "🔧 CPU Cores:"
CPU_CORES=$(nproc)
if [ "$CPU_CORES" -ge 4 ]; then
    print_status "$CPU_CORES cores available (4+ required)" 0
else
    print_warning "$CPU_CORES cores available (4+ required)"
fi

# Check RAM
echo "💾 RAM:"
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
if [ "$RAM_GB" -ge 16 ]; then
    print_status "${RAM_GB}GB RAM available (16GB+ required)" 0
else
    print_warning "${RAM_GB}GB RAM available (16GB+ required)"
fi

# Check GPU
echo "🎮 GPU:"
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits | head -1)
    GPU_NAME=$(echo $GPU_INFO | cut -d',' -f1)
    GPU_MEMORY=$(echo $GPU_INFO | cut -d',' -f2 | tr -d ' ')
    
    if [ "$GPU_MEMORY" -ge 12000 ]; then
        print_status "NVIDIA $GPU_NAME with ${GPU_MEMORY}MB VRAM (12GB+ required)" 0
    else
        print_warning "NVIDIA $GPU_NAME with ${GPU_MEMORY}MB VRAM (12GB+ required)"
    fi
else
    print_warning "NVIDIA GPU not detected or nvidia-smi not available"
fi

# Check disk space
echo "💿 Disk Space:"
DISK_FREE=$(df -BG . | awk 'NR==2{print $4}' | sed 's/G//')
if [ "$DISK_FREE" -ge 100 ]; then
    print_status "${DISK_FREE}GB free space (100GB+ required)" 0
else
    print_warning "${DISK_FREE}GB free space (100GB+ required)"
fi

# Check Docker
echo "🐳 Docker:"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
    print_status "Docker $DOCKER_VERSION installed" 0
    
    # Check if Docker daemon is running
    if docker info &> /dev/null; then
        print_status "Docker daemon is running" 0
    else
        print_warning "Docker daemon is not running"
    fi
else
    print_warning "Docker not installed"
fi

# Check Docker Compose
echo "🐙 Docker Compose:"
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
    print_status "Docker Compose $COMPOSE_VERSION installed" 0
else
    print_warning "Docker Compose not installed"
fi

# Check NVIDIA Docker
echo "🎮 NVIDIA Docker:"
if docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi &> /dev/null; then
    print_status "NVIDIA Docker support working" 0
else
    print_warning "NVIDIA Docker support not working"
fi

# Check Python
echo "🐍 Python:"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION installed" 0
else
    print_warning "Python3 not installed"
fi

# Check Git
echo "📁 Git:"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    print_status "Git $GIT_VERSION installed" 0
else
    print_warning "Git not installed"
fi

# Check curl
echo "🌐 curl:"
if command -v curl &> /dev/null; then
    print_status "curl installed" 0
else
    print_warning "curl not installed"
fi

# Check network connectivity
echo "🌍 Network Connectivity:"
if curl -s --max-time 5 https://www.google.com &> /dev/null; then
    print_status "Internet connectivity working" 0
else
    print_warning "Internet connectivity issues"
fi

# Summary
echo ""
echo "📊 Prerequisites Summary:"
echo "========================"

# Count issues
ISSUES=0

# Check critical requirements
if [ "$CPU_CORES" -lt 4 ]; then
    echo "❌ CPU: $CPU_CORES cores (4+ required)"
    ISSUES=$((ISSUES + 1))
fi

if [ "$RAM_GB" -lt 16 ]; then
    echo "❌ RAM: ${RAM_GB}GB (16GB+ required)"
    ISSUES=$((ISSUES + 1))
fi

if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ GPU: NVIDIA GPU not detected"
    ISSUES=$((ISSUES + 1))
fi

if [ "$DISK_FREE" -lt 100 ]; then
    echo "❌ Disk: ${DISK_FREE}GB free (100GB+ required)"
    ISSUES=$((ISSUES + 1))
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker: Not installed"
    ISSUES=$((ISSUES + 1))
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose: Not installed"
    ISSUES=$((ISSUES + 1))
fi

# Final assessment
echo ""
if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}🎉 All prerequisites met! You're ready to deploy the Content Repurposing Agent.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./scripts/setup-ubuntu.sh"
    echo "2. Run: docker-compose up -d"
    echo "3. Run: ./scripts/health-check.sh"
else
    echo -e "${RED}⚠️  $ISSUES critical issues found. Please resolve these before deployment.${NC}"
    echo ""
    echo "To fix common issues:"
    echo "1. Install Docker: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh"
    echo "2. Install Docker Compose: sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"
    echo "3. Install NVIDIA Docker: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
    echo "4. Check GPU: nvidia-smi"
fi

echo ""
echo "📋 For detailed setup instructions, see:"
echo "- docs/deployment_runbook.md"
echo "- scripts/setup-ubuntu.sh"
