from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import asyncio
import uuid
import os


from datetime import datetime, timedelta
import json

from .database import get_db, engine
from .models import Base, ContentSource, GeneratedContent, ContentChunk, User, Review
from .schemas import (
    ContentSourceCreate, ContentSourceResponse, 
    GeneratedContentCreate, GeneratedContentResponse,
    ContentGenerationRequest, ReviewRequest, ReviewResponse
)
from .services import (
    ContentService, EmbeddingService, GenerationService, 
    ReviewService, SchedulingService
)
try:
    from .workers import task_queue
except ImportError:
    # Fallback for when workers module is not available
    task_queue = None
try:
    from .auth import get_current_user, create_access_token
except ImportError:
    # Fallback for when auth module is not available
    def get_current_user():
        return {"user_id": "demo_user"}
    def create_access_token(data: dict):
        return "demo_token"
from .config import settings

# Create database tables (with error handling)
try:
    from .models import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")
    print("App will continue without database functionality")

app = FastAPI(
    title="Content Repurposing Agent API",
    description="Self-hosted content repurposing system using open-source LLMs",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        # Import models to ensure they're registered with Base
        from .models import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created on startup")
    except Exception as e:
        print(f"❌ Failed to create database tables on startup: {e}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Content Repurposing Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Simple test endpoint (no auth required)
@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "Content Repurposing Agent is working!",
        "status": "success",
        "features": [
            "Content upload",
            "Content generation", 
            "Multiple formats",
            "Review system"
        ]
    }

# AI Status Check endpoint
@app.get("/ai/status")
async def ai_status():
    """Check if AI is properly configured"""
    try:
        import openai
        from .config import settings
        
        has_api_key = bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "demo-key")
        
        if has_api_key:
            try:
                # Test OpenAI connection with multiple methods
                try:
                    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                    method = "new_client"
                except Exception:
                    try:
                        openai.api_key = settings.OPENAI_API_KEY
                        client = None
                        method = "legacy_api"
                    except Exception:
                        raise Exception("Both client methods failed")
                
                return {
                    "status": "ai_ready",
                    "message": f"AI is properly configured and ready (using {method})",
                    "has_api_key": True,
                    "model": settings.LLM_MODEL,
                    "method": method
                }
            except Exception as e:
                return {
                    "status": "ai_error", 
                    "message": f"AI configured but connection failed: {str(e)}",
                    "has_api_key": True,
                    "error": str(e)
                }
        else:
            return {
                "status": "template_mode",
                "message": "Running in template mode - no OpenAI API key provided",
                "has_api_key": False,
                "fallback": "Enhanced templates"
            }
    except ImportError:
        return {
            "status": "ai_unavailable",
            "message": "OpenAI library not available",
            "has_api_key": False,
            "fallback": "Enhanced templates"
        }

# Database status endpoint
@app.get("/admin/db-status")
async def database_status():
    """Check database status"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        return {
            "status": "success",
            "database_url": str(engine.url),
            "existing_tables": existing_tables,
            "needs_init": len(existing_tables) == 0,
            "total_tables": len(Base.metadata.tables)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to check database status: {str(e)}"
        }

# Database initialization endpoint
@app.post("/admin/init-db")
async def initialize_database():
    """Initialize database tables"""
    try:
        # Import models to ensure they're registered with Base
        from .models import Base
        Base.metadata.create_all(bind=engine)
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        created_tables = inspector.get_table_names()
        
        return {
            "status": "success",
            "message": "Database tables created successfully",
            "created_tables": created_tables,
            "total_tables": len(created_tables)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create database tables: {str(e)}"
        }

# Demo content generation (no auth, no DB required)
@app.post("/demo/generate")
async def demo_generate_content(request: dict):
    """Demo content generation without authentication"""
    source_text = request.get("text", "Sample content about AI and machine learning.")
    content_type = request.get("type", "linkedin_post")
    
    # Simple content generation (mock)
    if content_type == "linkedin_post":
        generated = {
            "title": "AI Revolution in Business",
            "content": f"Based on: {source_text[:100]}...\n\n🚀 Artificial Intelligence is transforming industries worldwide. From automation to decision-making, AI is reshaping how businesses operate.\n\nKey insights:\n• Increased efficiency\n• Better decision making\n• Enhanced customer experience\n\n#AI #Business #Innovation",
            "hashtags": ["#AI", "#Business", "#Innovation", "#Technology"]
        }
    elif content_type == "twitter_thread":
        generated = {
            "thread": [
                f"🧵 Based on: {source_text[:50]}...",
                "1/ AI is revolutionizing industries across the globe 🌍",
                "2/ From healthcare to finance, AI is improving efficiency and accuracy 📊",
                "3/ The future belongs to those who embrace AI innovation 🚀"
            ],
            "hashtags": ["#AI", "#Innovation"]
        }
    else:
        generated = {
            "content": f"Generated content from: {source_text}",
            "type": content_type
        }
    
    return {
        "status": "success",
        "generated_content": generated,
        "source_preview": source_text[:100] + "..." if len(source_text) > 100 else source_text
    }

# REAL AI-powered content generation
@app.post("/ai/generate")
async def ai_generate_content(request: dict):
    """Real AI-powered content generation"""
    source_text = request.get("text", "")
    content_type = request.get("type", "linkedin_post")
    target_audience = request.get("audience", "general")
    tone = request.get("tone", "professional")
    
    if not source_text:
        return {"error": "Text is required"}
    
    try:
        # Import OpenAI (if available)
        try:
            import openai
            from .config import settings
            
            # Check if we have a valid API key
            if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "demo-key":
                raise ImportError("No OpenAI API key provided")
            
            # Try different client initialization methods
            try:
                # Method 1: Simple initialization
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e1:
                try:
                    # Method 2: With timeout only
                    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY, timeout=30.0)
                except Exception as e2:
                    try:
                        # Method 3: Legacy method
                        openai.api_key = settings.OPENAI_API_KEY
                        client = None  # Use legacy API
                    except Exception as e3:
                        raise Exception(f"All OpenAI initialization methods failed: {e1}, {e2}, {e3}")
            
            # Create prompts based on content type
            if content_type == "linkedin_post":
                system_prompt = f"""You are a professional content creator specializing in LinkedIn posts. 
                Create engaging LinkedIn content based on the source material.
                Target audience: {target_audience}
                Tone: {tone}
                
                Format your response as JSON with:
                - title: Catchy headline
                - content: Full LinkedIn post (2-3 paragraphs)
                - hashtags: Array of relevant hashtags (5-8 hashtags)
                """
                user_prompt = f"Create a LinkedIn post from this content: {source_text}"
                
            elif content_type == "twitter_thread":
                system_prompt = f"""You are a Twitter content creator. Create a Twitter thread (3-5 tweets) based on the source material.
                Target audience: {target_audience}
                Tone: {tone}
                
                Format your response as JSON with:
                - thread: Array of tweets (numbered 1/, 2/, etc.)
                - hashtags: Array of relevant hashtags
                """
                user_prompt = f"Create a Twitter thread from this content: {source_text}"
                
            else:
                system_prompt = f"""Create {content_type} content based on the source material.
                Target audience: {target_audience}
                Tone: {tone}
                """
                user_prompt = f"Create {content_type} content from: {source_text}"
            
            # Make API call to OpenAI
            if client:
                # New client method
                response = client.chat.completions.create(
                    model=settings.LLM_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=settings.LLM_TEMPERATURE,
                    max_tokens=settings.LLM_MAX_TOKENS
                )
                ai_content = response.choices[0].message.content
            else:
                # Legacy API method
                response = openai.ChatCompletion.create(
                    model=settings.LLM_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=settings.LLM_TEMPERATURE,
                    max_tokens=settings.LLM_MAX_TOKENS
                )
                ai_content = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                import json
                generated = json.loads(ai_content)
                generated["ai_powered"] = True
            except:
                # If not JSON, wrap in structure
                generated = {
                    "content": ai_content,
                    "type": content_type,
                    "ai_powered": True
                }
                
        except ImportError:
            # Fallback if OpenAI not available
            generated = create_enhanced_template(source_text, content_type, target_audience, tone)
            
    except Exception as e:
        return {
            "error": f"AI generation failed: {str(e)}",
            "fallback": create_enhanced_template(source_text, content_type, target_audience, tone)
        }
    
    return {
        "status": "success",
        "generated_content": generated,
        "source_preview": source_text[:100] + "..." if len(source_text) > 100 else source_text,
        "ai_powered": True
    }

def create_enhanced_template(source_text: str, content_type: str, audience: str, tone: str):
    """Create enhanced template-based content"""
    
    # Extract key themes from source text
    words = source_text.lower().split()
    key_themes = [word for word in words if len(word) > 4][:3]
    
    if content_type == "linkedin_post":
        return {
            "title": f"Insights on {', '.join(key_themes).title()}" if key_themes else "Professional Insights",
            "content": f"""Based on the source content about "{source_text[:50]}..."

🚀 Key takeaways for {audience}:

• {key_themes[0].title() if key_themes else 'Innovation'} is transforming how we work
• Professional growth comes from understanding these concepts
• The future belongs to those who adapt

What's your experience with {key_themes[0] if key_themes else 'these topics'}?

#Professional #Growth #Innovation #Business""",
            "hashtags": ["#Professional", "#Growth", "#Innovation", "#Business"] + [f"#{theme.title()}" for theme in key_themes]
        }
    
    elif content_type == "twitter_thread":
        return {
            "thread": [
                f"🧵 Thread on: {source_text[:40]}...",
                f"1/ {key_themes[0].title() if key_themes else 'Innovation'} is reshaping industries",
                f"2/ For {audience}, this means new opportunities ahead",
                "3/ The key is staying informed and adaptable 🚀"
            ],
            "hashtags": ["#Innovation", "#Growth"] + [f"#{theme.title()}" for theme in key_themes[:2]]
        }
    
    else:
        return {
            "content": f"Enhanced content about: {source_text}",
            "type": content_type,
            "themes": key_themes
        }

# Authentication endpoints
@app.post("/auth/login")
async def login(username: str, password: str):
    """Authenticate user and return access token"""
    # Implement your authentication logic here
    # For demo purposes, we'll use a simple approach
    if username == "admin" and password == "admin":  # Change in production!
        token = create_access_token(data={"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Content ingestion endpoints
@app.post("/content/upload")
async def upload_content(
    file: UploadFile = File(...),
    source_type: str = "text",
    title: Optional[str] = None,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process content for repurposing"""
    
    # Validate file type
    allowed_types = ["text/plain", "audio/mpeg", "audio/wav", "video/mp4", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"
    
    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Create content source record
    content_source = ContentSource(
        id=file_id,
        title=title or file.filename,
        description=description,
        source_type=source_type,
        file_path=file_path,
        file_size=len(content),
        status="uploaded",
        user_id=current_user.get("user_id", "demo_user")
    )
    
    try:
        db.add(content_source)
        db.commit()
        db.refresh(content_source)
    except Exception as e:
        # If database fails, still return the file info
        content_source.id = file_id
        content_source.status = "uploaded"
        content_source.created_at = datetime.utcnow()
        content_source.updated_at = datetime.utcnow()
        content_source.content_metadata = {}
        print(f"Database error (continuing without DB): {e}")
    
    # Queue processing job (if task_queue is available)
    try:
        if task_queue and source_type in ["audio", "video"]:
            task_queue.enqueue("process_audio", file_id, file_path)
        elif task_queue:
            task_queue.enqueue("process_text", file_id, file_path)
        else:
            print("Task queue not available - skipping job queue")
    except Exception as e:
        print(f"Task queue error (continuing without queue): {e}")
    
    # Create response manually to avoid Pydantic issues
    return {
        "id": content_source.id,
        "title": content_source.title,
        "description": content_source.description,
        "source_type": content_source.source_type,
        "file_path": content_source.file_path,
        "file_size": content_source.file_size,
        "status": content_source.status,
        "transcript": content_source.transcript,
        "metadata": content_source.content_metadata or {},
        "created_at": content_source.created_at or datetime.utcnow(),
        "updated_at": content_source.updated_at or datetime.utcnow()
    }

@app.get("/content/sources")
async def list_content_sources(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all content sources for the current user"""
    try:
        user_id = current_user.get("user_id", "demo_user")
        print(f"Looking for content sources for user: {user_id}")
        
        # Also check what users exist in the database
        all_users = db.query(ContentSource.user_id).distinct().all()
        print(f"All users in database: {[user[0] for user in all_users]}")
        
        # Get all sources (for debugging)
        all_sources = db.query(ContentSource).all()
        print(f"Total sources in database: {len(all_sources)}")
        
        sources = db.query(ContentSource).filter(
            ContentSource.user_id == user_id
        ).offset(skip).limit(limit).all()
        
        print(f"Found {len(sources)} sources for user {user_id}")
        
        # Convert to dict to avoid Pydantic issues
        return [
            {
                "id": source.id,
                "title": source.title,
                "description": source.description,
                "source_type": source.source_type,
                "file_path": source.file_path,
                "file_size": source.file_size,
                "status": source.status,
                "transcript": source.transcript,
                "metadata": source.content_metadata or {},
                "created_at": source.created_at,
                "updated_at": source.updated_at
            }
            for source in sources
        ]
    except Exception as e:
        # Return empty list if database is not available
        print(f"Database error in list_content_sources: {e}")
        return []

# Temporary debug endpoint to see all content sources
@app.get("/debug/all-sources")
async def debug_all_sources(db: Session = Depends(get_db)):
    """Debug endpoint to see all content sources"""
    try:
        all_sources = db.query(ContentSource).all()
        return [
            {
                "id": source.id,
                "title": source.title,
                "user_id": source.user_id,
                "created_at": source.created_at,
                "status": source.status
            }
            for source in all_sources
        ]
    except Exception as e:
        return {"error": str(e)}

@app.get("/content/sources/{source_id}", response_model=ContentSourceResponse)
async def get_content_source(
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific content source details"""
    source = db.query(ContentSource).filter(
        ContentSource.id == source_id,
        ContentSource.user_id == current_user.get("user_id", "demo_user")
    ).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Content source not found")
    
    return ContentSourceResponse.from_orm(source)

# Content generation endpoints
@app.post("/content/generate", response_model=Dict[str, Any])
async def generate_content(
    request: ContentGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate repurposed content from source"""
    
    # Verify source exists and belongs to user
    source = db.query(ContentSource).filter(
        ContentSource.id == request.source_id,
        ContentSource.user_id == current_user.get("user_id", "demo_user")
    ).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Content source not found")
    
    if source.status != "processed":
        raise HTTPException(status_code=400, detail="Content source not yet processed")
    
    # Queue generation job
    job_id = str(uuid.uuid4())
    task_queue.enqueue(
        "generate_content",
        job_id,
        request.source_id,
        request.content_types,
        request.custom_prompts
    )
    
    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Content generation started"
    }

@app.get("/content/generated/{job_id}")
async def get_generation_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get status of content generation job"""
    
    # Check if job exists in database
    generated_content = db.query(GeneratedContent).filter(
        GeneratedContent.job_id == job_id
    ).first()
    
    if not generated_content:
        return {"status": "not_found", "message": "Job not found"}
    
    return {
        "job_id": job_id,
        "status": generated_content.status,
        "content": json.loads(generated_content.content) if generated_content.content else None,
        "created_at": generated_content.created_at.isoformat()
    }

# Review and approval endpoints
@app.post("/content/review", response_model=ReviewResponse)
async def submit_review(
    request: ReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit review for generated content"""
    
    review = Review(
        content_id=request.content_id,
        user_id=current_user.get("user_id", "demo_user"),
        status=request.status,
        feedback=request.feedback,
        modifications=request.modifications
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # Update content status
    content = db.query(GeneratedContent).filter(
        GeneratedContent.id == request.content_id
    ).first()
    
    if content:
        content.status = request.status
        db.commit()
    
    return ReviewResponse.from_orm(review)

@app.get("/content/reviews/{content_id}", response_model=List[ReviewResponse])
async def get_content_reviews(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get reviews for specific content"""
    
    reviews = db.query(Review).filter(
        Review.content_id == content_id
    ).all()
    
    return [ReviewResponse.from_orm(review) for review in reviews]

# Scheduling endpoints
@app.post("/content/schedule")
async def schedule_content(
    content_id: str,
    platform: str,
    scheduled_time: datetime,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Schedule content for publishing"""
    
    # Verify content exists and is approved
    content = db.query(GeneratedContent).filter(
        GeneratedContent.id == content_id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if content.status != "approved":
        raise HTTPException(status_code=400, detail="Content must be approved before scheduling")
    
    # Create scheduling record
    from .models import ContentSchedule
    schedule = ContentSchedule(
        content_id=content_id,
        platform=platform,
        scheduled_time=scheduled_time,
        status="scheduled",
        user_id=current_user.get("user_id", "demo_user")
    )
    
    db.add(schedule)
    db.commit()
    
    return {
        "message": "Content scheduled successfully",
        "scheduled_time": scheduled_time.isoformat(),
        "platform": platform
    }

# Analytics endpoints
@app.get("/analytics/overview")
async def get_analytics_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics overview for user"""
    
    # Get content statistics
    total_sources = db.query(ContentSource).filter(
        ContentSource.user_id == current_user.get("user_id", "demo_user")
    ).count()
    
    total_generated = db.query(GeneratedContent).join(ContentSource).filter(
        ContentSource.user_id == current_user.get("user_id", "demo_user")
    ).count()
    
    approved_content = db.query(GeneratedContent).join(ContentSource).filter(
        ContentSource.user_id == current_user.get("user_id", "demo_user"),
        GeneratedContent.status == "approved"
    ).count()
    
    return {
        "total_sources": total_sources,
        "total_generated": total_generated,
        "approved_content": approved_content,
        "approval_rate": approved_content / total_generated if total_generated > 0 else 0
    }

# Vector search endpoints
@app.post("/search/semantic")
async def semantic_search(
    query: str,
    source_id: Optional[str] = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform semantic search across content"""
    
    # Get embedding for query
    embedding_service = EmbeddingService()
    query_embedding = embedding_service.get_embedding(query)
    
    # Search in vector database
    from .services import VectorService
    vector_service = VectorService()
    results = vector_service.search(
        query_embedding,
        source_id=source_id,
        limit=limit
    )
    
    return {
        "query": query,
        "results": results,
        "total": len(results)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
