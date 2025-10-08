# 🚂 Railway Deployment Guide

## 🚀 Deploy Content Repurposing Agent on Railway

Railway is the easiest way to deploy your Content Repurposing Agent online with a free tier!

## 📋 Prerequisites

- GitHub account
- Railway account (free)
- Your repository on GitHub

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done)
```bash
git add .
git commit -m "Add Content Repurposing Agent"
git push origin main
```

### Step 2: Sign Up for Railway

1. **Go to**: https://railway.app
2. **Sign up** with your GitHub account
3. **Connect your repository**

### Step 3: Deploy on Railway

1. **Click "Deploy from GitHub repo"**
2. **Select your repository**
3. **Railway will auto-detect Docker**
4. **Click "Deploy"**

### Step 4: Configure Environment Variables

Add these environment variables in Railway dashboard:

```env
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

### Step 5: Add Services

In Railway dashboard, add these services:

1. **PostgreSQL** (Database)
2. **Redis** (Cache/Queue)
3. **Qdrant** (Vector Database)

### Step 6: Deploy

1. **Click "Deploy"**
2. **Wait for deployment** (5-10 minutes)
3. **Get your URL** from Railway dashboard

## 🔧 Railway-Specific Configuration

### Create `railway.json` (Optional)
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

### Update `docker-compose.yml` for Railway
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
      - DATABASE_URL=${{RAILWAY_DATABASE_URL}}
      - REDIS_URL=${{RAILWAY_REDIS_URL}}
      - QDRANT_URL=http://qdrant:6333
      - SECRET_KEY=${{SECRET_KEY}}
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=content_agent
      - POSTGRES_USER=content_agent
      - POSTGRES_PASSWORD=${{POSTGRES_PASSWORD}}
    restart: unless-stopped

  redis:
    image: redis:7.2-alpine
    command: redis-server --requirepass ${{REDIS_PASSWORD}}
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:v1.7.4
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=${{RAILWAY_PUBLIC_DOMAIN}}
    restart: unless-stopped
```

## 🧪 Testing Your Deployment

### After Deployment
1. **Get your Railway URL** from the dashboard
2. **Test the API**: `https://your-app.railway.app/health`
3. **Test the frontend**: `https://your-app.railway.app`

### Default Credentials
- **Username**: admin
- **Password**: admin

## 🔧 Troubleshooting Railway

### Common Issues

#### 1. Build Failures
- Check Docker logs in Railway dashboard
- Ensure all dependencies are in requirements.txt
- Verify Dockerfile is correct

#### 2. Database Connection Issues
- Check environment variables
- Verify PostgreSQL service is running
- Check connection string format

#### 3. Memory Issues
- Railway free tier has memory limits
- Consider upgrading to paid tier
- Optimize Docker images

### Railway Commands (CLI)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy from local
railway up

# View logs
railway logs

# Connect to database
railway connect postgres
```

## 📊 Railway Pricing

### Free Tier
- **$5 credit** per month
- **512MB RAM**
- **1GB storage**
- **Custom domains**

### Paid Tiers
- **Hobby**: $5/month
- **Pro**: $20/month
- **Team**: $99/month

## 🎯 Railway Advantages

✅ **Easy deployment** from GitHub  
✅ **Automatic HTTPS**  
✅ **Database included**  
✅ **Free tier available**  
✅ **Docker support**  
✅ **Environment variables**  
✅ **Custom domains**  

## 🚀 Quick Start Commands

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy
railway up

# 4. View logs
railway logs
```

## 🎉 Success!

Once deployed, your Content Repurposing Agent will be available at:
- **Frontend**: `https://your-app.railway.app`
- **API**: `https://your-app.railway.app/api`
- **API Docs**: `https://your-app.railway.app/docs`

## 📚 Next Steps

1. **Test the deployment**
2. **Upload sample content**
3. **Generate repurposed content**
4. **Set up custom domain** (optional)
5. **Monitor usage** and upgrade if needed

---

*Railway makes it easy to deploy your Content Repurposing Agent online with minimal configuration!*
