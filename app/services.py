from typing import List, Dict, Any, Optional
import asyncio
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import openai
from sqlalchemy.orm import Session
from .models import ContentSource, ContentChunk, GeneratedContent
from .config import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        return self.model.encode(text).tolist()
    
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        return self.model.encode(texts).tolist()

class VectorService:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = "content_chunks"
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Ensure collection exists"""
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,  # all-MiniLM-L6-v2 dimension
                    distance=Distance.COSINE
                )
            )
    
    def add_chunks(self, chunks: List[ContentChunk], embeddings: List[List[float]]):
        """Add content chunks to vector database"""
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            points.append(PointStruct(
                id=str(chunk.id),
                vector=embedding,
                payload={
                    "source_id": str(chunk.source_id),
                    "chunk_text": chunk.chunk_text,
                    "chunk_index": chunk.chunk_index,
                    "start_position": chunk.start_position,
                    "end_position": chunk.end_position,
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "token_count": chunk.token_count,
                    "metadata": chunk.metadata or {}
                }
            ))
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(self, query_embedding: List[float], source_id: Optional[str] = None, 
               limit: int = 10, score_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar chunks"""
        filter_conditions = None
        if source_id:
            filter_conditions = {
                "must": [{"key": "source_id", "match": {"value": source_id}}]
            }
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=filter_conditions
        )
        
        return [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]

class ContentService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()
    
    def process_text_content(self, source_id: str, file_path: str) -> bool:
        """Process text content and create chunks"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update source status
            source = self.db.query(ContentSource).filter(ContentSource.id == source_id).first()
            source.status = "processing"
            source.transcript = content
            self.db.commit()
            
            # Chunk the content
            chunks = self._chunk_text(content, source_id)
            
            # Generate embeddings
            chunk_texts = [chunk.chunk_text for chunk in chunks]
            embeddings = self.embedding_service.get_embeddings_batch(chunk_texts)
            
            # Save chunks to database
            for chunk in chunks:
                self.db.add(chunk)
            self.db.commit()
            
            # Add to vector database
            self.vector_service.add_chunks(chunks, embeddings)
            
            # Update source status
            source.status = "processed"
            self.db.commit()
            
            return True
            
        except Exception as e:
            # Update source status to failed
            source = self.db.query(ContentSource).filter(ContentSource.id == source_id).first()
            source.status = "failed"
            self.db.commit()
            raise e
    
    def _chunk_text(self, text: str, source_id: str, chunk_size: int = 500, 
                   overlap: int = 50) -> List[ContentChunk]:
        """Chunk text into overlapping segments"""
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end]
            
            # Create chunk object
            chunk = ContentChunk(
                source_id=source_id,
                chunk_text=chunk_text,
                chunk_index=chunk_index,
                start_position=start,
                end_position=end,
                token_count=len(chunk_text.split()),
                metadata={"chunk_size": chunk_size, "overlap": overlap}
            )
            
            chunks.append(chunk)
            start = end - overlap
            chunk_index += 1
        
        return chunks

class GenerationService:
    def __init__(self):
        self.llm_service_url = settings.LLM_SERVICE_URL
        self.vector_service = VectorService()
    
    async def generate_content(self, source_id: str, content_types: List[str], 
                             custom_prompts: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate content for specified types"""
        
        # Get source chunks
        chunks = self._get_relevant_chunks(source_id)
        
        results = {}
        for content_type in content_types:
            # Get prompt template
            prompt = self._get_prompt_template(content_type, custom_prompts)
            
            # Generate content
            content = await self._call_llm(prompt, chunks)
            
            # Parse and structure content
            structured_content = self._parse_content(content, content_type)
            results[content_type] = structured_content
        
        return results
    
    def _get_relevant_chunks(self, source_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most relevant chunks for content generation"""
        # This would typically use semantic search
        # For now, we'll get chunks by source_id
        return []  # Placeholder
    
    def _get_prompt_template(self, content_type: str, custom_prompts: Optional[Dict[str, str]] = None) -> str:
        """Get prompt template for content type"""
        if custom_prompts and content_type in custom_prompts:
            return custom_prompts[content_type]
        
        templates = {
            "linkedin_post": self._get_linkedin_prompt(),
            "twitter_thread": self._get_twitter_prompt(),
            "instagram_carousel": self._get_instagram_prompt(),
            "newsletter_section": self._get_newsletter_prompt(),
            "video_script": self._get_video_script_prompt(),
            "hashtags": self._get_hashtags_prompt()
        }
        
        return templates.get(content_type, "Generate content based on the provided source material.")
    
    async def _call_llm(self, prompt: str, chunks: List[Dict[str, Any]]) -> str:
        """Call LLM service to generate content"""
        import aiohttp
        
        payload = {
            "prompt": prompt,
            "context": chunks,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.llm_service_url}/generate", json=payload) as response:
                result = await response.json()
                return result.get("generated_text", "")
    
    def _parse_content(self, content: str, content_type: str) -> Dict[str, Any]:
        """Parse generated content into structured format"""
        # This would parse the LLM output based on content type
        return {"raw_content": content, "type": content_type}
    
    # Prompt templates
    def _get_linkedin_prompt(self) -> str:
        return """Generate a professional LinkedIn post based on the provided source material. 
        The post should be engaging, professional, and suitable for a business audience.
        Include relevant hashtags and a call-to-action.
        
        Source material: {context}
        
        Return the response in JSON format with the following structure:
        {
            "title": "Post title",
            "content": "Main post content",
            "hashtags": ["#tag1", "#tag2"],
            "call_to_action": "Call to action text"
        }"""
    
    def _get_twitter_prompt(self) -> str:
        return """Generate a Twitter thread (3-5 tweets) based on the provided source material.
        Each tweet should be under 280 characters and build upon the previous one.
        
        Source material: {context}
        
        Return the response in JSON format with the following structure:
        {
            "thread": [
                {"tweet": "First tweet content", "order": 1},
                {"tweet": "Second tweet content", "order": 2}
            ],
            "hashtags": ["#tag1", "#tag2"]
        }"""
    
    def _get_instagram_prompt(self) -> str:
        return """Generate an Instagram carousel post (5-7 slides) based on the provided source material.
        Each slide should have a title, content, and visual description.
        
        Source material: {context}
        
        Return the response in JSON format with the following structure:
        {
            "slides": [
                {
                    "title": "Slide title",
                    "content": "Slide content",
                    "visual_description": "Description of visual elements"
                }
            ],
            "caption": "Main caption for the post",
            "hashtags": ["#tag1", "#tag2"]
        }"""
    
    def _get_newsletter_prompt(self) -> str:
        return """Generate a newsletter section based on the provided source material.
        The content should be informative, engaging, and suitable for email format.
        
        Source material: {context}
        
        Return the response in JSON format with the following structure:
        {
            "subject": "Newsletter subject line",
            "content": "Main newsletter content",
            "call_to_action": "Call to action text"
        }"""
    
    def _get_video_script_prompt(self) -> str:
        return """Generate a short video script (30-60 seconds) based on the provided source material.
        Include timing cues and visual descriptions.
        
        Source material: {context}
        
        Return the response in JSON format with the following structure:
        {
            "script": [
                {
                    "time": "0:00-0:10",
                    "text": "Narrator text",
                    "visual": "Visual description"
                }
            ],
            "total_duration": "60 seconds"
        }"""
    
    def _get_hashtags_prompt(self) -> str:
        return """Generate relevant hashtags for the provided source material.
        Include a mix of popular and niche hashtags.
        
        Source material: {context}
        
        Return the response in JSON format with the following structure:
        {
            "hashtags": ["#tag1", "#tag2", "#tag3"],
            "categories": ["category1", "category2"]
        }"""

class ReviewService:
    def __init__(self, db: Session):
        self.db = db
    
    def submit_review(self, content_id: str, user_id: str, status: str, 
                     feedback: Optional[str] = None, modifications: Optional[Dict[str, Any]] = None):
        """Submit review for generated content"""
        # Implementation for review submission
        pass

class SchedulingService:
    def __init__(self, db: Session):
        self.db = db
    
    def schedule_content(self, content_id: str, platform: str, scheduled_time: datetime):
        """Schedule content for publishing"""
        # Implementation for content scheduling
        pass
