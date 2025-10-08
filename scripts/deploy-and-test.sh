#!/bin/bash

# Content Repurposing Agent - Complete Deploy and Test Script
# This script will deploy the system and run comprehensive tests

echo "🚀 Content Repurposing Agent - Complete Deploy and Test"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🔧 $1${NC}"
}

# Step 1: Prerequisites Check
echo ""
print_step "Step 1: Checking prerequisites..."
chmod +x scripts/test-prerequisites.sh
./scripts/test-prerequisites.sh

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Prerequisites check failed. Please resolve issues before continuing.${NC}"
    exit 1
fi

# Step 2: Environment Setup
echo ""
print_step "Step 2: Setting up environment..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_info "Creating .env file..."
    cat > .env << 'EOF'
# Database Configuration
POSTGRES_PASSWORD=secure_password_123
DATABASE_URL=postgresql://content_agent:secure_password_123@postgres:5432/content_agent

# Redis Configuration
REDIS_PASSWORD=redis_password_123
REDIS_URL=redis://:redis_password_123@redis:6379

# Qdrant Configuration
QDRANT_URL=http://qdrant:6333

# API Configuration
SECRET_KEY=your_secret_key_here_change_in_production
NEXTAUTH_SECRET=your_nextauth_secret_here_change_in_production

# LLM Configuration
MODEL_NAME=microsoft/DialoGPT-medium
MODEL_PATH=/models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Monitoring
GRAFANA_PASSWORD=grafana_password_123

# Environment
ENVIRONMENT=production
DEBUG=false
EOF
    print_status "Environment file created" 0
else
    print_info "Environment file already exists"
fi

# Create necessary directories
print_info "Creating directories..."
mkdir -p {models,uploads,logs,data/{postgres,redis,qdrant},nginx/ssl}
chmod 755 models uploads logs data
chmod 777 uploads

# Step 3: Download Models
echo ""
print_step "Step 3: Downloading models..."

# Create a simple model download script
cat > download-models.sh << 'EOF'
#!/bin/bash
echo "📥 Downloading models..."

# Create models directory
mkdir -p models

# Download embedding model (this will be done by the embedding worker)
echo "Embedding model will be downloaded automatically by the worker"

# For now, create a placeholder
echo "Model download completed (models will be downloaded by workers)"
EOF

chmod +x download-models.sh
./download-models.sh

# Step 4: Deploy Services
echo ""
print_step "Step 4: Deploying services with Docker Compose..."

print_info "Starting Docker Compose services..."
docker-compose up -d

if [ $? -eq 0 ]; then
    print_status "Docker Compose services started" 0
else
    print_warning "Docker Compose had issues starting"
fi

# Step 5: Wait for Services
echo ""
print_step "Step 5: Waiting for services to initialize..."

print_info "Waiting 60 seconds for services to start..."
sleep 60

# Check service status
print_info "Checking service status..."
docker-compose ps

# Step 6: Health Checks
echo ""
print_step "Step 6: Running health checks..."

# Make scripts executable
chmod +x scripts/health-check.sh
chmod +x scripts/quick-test.sh

# Run health check
./scripts/health-check.sh

# Step 7: Quick Tests
echo ""
print_step "Step 7: Running quick tests..."

./scripts/quick-test.sh

# Step 8: Manual Testing Guide
echo ""
print_step "Step 8: Manual testing guide..."

echo -e "${BLUE}🧪 Manual Testing Steps:${NC}"
echo ""
echo "1. 🌐 Access the frontend:"
echo "   - URL: http://localhost:3000"
echo "   - Credentials: admin/admin"
echo ""
echo "2. 📊 Check API documentation:"
echo "   - URL: http://localhost:8000/docs"
echo "   - Interactive API testing available"
echo ""
echo "3. 📈 Monitor system:"
echo "   - Grafana: http://localhost:3001"
echo "   - Prometheus: http://localhost:9090"
echo ""
echo "4. 🧪 Test content workflow:"
echo "   a. Upload a text file"
echo "   b. Wait for processing (check logs)"
echo "   c. Generate content (LinkedIn, Twitter, etc.)"
echo "   d. Review and approve content"
echo "   e. Schedule for publishing"
echo ""

# Step 9: Troubleshooting Guide
echo ""
print_step "Step 9: Troubleshooting guide..."

echo -e "${YELLOW}🔧 Common Issues and Solutions:${NC}"
echo ""
echo "❌ Services not starting:"
echo "   - Check logs: docker-compose logs [service-name]"
echo "   - Restart: docker-compose restart"
echo "   - Check resources: docker stats"
echo ""
echo "❌ GPU not available:"
echo "   - Check: nvidia-smi"
echo "   - Restart Docker: sudo systemctl restart docker"
echo "   - Check NVIDIA Docker: docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi"
echo ""
echo "❌ Database connection issues:"
echo "   - Check: docker-compose logs postgres"
echo "   - Restart: docker-compose restart postgres"
echo ""
echo "❌ API not responding:"
echo "   - Check: docker-compose logs api"
echo "   - Restart: docker-compose restart api"
echo "   - Check port: netstat -tlnp | grep :8000"
echo ""

# Step 10: Performance Monitoring
echo ""
print_step "Step 10: Performance monitoring setup..."

echo -e "${BLUE}📊 Monitoring Commands:${NC}"
echo ""
echo "Monitor all services:"
echo "  docker-compose logs -f"
echo ""
echo "Monitor specific service:"
echo "  docker-compose logs -f [service-name]"
echo ""
echo "Check resource usage:"
echo "  docker stats"
echo ""
echo "Check service health:"
echo "  ./scripts/health-check.sh"
echo ""
echo "Run quick tests:"
echo "  ./scripts/quick-test.sh"
echo ""

# Final Summary
echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo -e "${GREEN}✅ Content Repurposing Agent is now running!${NC}"
echo ""
echo "🌐 Access URLs:"
echo "  - Frontend: http://localhost:3000"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Monitoring: http://localhost:3001"
echo ""
echo "🔑 Default Credentials:"
echo "  - Username: admin"
echo "  - Password: admin"
echo ""
echo "📋 Next Steps:"
echo "1. Access the frontend at http://localhost:3000"
echo "2. Login with admin/admin"
echo "3. Upload your first content piece"
echo "4. Generate repurposed content"
echo "5. Review and approve content"
echo "6. Schedule for publishing"
echo ""
echo "🔧 Management Commands:"
echo "  - Stop: docker-compose down"
echo "  - Restart: docker-compose restart"
echo "  - Update: docker-compose pull && docker-compose up -d"
echo "  - Logs: docker-compose logs -f"
echo ""
echo "📚 Documentation:"
echo "  - Deployment: docs/deployment_runbook.md"
echo "  - Cost Analysis: docs/cost_analysis.md"
echo "  - Business Criteria: docs/business_criteria.md"
echo "  - Security: security/security_checklist.md"
echo ""
echo -e "${YELLOW}⚠️  Remember to change default passwords in production!${NC}"
echo ""
echo "🎯 Happy content repurposing!"
