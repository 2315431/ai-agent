# 🪟 Getting Started with Content Repurposing Agent on Windows

## 🚀 Quick Start for Windows Users

Since you're on Windows, here are your options for running the Content Repurposing Agent:

## 🐧 Option 1: WSL2 + Ubuntu (Recommended)

### Why This is Best
- ✅ **Full GPU support** with NVIDIA drivers
- ✅ **Complete compatibility** with all features  
- ✅ **Best performance** for AI/ML workloads
- ✅ **Native Linux environment** for the application

### Quick Setup (30 minutes)
```powershell
# 1. Install WSL2 (run as Administrator)
wsl --install

# 2. Restart your computer
# 3. Install Ubuntu 22.04 from Microsoft Store
# 4. Install Docker Desktop with WSL2 backend
# 5. Install NVIDIA drivers for WSL2
```

Then in WSL2 Ubuntu:
```bash
# Clone and deploy
git clone <your-repository-url>
cd content-repurposing-agent
./scripts/test-prerequisites.sh
./scripts/deploy-and-test.sh
```

## 🐳 Option 2: Docker Desktop Only

### Limitations
- ⚠️ **Limited GPU support** (may not work properly)
- ⚠️ **Performance issues** with AI/ML workloads
- ⚠️ **Compatibility issues** with some features

### Quick Setup
```cmd
# 1. Install Docker Desktop for Windows
# 2. Enable WSL2 backend in settings
# 3. Run:
docker-compose up -d
```

## 🧪 Test Your System

### Windows Prerequisites Check
```cmd
# Run this to check your Windows system
scripts\test-prerequisites.bat
```

### Windows Deployment Guide
```cmd
# Run this for step-by-step Windows deployment
scripts\deploy-and-test.bat
```

## 📋 What You Need

### Hardware Requirements
- **CPU**: 4+ cores (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 16+ GB
- **GPU**: NVIDIA RTX 3080/4080 or better (12+ GB VRAM)
- **Storage**: 100+ GB free space

### Software Requirements
- **Windows 10/11** with WSL2 support
- **Docker Desktop** for Windows
- **NVIDIA drivers** for WSL2 (if using GPU)
- **Git** for cloning the repository

## 🎯 Recommended Approach

### For Best Results: WSL2 + Ubuntu
1. **Install WSL2**: `wsl --install`
2. **Install Ubuntu 22.04** from Microsoft Store
3. **Install Docker Desktop** with WSL2 backend
4. **Install NVIDIA drivers** for WSL2
5. **Follow Linux deployment guide** in WSL2

### Why WSL2?
- **Full GPU acceleration** for AI models
- **Complete feature compatibility**
- **Best performance** for content generation
- **Native Linux environment** for the application

## 🔧 Step-by-Step Windows Setup

### Step 1: Install WSL2
```powershell
# Open PowerShell as Administrator
wsl --install
# Restart your computer when prompted
```

### Step 2: Install Ubuntu 22.04
1. Open Microsoft Store
2. Search for "Ubuntu 22.04 LTS"
3. Install and launch
4. Set up your username and password

### Step 3: Install Docker Desktop
1. Download from: https://www.docker.com/products/docker-desktop/
2. Install with WSL2 backend enabled
3. Enable GPU support in Docker settings

### Step 4: Install NVIDIA Drivers for WSL2
1. Download from: https://developer.nvidia.com/cuda/wsl
2. Install the WSL2 CUDA driver
3. Verify with: `nvidia-smi`

### Step 5: Deploy the Application
```bash
# In WSL2 Ubuntu terminal
# Clone the repository
git clone <repository-url>
cd content-repurposing-agent

# Run prerequisites check
./scripts/test-prerequisites.sh

# Deploy and test
./scripts/deploy-and-test.sh
```

## 🧪 Testing Your Deployment

### After Deployment
Access your system at:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Monitoring**: http://localhost:3001

**Default credentials**: admin/admin

### Test the Workflow
1. **Upload Content**: Go to frontend, upload a text file
2. **Generate Content**: Create LinkedIn posts, Twitter threads, etc.
3. **Review Content**: Use the review interface to approve/reject
4. **Schedule Publishing**: Set up content calendar

## 🔧 Troubleshooting Windows Issues

### Common Issues

#### WSL2 Not Available
```powershell
# Enable WSL2
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
# Restart computer
wsl --set-default-version 2
```

#### Docker Desktop Issues
- Ensure WSL2 backend is enabled
- Check if Docker Desktop is running
- Verify WSL2 integration is enabled

#### GPU Not Working
- Install NVIDIA drivers for WSL2
- Verify with `nvidia-smi` in WSL2
- Check Docker Desktop GPU settings

### Performance Optimization

#### Docker Desktop Settings
1. **Memory**: Allocate 8GB+ RAM
2. **CPU**: Allocate 4+ CPU cores
3. **WSL2 Integration**: Enable for Ubuntu 22.04
4. **GPU Support**: Enable if available

#### WSL2 Optimization
```bash
# In WSL2 Ubuntu
# Create .wslconfig in Windows user directory
echo "[wsl2]
memory=8GB
processors=4
swap=2GB" > ~/.wslconfig
```

## 📊 Performance Comparison

| Method | GPU Support | Performance | Compatibility | Ease of Use |
|--------|-------------|-------------|---------------|-------------|
| **WSL2 + Ubuntu** | ✅ Full | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Docker Desktop** | ⚠️ Limited | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎯 Next Steps

### Immediate (Today)
1. ✅ Choose your deployment method (WSL2 recommended)
2. ✅ Install prerequisites
3. ✅ Deploy the system
4. ✅ Test basic functionality

### Short-term (This Week)
1. **Test all features** thoroughly
2. **Upload real content** and generate posts
3. **Set up monitoring** and alerts
4. **Plan production deployment**

### Long-term (This Month)
1. **Deploy to production** environment
2. **Onboard users** and provide training
3. **Monitor performance** and optimize
4. **Scale infrastructure** as needed

## 📚 Documentation

### Windows-Specific
- **Windows Deployment**: `docs/windows_deployment.md`
- **Windows Scripts**: `scripts/test-prerequisites.bat`, `scripts/deploy-and-test.bat`

### General Documentation
- **Deployment Guide**: `docs/deployment_runbook.md`
- **Testing Guide**: `docs/testing_guide.md`
- **Cost Analysis**: `docs/cost_analysis.md`
- **Business Planning**: `docs/business_criteria.md`

## 🆘 Getting Help

### If You Get Stuck
1. **Check Windows documentation**: `docs/windows_deployment.md`
2. **Run Windows scripts**: `scripts/test-prerequisites.bat`
3. **Review troubleshooting guide** in the documentation
4. **Consider WSL2** for best compatibility

### Common Solutions
- **WSL2 issues**: Check Windows features and restart
- **Docker issues**: Restart Docker Desktop
- **GPU issues**: Install NVIDIA drivers for WSL2
- **Performance issues**: Optimize Docker Desktop settings

## 🎉 Success!

Once deployed, you'll have a **complete Content Repurposing Agent** that can:

✅ **Process any content** (text, audio, video, PDF)  
✅ **Generate multiple formats** (LinkedIn, Twitter, Instagram, Newsletter)  
✅ **Handle human review** and approval  
✅ **Schedule publishing** across platforms  
✅ **Track analytics** and performance  
✅ **Scale to enterprise** levels  

## 🚀 Ready to Start?

### Quick Start Commands
```cmd
# Check your Windows system
scripts\test-prerequisites.bat

# Get deployment guidance
scripts\deploy-and-test.bat
```

### Recommended Path
1. **Install WSL2 and Ubuntu 22.04**
2. **Follow the Linux deployment guide**
3. **Enjoy your Content Repurposing Agent!**

---

*For the best experience on Windows, we strongly recommend using WSL2 + Ubuntu 22.04 for full functionality and performance.*
