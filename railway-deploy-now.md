# 🚂 Deploy Your Content Repurposing Agent to Railway

## 🎯 Your Repository is Ready!

**Repository**: https://github.com/2315431/ai-agent

## 🚀 Quick Deployment Steps

### Step 1: Go to Railway
1. **Open**: https://railway.app
2. **Sign up** with your GitHub account
3. **Click "Deploy from GitHub repo"**

### Step 2: Connect Your Repository
1. **Search for**: `2315431/ai-agent`
2. **Select your repository**
3. **Click "Deploy"**

### Step 3: Railway Auto-Detection
Railway will automatically:
- ✅ Detect your `docker-compose.yml`
- ✅ Set up the services
- ✅ Configure the deployment

### Step 4: Add Environment Variables
In Railway dashboard, go to **Variables** tab and add:

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
2. **Wait 5-10 minutes**
3. **Get your URL** from Railway dashboard

## 🧪 Test Your Deployment

### After Deployment
Your app will be available at:
- **Frontend**: `https://your-app.railway.app`
- **API**: `https://your-app.railway.app/api`
- **API Docs**: `https://your-app.railway.app/docs`

### Default Credentials
- **Username**: admin
- **Password**: admin

## 🔧 Railway CLI (Optional)

If you want to use the CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up

# View logs
railway logs
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

## 🎯 What Happens Next?

1. **Railway builds** your Docker containers
2. **Services start** (PostgreSQL, Redis, Qdrant)
3. **Your app deploys** automatically
4. **You get a URL** to access your app
5. **Start testing** your Content Repurposing Agent!

## 🚀 Ready to Deploy?

**Go to**: https://railway.app

**Steps**:
1. Sign up with GitHub
2. Connect `2315431/ai-agent`
3. Add environment variables
4. Add services (PostgreSQL, Redis, Qdrant)
5. Deploy!

**Your Content Repurposing Agent will be live in minutes!** 🎉
