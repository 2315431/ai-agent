from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    LINKEDIN_POST = "linkedin_post"
    TWITTER_THREAD = "twitter_thread"
    INSTAGRAM_CAROUSEL = "instagram_carousel"
    NEWSLETTER_SECTION = "newsletter_section"
    VIDEO_SCRIPT = "video_script"
    HASHTAGS = "hashtags"

class ContentSourceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    source_type: str
    file_path: str

class ContentSourceResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    source_type: str
    file_path: str
    file_size: Optional[int]
    status: str
    transcript: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContentGenerationRequest(BaseModel):
    source_id: str
    content_types: List[ContentType]
    custom_prompts: Optional[Dict[str, str]] = None
    target_audience: Optional[str] = None
    tone: Optional[str] = "professional"
    max_length: Optional[int] = None

class GeneratedContentCreate(BaseModel):
    source_id: str
    content_type: ContentType
    content: Dict[str, Any]
    source_chunks: List[str]
    generation_prompt: str
    model_used: str

class GeneratedContentResponse(BaseModel):
    id: str
    source_id: str
    job_id: Optional[str]
    content_type: str
    content: Dict[str, Any]
    status: str
    source_chunks: Optional[List[str]]
    generation_prompt: Optional[str]
    model_used: Optional[str]
    generation_time: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReviewRequest(BaseModel):
    content_id: str
    status: str  # approved, rejected, needs_revision
    feedback: Optional[str] = None
    modifications: Optional[Dict[str, Any]] = None

class ReviewResponse(BaseModel):
    id: str
    content_id: str
    status: str
    feedback: Optional[str]
    modifications: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ContentScheduleRequest(BaseModel):
    content_id: str
    platform: str
    scheduled_time: datetime
    external_credentials: Optional[Dict[str, str]] = None

class AnalyticsResponse(BaseModel):
    total_sources: int
    total_generated: int
    approved_content: int
    approval_rate: float
    content_by_type: Dict[str, int]
    content_by_status: Dict[str, int]
    average_generation_time: float
    most_used_chunks: List[Dict[str, Any]]

class SemanticSearchRequest(BaseModel):
    query: str
    source_id: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)

class SemanticSearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    total: int
    search_time: float
    similarity_threshold: float
