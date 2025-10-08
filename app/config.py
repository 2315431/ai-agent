from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Auto-detect environment
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._auto_configure()
    
    def _auto_configure(self):
        """Auto-configure based on environment detection"""
        # Detect if running on cloud platforms
        if os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU"):
            # Cloud deployment - use SQLite
            self.DATABASE_URL = "sqlite:///./content_agent.db"
            self.REDIS_URL = "redis://localhost:6379"
            self.ENVIRONMENT = "production"
            self.DEBUG = False
        else:
            # Local development
            self.DATABASE_URL = "sqlite:///./content_agent.db"
            self.REDIS_URL = "redis://localhost:6379"
            self.ENVIRONMENT = "development"
            self.DEBUG = True
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./content_agent.db"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    
    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    
    # LLM settings
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000
    
    # Embedding settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File upload settings
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list = [".txt", ".pdf", ".mp4", ".mp3", ".wav", ".docx"]
    
    # Content generation settings
    MAX_CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_RETRIEVAL_RESULTS: int = 10
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
