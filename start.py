#!/usr/bin/env python3
"""
Smart startup script for Content Repurposing Agent
Automatically detects environment and configures the app
"""
import os
import sys
import logging
from pathlib import Path

def setup_environment():
    """Setup environment variables based on deployment context"""
    
    # Detect deployment platform
    if os.getenv("RENDER"):
        platform = "Render"
        setup_render_environment()
    elif os.getenv("RAILWAY"):
        platform = "Railway"
        setup_railway_environment()
    elif os.getenv("HEROKU"):
        platform = "Heroku"
        setup_heroku_environment()
    else:
        platform = "Local"
        setup_local_environment()
    
    print(f"🚀 Detected platform: {platform}")
    return platform

def setup_render_environment():
    """Configure for Render deployment"""
    os.environ.setdefault("DATABASE_URL", "sqlite:///./content_agent.db")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
    os.environ.setdefault("SECRET_KEY", "render-secret-key-change-in-production")
    os.environ.setdefault("ENVIRONMENT", "production")
    os.environ.setdefault("DEBUG", "false")
    print("✅ Configured for Render")

def setup_railway_environment():
    """Configure for Railway deployment"""
    os.environ.setdefault("DATABASE_URL", "sqlite:///./content_agent.db")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
    os.environ.setdefault("SECRET_KEY", "railway-secret-key-change-in-production")
    os.environ.setdefault("ENVIRONMENT", "production")
    os.environ.setdefault("DEBUG", "false")
    print("✅ Configured for Railway")

def setup_heroku_environment():
    """Configure for Heroku deployment"""
    os.environ.setdefault("DATABASE_URL", "sqlite:///./content_agent.db")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
    os.environ.setdefault("SECRET_KEY", "heroku-secret-key-change-in-production")
    os.environ.setdefault("ENVIRONMENT", "production")
    os.environ.setdefault("DEBUG", "false")
    print("✅ Configured for Heroku")

def setup_local_environment():
    """Configure for local development"""
    os.environ.setdefault("DATABASE_URL", "sqlite:///./content_agent.db")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
    os.environ.setdefault("SECRET_KEY", "local-development-secret-key")
    os.environ.setdefault("ENVIRONMENT", "development")
    os.environ.setdefault("DEBUG", "true")
    print("✅ Configured for Local Development")

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Core dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    """Main startup function"""
    print("🔧 Content Repurposing Agent - Smart Startup")
    print("=" * 50)
    
    # Setup environment
    platform = setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start the application
    print("🚀 Starting FastAPI application...")
    
    # Import and run the app
    try:
        import uvicorn
        from app.main import app
        
        # Get port from environment (Render sets this)
        port = int(os.getenv("PORT", 8000))
        
        print(f"🌐 Server starting on port {port}")
        print(f"📱 Platform: {platform}")
        print("=" * 50)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
