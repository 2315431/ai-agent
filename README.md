# Content Repurposing Agent

A FastAPI-based AI content repurposing system that transforms source content into multiple formats.

## Quick Start

### Deploy to Render.com

1. **Fork this repository**
2. **Create a new Web Service on Render.com**
3. **Connect your GitHub repository**
4. **Use these settings:**
   - **Build Command:** `pip install -r requirements.minimal.txt`
   - **Start Command:** `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11

### Environment Variables (Optional)

- `OPENAI_API_KEY` - For real AI content generation
- `DATABASE_URL` - Database connection (defaults to SQLite)

### API Endpoints

- `GET /health` - Health check
- `GET /test` - Basic functionality test
- `POST /ai/generate` - AI-powered content generation
- `POST /demo/generate` - Demo content generation
- `POST /auth/login` - User authentication
- `POST /content/upload` - Upload content files
- `GET /content/sources` - List uploaded content

### Example Usage

```bash
# Test the API
curl https://your-app.onrender.com/health

# Generate content with AI
curl -X POST https://your-app.onrender.com/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your source content here",
    "type": "linkedin_post",
    "audience": "professionals",
    "tone": "professional"
  }'
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.minimal.txt

# Run the app
python -m uvicorn app.main:app --reload
```

## Features

- ✅ File upload and processing
- ✅ AI-powered content generation
- ✅ Multiple content formats (LinkedIn, Twitter, etc.)
- ✅ SQLite database (works without external DB)
- ✅ Authentication system
- ✅ RESTful API
- ✅ Deployable to cloud platforms