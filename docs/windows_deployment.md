# Content Repurposing Agent - Windows Deployment Guide

## 🪟 Windows Deployment Options

The Content Repurposing Agent is designed for Linux/Ubuntu deployment, but you can run it on Windows using these methods:

## 🐧 Option 1: WSL2 + Ubuntu (Recommended)

### Why WSL2?
- **Full GPU support** with NVIDIA drivers
- **Complete compatibility** with all features
- **Best performance** for AI/ML workloads
- **Native Linux environment** for the application

### Prerequisites
- Windows 10/11 with WSL2 support
- NVIDIA GPU with WSL2 support
- At least 16GB RAM
- 100GB+ free disk space

### Installation Steps

#### Step 1: Install WSL2
```powershell
# Open PowerShell as Administrator
wsl --install
# Restart your computer when prompted
```

#### Step 2: Install Ubuntu 22.04
1. Open Microsoft Store
2. Search for "Ubuntu 22.04 LTS"
3. Install and launch
4. Set up your username and password

#### Step 3: Install Docker Desktop
1. Download from: https://www.docker.com/products/docker-desktop/
2. Install with WSL2 backend enabled
3. Enable GPU support in Docker settings

#### Step 4: Install NVIDIA Drivers for WSL2
1. Download from: https://developer.nvidia.com/cuda/wsl
2. Install the WSL2 CUDA driver
3. Verify with: `nvidia-smi`

#### Step 5: Deploy the Application
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

## 🐳 Option 2: Docker Desktop Only

### Limitations
- **Limited GPU support** (may not work properly)
- **Performance issues** with AI/ML workloads
- **Compatibility issues** with some features

### Installation Steps

#### Step 1: Install Docker Desktop
1. Download from: https://www.docker.com/products/docker-desktop/
2. Install with WSL2 backend enabled
3. Enable experimental features

#### Step 2: Configure for GPU Support
1. Open Docker Desktop settings
2. Go to Resources > WSL Integration
3. Enable integration with Ubuntu 22.04
4. Go to Resources > Advanced
5. Increase memory allocation to 8GB+

#### Step 3: Deploy with Docker Compose
```cmd
# In Windows Command Prompt or PowerShell
docker-compose up -d
```

## 🔧 Windows-Specific Configuration

### Environment Variables
Create a `.env` file with Windows-compatible paths:

```env
# Windows-specific configuration
POSTGRES_PASSWORD=secure_password_123
DATABASE_URL=postgresql://content_agent:secure_password_123@postgres:5432/content_agent
REDIS_PASSWORD=redis_password_123
REDIS_URL=redis://:redis_password_123@redis:6379
QDRANT_URL=http://qdrant:6333
SECRET_KEY=your_secret_key_here
NEXTAUTH_SECRET=your_nextauth_secret_here
MODEL_NAME=microsoft/DialoGPT-medium
MODEL_PATH=/models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
GRAFANA_PASSWORD=grafana_password_123
ENVIRONMENT=production
DEBUG=false
```

### Docker Compose for Windows
Create a `docker-compose.windows.yml`:

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://content_agent:${POSTGRES_PASSWORD}@postgres:5432/content_agent
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
      - QDRANT_URL=http://qdrant:6333
      - LLM_SERVICE_URL=http://llm-service:8001
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./app:/app:ro
      - ./models:/models:ro
      - ./uploads:/uploads:rw
    depends_on:
      - postgres
      - redis
      - qdrant
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=content_agent
      - POSTGRES_USER=content_agent
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:v1.7.4
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  llm-service:
    build:
      context: .
      dockerfile: Dockerfile.llm
    ports:
      - "8001:8001"
    environment:
      - MODEL_NAME=${MODEL_NAME}
      - MODEL_PATH=/models
    volumes:
      - ./models:/models:ro
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
```

## 🧪 Testing on Windows

### Prerequisites Check
```cmd
# Run the Windows prerequisites check
scripts\test-prerequisites.bat
```

### Deploy and Test
```cmd
# Run the Windows deployment guide
scripts\deploy-and-test.bat
```

### Manual Testing
```cmd
# Check if services are running
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

## 🔧 Troubleshooting Windows Issues

### Common Issues

#### 1. WSL2 Not Available
```powershell
# Enable WSL2
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
# Restart computer
wsl --set-default-version 2
```

#### 2. Docker Desktop Issues
- Ensure WSL2 backend is enabled
- Check if Docker Desktop is running
- Verify WSL2 integration is enabled

#### 3. GPU Not Working
- Install NVIDIA drivers for WSL2
- Verify with `nvidia-smi` in WSL2
- Check Docker Desktop GPU settings

#### 4. Performance Issues
- Increase Docker Desktop memory allocation
- Use WSL2 for better performance
- Consider using Linux directly

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

## 🎯 Recommendations

### For Development
- **Use WSL2 + Ubuntu** for full functionality
- **Best performance** for AI/ML workloads
- **Complete feature support**

### For Production
- **Consider Linux server** for production deployment
- **Use cloud services** (AWS, Google Cloud, Azure)
- **WSL2 for local development** only

## 🚀 Quick Start for Windows

### Option 1: WSL2 (Recommended)
```bash
# 1. Install WSL2 and Ubuntu 22.04
# 2. Install Docker Desktop with WSL2 backend
# 3. Install NVIDIA drivers for WSL2
# 4. In WSL2 Ubuntu:
git clone <repository-url>
cd content-repurposing-agent
./scripts/test-prerequisites.sh
./scripts/deploy-and-test.sh
```

### Option 2: Docker Desktop Only
```cmd
# 1. Install Docker Desktop
# 2. Enable WSL2 backend
# 3. Run:
docker-compose -f docker-compose.windows.yml up -d
```

## 📚 Additional Resources

### Documentation
- **Linux Deployment**: `docs/deployment_runbook.md`
- **Testing Guide**: `docs/testing_guide.md`
- **Cost Analysis**: `docs/cost_analysis.md`

### Windows-Specific
- **WSL2 Setup**: Microsoft WSL2 documentation
- **Docker Desktop**: Docker Desktop for Windows guide
- **NVIDIA WSL2**: NVIDIA CUDA on WSL2 guide

## 🎉 Success!

Once deployed, access your Content Repurposing Agent:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Monitoring**: http://localhost:3001

**Default credentials**: admin/admin

---

*For the best experience, we recommend using WSL2 + Ubuntu 22.04 for full functionality and performance.*
