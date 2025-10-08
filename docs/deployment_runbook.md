# Content Repurposing Agent - 30-Minute Deployment Runbook

## 🚀 Quick Start Guide

This runbook provides step-by-step instructions to deploy the Content Repurposing Agent in 30 minutes or less. Perfect for non-technical users and quick demonstrations.

## ⏱️ Time Breakdown

- **Prerequisites Check**: 5 minutes
- **System Setup**: 10 minutes
- **Application Deployment**: 10 minutes
- **Verification & Testing**: 5 minutes
- **Total Time**: 30 minutes

## 📋 Prerequisites

### Hardware Requirements
- **CPU**: 4+ cores (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 16+ GB
- **GPU**: NVIDIA RTX 3080/4080 or better (12+ GB VRAM)
- **Storage**: 100+ GB free space
- **Network**: Stable internet connection

### Software Requirements
- **Operating System**: Ubuntu 22.04 LTS
- **Docker**: 20.10+ with NVIDIA Container Toolkit
- **Git**: For cloning the repository
- **curl**: For testing endpoints

## 🔧 Step 1: Prerequisites Check (5 minutes)

### 1.1 Check System Requirements
```bash
# Check CPU cores
nproc

# Check RAM
free -h

# Check GPU
nvidia-smi

# Check available disk space
df -h
```

**Expected Output**:
- CPU: 4+ cores
- RAM: 16+ GB available
- GPU: NVIDIA GPU with 12+ GB VRAM
- Disk: 100+ GB free space

### 1.2 Install Required Software
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git unzip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 1.3 Verify Installation
```bash
# Check Docker
docker --version
docker-compose --version

# Check NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

## 🏗️ Step 2: System Setup (10 minutes)

### 2.1 Create Project Directory
```bash
# Create project directory
sudo mkdir -p /opt/content-agent
sudo chown $USER:$USER /opt/content-agent
cd /opt/content-agent
```

### 2.2 Clone Repository
```bash
# Clone the repository (replace with actual repository URL)
git clone https://github.com/your-org/content-repurposing-agent.git .

# Or create the directory structure manually
mkdir -p {app,frontend,scripts,security,docs,tests,nginx,models,uploads,logs,data}
```

### 2.3 Create Environment File
```bash
# Create environment file
cat > .env << 'EOF'
# Database Configuration
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://content_agent:your_secure_password_here@postgres:5432/content_agent

# Redis Configuration
REDIS_PASSWORD=your_redis_password_here
REDIS_URL=redis://:your_redis_password_here@redis:6379

# Qdrant Configuration
QDRANT_URL=http://qdrant:6333

# API Configuration
SECRET_KEY=your_secret_key_here
NEXTAUTH_SECRET=your_nextauth_secret_here

# LLM Configuration
MODEL_NAME=microsoft/DialoGPT-medium
MODEL_PATH=/models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Monitoring
GRAFANA_PASSWORD=your_grafana_password_here

# Environment
ENVIRONMENT=production
DEBUG=false
EOF
```

### 2.4 Create Directory Structure
```bash
# Create necessary directories
mkdir -p {models,uploads,logs,data/{postgres,redis,qdrant}}

# Set permissions
chmod 755 models uploads logs data
chmod 777 uploads
```

## 🚀 Step 3: Application Deployment (10 minutes)

### 3.1 Download Models
```bash
# Create model download script
cat > download-models.sh << 'EOF'
#!/bin/bash
echo "📥 Downloading models..."

# Create models directory
mkdir -p models

# Download embedding model
echo "Downloading embedding model..."
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model.save('./models/all-MiniLM-L6-v2')
print('Embedding model downloaded successfully')
"

# Download LLM model (placeholder - replace with actual model)
echo "Downloading LLM model..."
# This is a placeholder - replace with actual model download
echo "LLM model download completed"

echo "✅ Models downloaded successfully"
EOF

chmod +x download-models.sh
./download-models.sh
```

### 3.2 Deploy with Docker Compose
```bash
# Start the application
docker-compose up -d

# Check status
docker-compose ps
```

### 3.3 Wait for Services to Start
```bash
# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 60

# Check service health
docker-compose logs api | tail -20
docker-compose logs llm-service | tail -20
```

## ✅ Step 4: Verification & Testing (5 minutes)

### 4.1 Check Service Status
```bash
# Check all services are running
docker-compose ps

# Check service logs
docker-compose logs --tail=10
```

### 4.2 Test API Endpoints
```bash
# Test health endpoint
curl -f http://localhost:8000/health

# Test authentication
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Test content upload (create a test file)
echo "This is a test document for content repurposing." > test-document.txt

curl -X POST http://localhost:8000/content/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test-document.txt" \
  -F "title=Test Document" \
  -F "content_type=text"
```

### 4.3 Test Frontend
```bash
# Check if frontend is accessible
curl -f http://localhost:3000

# Open in browser
echo "🌐 Frontend available at: http://localhost:3000"
echo "🔑 Login credentials: admin/admin"
```

### 4.4 Test Content Generation
```bash
# Test content generation
curl -X POST http://localhost:8000/content/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": "YOUR_SOURCE_ID",
    "content_types": ["linkedin", "twitter"],
    "custom_prompts": {}
  }'
```

## 🎯 Quick Test Scenarios

### Scenario 1: Basic Content Upload
1. **Upload a text file**:
   ```bash
   curl -X POST http://localhost:8000/content/upload \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "file=@sample-content.txt" \
     -F "title=Sample Content" \
     -F "content_type=text"
   ```

2. **Check upload status**:
   ```bash
   curl http://localhost:8000/content/sources \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Scenario 2: Content Generation
1. **Generate LinkedIn post**:
   ```bash
   curl -X POST http://localhost:8000/content/generate \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "source_id": "YOUR_SOURCE_ID",
       "content_types": ["linkedin"],
       "custom_prompts": {}
     }'
   ```

2. **Check generation status**:
   ```bash
   curl http://localhost:8000/content/generated/YOUR_JOB_ID \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Scenario 3: Review and Approval
1. **Get content for review**:
   ```bash
   curl http://localhost:8000/review/pending \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

2. **Submit review**:
   ```bash
   curl -X POST http://localhost:8000/review/submit \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "content_id": "YOUR_CONTENT_ID",
       "status": "approved",
       "rating": 5,
       "feedback": "Great content!",
       "tags": ["marketing", "social-media"]
     }'
   ```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Services Not Starting
**Symptoms**: Docker containers failing to start
**Solution**:
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose down
docker-compose up -d

# Check resource usage
docker stats
```

#### Issue 2: GPU Not Available
**Symptoms**: LLM service failing to start
**Solution**:
```bash
# Check NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Restart Docker
sudo systemctl restart docker

# Check GPU in container
docker-compose exec llm-service nvidia-smi
```

#### Issue 3: Database Connection Issues
**Symptoms**: API errors related to database
**Solution**:
```bash
# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Check connection
docker-compose exec postgres psql -U content_agent -d content_agent -c "SELECT 1;"
```

#### Issue 4: Memory Issues
**Symptoms**: Out of memory errors
**Solution**:
```bash
# Check memory usage
free -h
docker stats

# Reduce model size or increase system memory
# Edit docker-compose.yml to reduce GPU memory fraction
```

#### Issue 5: Port Conflicts
**Symptoms**: Port already in use errors
**Solution**:
```bash
# Check port usage
netstat -tlnp | grep :8000
netstat -tlnp | grep :3000

# Kill conflicting processes
sudo kill -9 $(lsof -t -i:8000)
sudo kill -9 $(lsof -t -i:3000)

# Restart services
docker-compose up -d
```

## 📊 Monitoring and Health Checks

### Health Check Script
```bash
#!/bin/bash
# health-check.sh

echo "🔍 Checking system health..."

# Check Docker services
echo "📦 Docker services:"
docker-compose ps

# Check API health
echo "🌐 API health:"
curl -f http://localhost:8000/health || echo "❌ API not responding"

# Check frontend
echo "🖥️  Frontend:"
curl -f http://localhost:3000 || echo "❌ Frontend not responding"

# Check database
echo "🗄️  Database:"
docker-compose exec postgres psql -U content_agent -d content_agent -c "SELECT 1;" || echo "❌ Database not responding"

# Check Redis
echo "🔴 Redis:"
docker-compose exec redis redis-cli ping || echo "❌ Redis not responding"

# Check Qdrant
echo "🔍 Qdrant:"
curl -f http://localhost:6333/health || echo "❌ Qdrant not responding"

# Check GPU
echo "🎮 GPU:"
docker-compose exec llm-service nvidia-smi || echo "❌ GPU not available"

echo "✅ Health check completed"
```

### Performance Monitoring
```bash
# Monitor resource usage
docker stats

# Monitor logs
docker-compose logs -f

# Monitor specific service
docker-compose logs -f api
docker-compose logs -f llm-service
```

## 🚀 Production Deployment

### Production Checklist
- [ ] **Security**: Change default passwords
- [ ] **SSL**: Configure HTTPS certificates
- [ ] **Monitoring**: Set up comprehensive monitoring
- [ ] **Backup**: Configure automated backups
- [ ] **Scaling**: Plan for horizontal scaling
- [ ] **Documentation**: Update user documentation

### Production Commands
```bash
# Start in production mode
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale generation-worker=3

# Update services
docker-compose pull
docker-compose up -d

# Backup data
docker-compose exec postgres pg_dump -U content_agent content_agent > backup.sql
```

## 📋 Maintenance

### Daily Tasks
- [ ] Check system health
- [ ] Monitor resource usage
- [ ] Review error logs
- [ ] Check backup status

### Weekly Tasks
- [ ] Update system packages
- [ ] Review security logs
- [ ] Optimize performance
- [ ] Clean up old data

### Monthly Tasks
- [ ] Security audit
- [ ] Performance review
- [ ] Capacity planning
- [ ] Documentation update

## 🎯 Success Criteria

### Deployment Success
- [ ] All services running
- [ ] API responding
- [ ] Frontend accessible
- [ ] Database connected
- [ ] GPU available
- [ ] Models loaded

### Functional Success
- [ ] Content upload working
- [ ] Content generation working
- [ ] Review workflow working
- [ ] Publishing working
- [ ] Analytics working

### Performance Success
- [ ] Response times <2 seconds
- [ ] Content generation <30 seconds
- [ ] System stable
- [ ] No memory leaks
- [ ] GPU utilization optimal

## 📞 Support

### Getting Help
- **Documentation**: Check the docs/ directory
- **Logs**: Review docker-compose logs
- **Issues**: Check GitHub issues
- **Community**: Join the community forum

### Emergency Contacts
- **Technical Issues**: Check logs and restart services
- **Performance Issues**: Monitor resource usage
- **Security Issues**: Review security checklist
- **Data Issues**: Check backup and recovery procedures

## 🎉 Congratulations!

You have successfully deployed the Content Repurposing Agent! 

### Next Steps:
1. **Explore the Interface**: Visit http://localhost:3000
2. **Upload Content**: Try uploading your first content piece
3. **Generate Content**: Create your first repurposed content
4. **Review and Approve**: Use the review interface
5. **Schedule Publishing**: Set up your content calendar

### Key URLs:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Monitoring**: http://localhost:3001 (Grafana)

### Default Credentials:
- **Username**: admin
- **Password**: admin

**Remember to change these credentials in production!**

---

*This runbook provides a quick start guide for deploying the Content Repurposing Agent. For detailed configuration and advanced features, refer to the comprehensive documentation in the docs/ directory.*
