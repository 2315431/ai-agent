# 🐳 Railway Docker Configuration Fix

## 🚨 Issue: "Script start.sh not found"

Railway is trying to auto-detect the build method but can't find the right files. Since we have a `docker-compose.yml` file, we need to configure Railway to use Docker.

## 🔧 **Solution: Configure Railway for Docker**

### **Step 1: Create Railway Configuration**

Create a `railway.json` file in your project root:

```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "docker-compose up -d",
    "healthcheckPath": "/health"
  }
}
```

### **Step 2: Create Dockerfile for API**

Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY scripts/ ./scripts/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Step 3: Create requirements.txt**

Create a `requirements.txt` file:

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
qdrant-client==1.7.0
sentence-transformers==2.2.2
transformers==4.36.0
torch==2.1.0
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
requests==2.31.0
aiohttp==3.9.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

### **Step 4: Update Railway Settings**

In Railway dashboard:
1. **Go to your project**
2. **Click "Settings"**
3. **Click "Build"**
4. **Set Build Command**: `docker-compose up -d`
5. **Set Start Command**: `docker-compose up -d`
6. **Set Health Check**: `/health`

## 🚀 **Alternative: Use Railway Services**

### **Step 1: Add Services Manually**

In Railway dashboard, add these services:
1. **PostgreSQL** (Database)
2. **Redis** (Cache/Queue)
3. **Qdrant** (Vector Database)

### **Step 2: Configure Main Service**

For your main app service:
1. **Set Build Command**: `docker-compose up -d`
2. **Set Start Command**: `docker-compose up -d`
3. **Set Health Check**: `/health`

### **Step 3: Environment Variables**

Add these environment variables:
```
POSTGRES_PASSWORD=secure_password_123
DATABASE_URL=postgresql://content_agent:secure_password_123@postgres:5432/content_agent
REDIS_PASSWORD=redis_password_123
REDIS_URL=redis://:redis_password_123@redis:6379
QDRANT_URL=http://qdrant:6333
SECRET_KEY=your_secret_key_here_change_in_production
NEXTAUTH_SECRET=your_nextauth_secret_here_change_in_production
MODEL_NAME=microsoft/DialoGPT-medium
MODEL_PATH=/models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
GRAFANA_PASSWORD=grafana_password_123
ENVIRONMENT=production
DEBUG=false
```

## 🔧 **Quick Fix Commands**

### **Add Files to Your Repository**

```bash
# Add the new files
git add railway.json Dockerfile requirements.txt

# Commit the changes
git commit -m "Add Railway Docker configuration"

# Push to GitHub
git push origin master
```

### **Redeploy on Railway**

1. **Go to Railway dashboard**
2. **Click "Redeploy"**
3. **Wait for build** to complete
4. **Check logs** for any errors

## 🎯 **Alternative: Use Render Instead**

If Railway continues to have issues, try **Render** (easier for Docker):

### **Render Deployment**
1. **Go to**: https://render.com
2. **Sign up** with GitHub
3. **Connect** your repository
4. **Select "Docker"** as build method
5. **Deploy** automatically

## 🚀 **What to Do Next**

### **Option 1: Fix Railway**
1. **Add the files** above to your repository
2. **Push to GitHub**
3. **Redeploy** on Railway

### **Option 2: Use Render**
1. **Go to**: https://render.com
2. **Connect** your GitHub repository
3. **Deploy** with Docker

### **Option 3: Use DigitalOcean**
1. **Create** Ubuntu 22.04 droplet
2. **SSH** into the server
3. **Run** the deployment scripts

## 🎉 **Success!**

Once configured, your Content Repurposing Agent will be live at:
- **Frontend**: `https://your-app.railway.app`
- **API**: `https://your-app.railway.app/api`
- **API Docs**: `https://your-app.railway.app/docs`

**Default credentials**: admin/admin

---

*The easiest solution is to add the Docker configuration files and redeploy!*
