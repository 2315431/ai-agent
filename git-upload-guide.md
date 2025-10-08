# 📤 Upload to GitHub and Deploy to Railway

## 🚀 Complete Guide: From Local to Railway

### Step 1: Initialize Git (if not already done)
```bash
# Check if git is already initialized
git status

# If not initialized, run:
git init
```

### Step 2: Add All Files
```bash
# Add all files to git
git add .

# Check what files are added
git status
```

### Step 3: Commit Your Changes
```bash
# Commit with a message
git commit -m "Add Content Repurposing Agent - Complete System"
```

### Step 4: Connect to Your GitHub Repository
```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/2315431/ai-agent.git

# Check if remote is added
git remote -v
```

### Step 5: Push to GitHub
```bash
# Push to main branch
git push -u origin main

# If you get authentication issues, use:
git push -u origin main --force
```

### Step 6: Deploy to Railway
1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Click "Deploy from GitHub repo"**
4. **Select**: `2315431/ai-agent`
5. **Click "Deploy"**

## 🔧 Troubleshooting

### If Git is Not Installed
```bash
# Download Git from: https://git-scm.com/download/win
# Or install via winget:
winget install Git.Git
```

### If Authentication Fails
```bash
# Use GitHub CLI (easier)
# Install: winget install GitHub.cli
gh auth login
gh repo create 2315431/ai-agent --public
```

### If Repository Already Exists
```bash
# Clone existing repository
git clone https://github.com/2315431/ai-agent.git
cd ai-agent

# Copy your files here
# Then commit and push
git add .
git commit -m "Update Content Repurposing Agent"
git push
```

## 🎯 Quick Commands

### Complete Upload Process
```bash
# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Add Content Repurposing Agent"

# 4. Add remote
git remote add origin https://github.com/2315431/ai-agent.git

# 5. Push to GitHub
git push -u origin main
```

### Deploy to Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Connect `2315431/ai-agent`
4. Deploy!

## 🚀 What Happens Next?

1. **Files upload** to GitHub
2. **Railway detects** your repository
3. **Docker containers** build automatically
4. **Your app deploys** to Railway
5. **You get a URL** to access your app

## 🎉 Success!

Once deployed, your Content Repurposing Agent will be live at:
- **Frontend**: `https://your-app.railway.app`
- **API**: `https://your-app.railway.app/api`
- **API Docs**: `https://your-app.railway.app/docs`

**Default credentials**: admin/admin
