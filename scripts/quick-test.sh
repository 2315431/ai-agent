#!/bin/bash

# Content Repurposing Agent - Quick Test Script
# Run this script to test the system after deployment

echo "🧪 Testing Content Repurposing Agent..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Test 1: Check if services are running
echo "🔍 Test 1: Checking service status..."
print_info "Checking Docker services..."

if docker-compose ps | grep -q "Up"; then
    print_status "Docker services are running" 0
else
    print_warning "Some Docker services may not be running"
    docker-compose ps
fi

# Test 2: Check API health
echo ""
echo "🔍 Test 2: Checking API health..."
print_info "Testing API endpoints..."

# Wait for API to be ready
sleep 5

if curl -f -s http://localhost:8000/health > /dev/null; then
    print_status "API health check passed" 0
else
    print_warning "API health check failed"
    echo "Trying to get API logs..."
    docker-compose logs api | tail -10
fi

# Test 3: Check frontend
echo ""
echo "🔍 Test 3: Checking frontend..."
print_info "Testing frontend accessibility..."

if curl -f -s http://localhost:3000 > /dev/null; then
    print_status "Frontend is accessible" 0
else
    print_warning "Frontend is not accessible"
    echo "Trying to get frontend logs..."
    docker-compose logs frontend | tail -10
fi

# Test 4: Check database
echo ""
echo "🔍 Test 4: Checking database..."
print_info "Testing database connection..."

if docker-compose exec -T postgres psql -U content_agent -d content_agent -c "SELECT 1;" > /dev/null 2>&1; then
    print_status "Database connection successful" 0
else
    print_warning "Database connection failed"
    echo "Trying to get database logs..."
    docker-compose logs postgres | tail -10
fi

# Test 5: Check Redis
echo ""
echo "🔍 Test 5: Checking Redis..."
print_info "Testing Redis connection..."

if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_status "Redis connection successful" 0
else
    print_warning "Redis connection failed"
    echo "Trying to get Redis logs..."
    docker-compose logs redis | tail -10
fi

# Test 6: Check Qdrant
echo ""
echo "🔍 Test 6: Checking Qdrant..."
print_info "Testing Qdrant connection..."

if curl -f -s http://localhost:6333/health > /dev/null; then
    print_status "Qdrant connection successful" 0
else
    print_warning "Qdrant connection failed"
    echo "Trying to get Qdrant logs..."
    docker-compose logs qdrant | tail -10
fi

# Test 7: Check LLM service
echo ""
echo "🔍 Test 7: Checking LLM service..."
print_info "Testing LLM service..."

if curl -f -s http://localhost:8001/health > /dev/null; then
    print_status "LLM service is running" 0
else
    print_warning "LLM service is not responding"
    echo "Trying to get LLM service logs..."
    docker-compose logs llm-service | tail -10
fi

# Test 8: Authentication test
echo ""
echo "🔍 Test 8: Testing authentication..."
print_info "Testing user authentication..."

# Test login endpoint
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' 2>/dev/null)

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    print_status "Authentication working" 0
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    echo "Token received: ${TOKEN:0:20}..."
else
    print_warning "Authentication failed"
    echo "Response: $LOGIN_RESPONSE"
fi

# Test 9: Content upload test
echo ""
echo "🔍 Test 9: Testing content upload..."
print_info "Testing file upload functionality..."

# Create a test file
echo "This is a test document for content repurposing. It contains sample text that will be processed by the Content Repurposing Agent to generate various social media posts and content formats." > test-document.txt

if [ -n "$TOKEN" ]; then
    UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8000/content/upload \
      -H "Authorization: Bearer $TOKEN" \
      -F "file=@test-document.txt" \
      -F "title=Test Document" \
      -F "content_type=text" 2>/dev/null)
    
    if echo "$UPLOAD_RESPONSE" | grep -q "source_id"; then
        print_status "Content upload successful" 0
        SOURCE_ID=$(echo "$UPLOAD_RESPONSE" | grep -o '"source_id":"[^"]*"' | cut -d'"' -f4)
        echo "Source ID: $SOURCE_ID"
    else
        print_warning "Content upload failed"
        echo "Response: $UPLOAD_RESPONSE"
    fi
else
    print_warning "Skipping upload test (no authentication token)"
fi

# Test 10: Content generation test
echo ""
echo "🔍 Test 10: Testing content generation..."
print_info "Testing content generation functionality..."

if [ -n "$TOKEN" ] && [ -n "$SOURCE_ID" ]; then
    # Wait a bit for content processing
    sleep 10
    
    GENERATION_RESPONSE=$(curl -s -X POST http://localhost:8000/content/generate \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"source_id\": \"$SOURCE_ID\",
        \"content_types\": [\"linkedin\"],
        \"custom_prompts\": {}
      }" 2>/dev/null)
    
    if echo "$GENERATION_RESPONSE" | grep -q "job_id"; then
        print_status "Content generation initiated" 0
        JOB_ID=$(echo "$GENERATION_RESPONSE" | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
        echo "Job ID: $JOB_ID"
    else
        print_warning "Content generation failed"
        echo "Response: $GENERATION_RESPONSE"
    fi
else
    print_warning "Skipping generation test (no token or source ID)"
fi

# Test 11: Check workers
echo ""
echo "🔍 Test 11: Checking workers..."
print_info "Testing worker processes..."

# Check if workers are running
WORKER_COUNT=$(docker-compose ps | grep -c "worker")
if [ "$WORKER_COUNT" -gt 0 ]; then
    print_status "$WORKER_COUNT worker(s) running" 0
else
    print_warning "No workers detected"
fi

# Test 12: Check monitoring
echo ""
echo "🔍 Test 12: Checking monitoring..."
print_info "Testing monitoring services..."

if curl -f -s http://localhost:9090 > /dev/null; then
    print_status "Prometheus is accessible" 0
else
    print_warning "Prometheus is not accessible"
fi

if curl -f -s http://localhost:3001 > /dev/null; then
    print_status "Grafana is accessible" 0
else
    print_warning "Grafana is not accessible"
fi

# Cleanup
echo ""
echo "🧹 Cleaning up test files..."
rm -f test-document.txt

# Final summary
echo ""
echo "📊 Test Summary:"
echo "================"

# Count successful tests
SUCCESS_COUNT=0
TOTAL_TESTS=12

# Check each test result (simplified)
if docker-compose ps | grep -q "Up"; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if curl -f -s http://localhost:8000/health > /dev/null; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if curl -f -s http://localhost:3000 > /dev/null; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if docker-compose exec -T postgres psql -U content_agent -d content_agent -c "SELECT 1;" > /dev/null 2>&1; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if curl -f -s http://localhost:6333/health > /dev/null; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if curl -f -s http://localhost:8001/health > /dev/null; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if [ -n "$TOKEN" ]; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if [ -n "$SOURCE_ID" ]; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if [ -n "$JOB_ID" ]; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if [ "$WORKER_COUNT" -gt 0 ]; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi
if curl -f -s http://localhost:9090 > /dev/null; then SUCCESS_COUNT=$((SUCCESS_COUNT + 1)); fi

echo "Tests passed: $SUCCESS_COUNT/$TOTAL_TESTS"

if [ $SUCCESS_COUNT -eq $TOTAL_TESTS ]; then
    echo -e "${GREEN}🎉 All tests passed! The system is working correctly.${NC}"
    echo ""
    echo "🌐 Access your Content Repurposing Agent:"
    echo "- Frontend: http://localhost:3000"
    echo "- API: http://localhost:8000"
    echo "- API Docs: http://localhost:8000/docs"
    echo "- Monitoring: http://localhost:3001 (Grafana)"
    echo ""
    echo "🔑 Default credentials: admin/admin"
elif [ $SUCCESS_COUNT -ge 8 ]; then
    echo -e "${YELLOW}⚠️  Most tests passed ($SUCCESS_COUNT/$TOTAL_TESTS). System is mostly functional.${NC}"
    echo ""
    echo "Check the failed tests above and review logs:"
    echo "docker-compose logs [service-name]"
else
    echo -e "${RED}❌ Many tests failed ($SUCCESS_COUNT/$TOTAL_TESTS). System needs attention.${NC}"
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check all services: docker-compose ps"
    echo "2. Check logs: docker-compose logs"
    echo "3. Restart services: docker-compose restart"
    echo "4. Check prerequisites: ./scripts/test-prerequisites.sh"
fi

echo ""
echo "📋 Next steps:"
echo "1. Access the frontend at http://localhost:3000"
echo "2. Upload your first content piece"
echo "3. Generate repurposed content"
echo "4. Review and approve content"
echo "5. Schedule for publishing"
