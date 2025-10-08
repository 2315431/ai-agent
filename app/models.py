from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content_sources = relationship("ContentSource", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class ContentSource(Base):
    __tablename__ = "content_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    source_type = Column(String(50), nullable=False)  # text, audio, video, pdf
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    status = Column(String(50), default="uploaded")  # uploaded, processing, processed, failed
    transcript = Column(Text)  # For audio/video content
    metadata = Column(JSON)  # Additional metadata
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="content_sources")
    chunks = relationship("ContentChunk", back_populates="source")
    generated_content = relationship("GeneratedContent", back_populates="source")

class ContentChunk(Base):
    __tablename__ = "content_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("content_sources.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    start_position = Column(Integer)  # Character position in original text
    end_position = Column(Integer)
    start_time = Column(Float)  # For audio/video, start time in seconds
    end_time = Column(Float)
    token_count = Column(Integer)
    embedding = Column(JSON)  # Vector embedding
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    source = relationship("ContentSource", back_populates="chunks")

class GeneratedContent(Base):
    __tablename__ = "generated_content"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("content_sources.id"), nullable=False)
    job_id = Column(String(100), unique=True)
    content_type = Column(String(50), nullable=False)  # linkedin, twitter, instagram, etc.
    content = Column(JSON, nullable=False)  # Generated content in structured format
    status = Column(String(50), default="generated")  # generated, approved, rejected, published
    source_chunks = Column(JSON)  # References to source chunks used
    generation_prompt = Column(Text)
    model_used = Column(String(100))
    generation_time = Column(Float)  # Time taken to generate in seconds
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    source = relationship("ContentSource", back_populates="generated_content")
    reviews = relationship("Review", back_populates="content")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("generated_content.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # approved, rejected, needs_revision
    feedback = Column(Text)
    modifications = Column(JSON)  # Specific modifications requested
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("GeneratedContent", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

class ContentSchedule(Base):
    __tablename__ = "content_schedules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("generated_content.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # linkedin, twitter, instagram, etc.
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="scheduled")  # scheduled, published, failed
    external_id = Column(String(100))  # ID from external platform
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("GeneratedContent")
    user = relationship("User")

class ContentMetrics(Base):
    __tablename__ = "content_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("generated_content.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    metric_type = Column(String(50), nullable=False)  # views, likes, shares, clicks
    value = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("GeneratedContent")
