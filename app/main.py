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

from .database import get_db, engine, Base
from .models import ContentSource, GeneratedContent, ContentChunk, User, Review
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

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Content Repurposing Agent API",
    description="Self-hosted content repurposing system using open-source LLMs",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
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
@app.post("/content/upload", response_model=ContentSourceResponse)
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
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = f"/uploads/{file_id}_{file.filename}"
    
    with open(f"uploads/{file_id}_{file.filename}", "wb") as buffer:
        content = await file.read()
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
        user_id=current_user.id
    )
    
    db.add(content_source)
    db.commit()
    db.refresh(content_source)
    
    # Queue processing job
    if source_type in ["audio", "video"]:
        task_queue.enqueue("process_audio", file_id, file_path)
    else:
        task_queue.enqueue("process_text", file_id, file_path)
    
    return ContentSourceResponse.from_orm(content_source)

@app.get("/content/sources", response_model=List[ContentSourceResponse])
async def list_content_sources(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all content sources for the current user"""
    sources = db.query(ContentSource).filter(
        ContentSource.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return [ContentSourceResponse.from_orm(source) for source in sources]

@app.get("/content/sources/{source_id}", response_model=ContentSourceResponse)
async def get_content_source(
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific content source details"""
    source = db.query(ContentSource).filter(
        ContentSource.id == source_id,
        ContentSource.user_id == current_user.id
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
        ContentSource.user_id == current_user.id
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
        user_id=current_user.id,
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
        user_id=current_user.id
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
        ContentSource.user_id == current_user.id
    ).count()
    
    total_generated = db.query(GeneratedContent).join(ContentSource).filter(
        ContentSource.user_id == current_user.id
    ).count()
    
    approved_content = db.query(GeneratedContent).join(ContentSource).filter(
        ContentSource.user_id == current_user.id,
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
