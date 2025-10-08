# Content Repurposing Agent - Complete Testing Guide

## 🧪 Testing Overview

This guide provides comprehensive testing procedures for the Content Repurposing Agent system, from basic functionality to advanced scenarios.

## 🚀 Quick Start Testing

### 1. Automated Testing
```bash
# Run the complete deploy and test script
chmod +x scripts/deploy-and-test.sh
./scripts/deploy-and-test.sh
```

### 2. Prerequisites Check
```bash
# Check system requirements
chmod +x scripts/test-prerequisites.sh
./scripts/test-prerequisites.sh
```

### 3. Quick System Test
```bash
# Run quick tests after deployment
chmod +x scripts/quick-test.sh
./scripts/quick-test.sh
```

## 🔍 Manual Testing Procedures

### Phase 1: System Health Checks

#### 1.1 Service Status Check
```bash
# Check all services are running
docker-compose ps

# Expected output: All services should show "Up" status
```

#### 1.2 Port Accessibility
```bash
# Check API port
curl -f http://localhost:8000/health

# Check frontend port
curl -f http://localhost:3000

# Check monitoring ports
curl -f http://localhost:9090  # Prometheus
curl -f http://localhost:3001  # Grafana
```

#### 1.3 Database Connectivity
```bash
# Test PostgreSQL connection
docker-compose exec postgres psql -U content_agent -d content_agent -c "SELECT 1;"

# Test Redis connection
docker-compose exec redis redis-cli ping

# Test Qdrant connection
curl -f http://localhost:6333/health
```

### Phase 2: Authentication Testing

#### 2.1 User Login
```bash
# Test login endpoint
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Expected: JSON response with access_token
```

#### 2.2 Token Validation
```bash
# Extract token from login response
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' | \
  grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# Test protected endpoint
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/content/sources
```

### Phase 3: Content Upload Testing

#### 3.1 Text File Upload
```bash
# Create test file
echo "This is a comprehensive test document for the Content Repurposing Agent. It contains detailed information about artificial intelligence, machine learning, and content automation. The system should be able to process this text and generate various social media posts, including LinkedIn articles, Twitter threads, Instagram carousels, and newsletter sections." > test-document.txt

# Upload file
curl -X POST http://localhost:8000/content/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test-document.txt" \
  -F "title=Test Document" \
  -F "content_type=text"

# Expected: JSON response with source_id
```

#### 3.2 Audio File Upload
```bash
# Create a test audio file (if you have one)
# curl -X POST http://localhost:8000/content/upload \
#   -H "Authorization: Bearer $TOKEN" \
#   -F "file=@test-audio.mp3" \
#   -F "title=Test Audio" \
#   -F "content_type=audio"
```

#### 3.3 Video File Upload
```bash
# Create a test video file (if you have one)
# curl -X POST http://localhost:8000/content/upload \
#   -H "Authorization: Bearer $TOKEN" \
#   -F "file=@test-video.mp4" \
#   -F "title=Test Video" \
#   -F "content_type=video"
```

### Phase 4: Content Processing Testing

#### 4.1 Check Processing Status
```bash
# Get list of content sources
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/content/sources

# Check specific source status
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/content/sources/{source_id}
```

#### 4.2 Monitor Processing Logs
```bash
# Check ASR worker logs
docker-compose logs asr-worker

# Check embedding worker logs
docker-compose logs embedding-worker

# Check generation worker logs
docker-compose logs generation-worker
```

### Phase 5: Content Generation Testing

#### 5.1 Generate LinkedIn Post
```bash
# Generate LinkedIn content
curl -X POST http://localhost:8000/content/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": "YOUR_SOURCE_ID",
    "content_types": ["linkedin"],
    "custom_prompts": {}
  }'

# Expected: JSON response with job_id
```

#### 5.2 Generate Twitter Thread
```bash
# Generate Twitter content
curl -X POST http://localhost:8000/content/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": "YOUR_SOURCE_ID",
    "content_types": ["twitter"],
    "custom_prompts": {}
  }'
```

#### 5.3 Generate Multiple Content Types
```bash
# Generate multiple content types at once
curl -X POST http://localhost:8000/content/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": "YOUR_SOURCE_ID",
    "content_types": ["linkedin", "twitter", "instagram", "newsletter"],
    "custom_prompts": {}
  }'
```

### Phase 6: Content Review Testing

#### 6.1 Get Content for Review
```bash
# Get pending content for review
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/review/pending

# Expected: List of generated content awaiting review
```

#### 6.2 Submit Review
```bash
# Approve content
curl -X POST http://localhost:8000/review/submit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "YOUR_CONTENT_ID",
    "status": "approved",
    "rating": 5,
    "feedback": "Great content!",
    "tags": ["marketing", "social-media"]
  }'
```

#### 6.3 Reject Content
```bash
# Reject content with feedback
curl -X POST http://localhost:8000/review/submit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "YOUR_CONTENT_ID",
    "status": "rejected",
    "rating": 2,
    "feedback": "Needs improvement in tone",
    "tags": ["needs-revision"]
  }'
```

### Phase 7: Publishing Testing

#### 7.1 Schedule Content
```bash
# Schedule content for publishing
curl -X POST http://localhost:8000/content/schedule \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "YOUR_CONTENT_ID",
    "platform": "linkedin",
    "scheduled_time": "2024-01-15T10:00:00Z"
  }'
```

#### 7.2 Check Scheduled Content
```bash
# Get scheduled content
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/content/schedule
```

### Phase 8: Analytics Testing

#### 8.1 Get Analytics Overview
```bash
# Get analytics data
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/analytics/overview
```

#### 8.2 Get Review Statistics
```bash
# Get review statistics
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/review/stats
```

### Phase 9: Search Testing

#### 9.1 Semantic Search
```bash
# Test semantic search
curl -X POST http://localhost:8000/search/semantic \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "limit": 10
  }'
```

## 🧪 Automated Test Suite

### Run All Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_transcription.py -v
pytest tests/test_chunking.py -v
pytest tests/test_embedding.py -v
pytest tests/test_generation.py -v
pytest tests/test_end_to_end.py -v
```

### Test Categories

#### 1. Transcription Tests
```bash
# Test ASR functionality
pytest tests/test_transcription.py::test_audio_transcription -v
pytest tests/test_transcription.py::test_video_processing -v
```

#### 2. Chunking Tests
```bash
# Test text chunking strategies
pytest tests/test_chunking.py::test_fixed_size_chunking -v
pytest tests/test_chunking.py::test_sentence_boundary_chunking -v
```

#### 3. Embedding Tests
```bash
# Test embedding generation and search
pytest tests/test_embedding.py::test_embedding_generation -v
pytest tests/test_embedding.py::test_semantic_search -v
```

#### 4. Generation Tests
```bash
# Test content generation
pytest tests/test_generation.py::test_linkedin_content_validation -v
pytest tests/test_generation.py::test_twitter_content_validation -v
```

#### 5. End-to-End Tests
```bash
# Test complete workflows
pytest tests/test_end_to_end.py::test_content_upload_flow -v
pytest tests/test_end_to_end.py::test_content_generation_flow -v
```

## 🔧 Performance Testing

### Load Testing
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test API performance
ab -n 100 -c 10 http://localhost:8000/health

# Test with authentication
ab -n 50 -c 5 -H "Authorization: Bearer $TOKEN" http://localhost:8000/content/sources
```

### Resource Monitoring
```bash
# Monitor Docker resources
docker stats

# Monitor specific services
docker stats content-agent-api content-agent-llm-service

# Check GPU usage
nvidia-smi
```

### Memory Testing
```bash
# Test memory usage under load
for i in {1..10}; do
  curl -X POST http://localhost:8000/content/generate \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"source_id": "YOUR_SOURCE_ID", "content_types": ["linkedin"]}' &
done
wait
```

## 🐛 Troubleshooting Tests

### Common Issues Testing

#### 1. Service Startup Issues
```bash
# Check service logs
docker-compose logs api
docker-compose logs postgres
docker-compose logs redis
docker-compose logs qdrant

# Restart problematic services
docker-compose restart api
docker-compose restart postgres
```

#### 2. GPU Issues
```bash
# Test GPU availability
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Check GPU in LLM service
docker-compose exec llm-service nvidia-smi
```

#### 3. Database Issues
```bash
# Check database connection
docker-compose exec postgres psql -U content_agent -d content_agent -c "SELECT 1;"

# Check database logs
docker-compose logs postgres
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h
docker stats

# Check for memory leaks
docker-compose logs | grep -i "memory\|oom"
```

## 📊 Test Results Validation

### Expected Results

#### 1. Service Health
- All Docker services running
- API responding within 2 seconds
- Frontend accessible
- Database connections working

#### 2. Content Processing
- File uploads successful
- Content processing within 5 minutes
- Transcription accuracy >90%
- Embeddings generated successfully

#### 3. Content Generation
- Content generated within 30 seconds
- JSON schema validation passing
- Quality scores >80%
- Source attribution present

#### 4. Review Workflow
- Review interface functional
- Approval/rejection working
- Feedback collection working
- Status updates working

#### 5. Publishing
- Content scheduling working
- Platform integrations functional
- Analytics data collected
- Performance metrics tracked

## 🎯 Test Scenarios

### Scenario 1: Complete Content Workflow
1. Upload a text document
2. Wait for processing (5 minutes)
3. Generate LinkedIn post
4. Review and approve content
5. Schedule for publishing
6. Check analytics

### Scenario 2: Multi-format Content
1. Upload text, audio, and video files
2. Process all content types
3. Generate multiple content formats
4. Review all generated content
5. Schedule across multiple platforms

### Scenario 3: Error Handling
1. Upload invalid file types
2. Test with corrupted files
3. Test network interruptions
4. Test resource exhaustion
5. Verify error recovery

### Scenario 4: Performance Testing
1. Upload large files
2. Generate multiple content types
3. Test concurrent users
4. Monitor resource usage
5. Test scaling limits

## 📋 Test Checklist

### Pre-Testing Setup
- [ ] System prerequisites met
- [ ] Docker services running
- [ ] Environment variables set
- [ ] Models downloaded
- [ ] Test data prepared

### Basic Functionality
- [ ] Service health checks
- [ ] Authentication working
- [ ] File uploads working
- [ ] Content processing working
- [ ] Content generation working

### Advanced Features
- [ ] Review workflow functional
- [ ] Publishing working
- [ ] Analytics collecting
- [ ] Search working
- [ ] Monitoring active

### Performance
- [ ] Response times acceptable
- [ ] Memory usage stable
- [ ] GPU utilization optimal
- [ ] Database performance good
- [ ] Network performance good

### Security
- [ ] Authentication secure
- [ ] Data encrypted
- [ ] Access controls working
- [ ] Audit logging active
- [ ] Security scanning clean

## 🚀 Production Testing

### Pre-Production Checklist
- [ ] All tests passing
- [ ] Performance benchmarks met
- [ ] Security audit completed
- [ ] Backup systems tested
- [ ] Monitoring configured
- [ ] Documentation updated

### Production Deployment
- [ ] Environment configured
- [ ] Secrets secured
- [ ] SSL certificates installed
- [ ] Domain configured
- [ ] Load balancer configured
- [ ] Monitoring active

### Post-Deployment Testing
- [ ] Smoke tests passing
- [ ] Performance monitoring
- [ ] User acceptance testing
- [ ] Security scanning
- [ ] Backup verification
- [ ] Disaster recovery testing

## 📞 Support and Help

### Getting Help
- Check logs: `docker-compose logs [service-name]`
- Run health checks: `./scripts/health-check.sh`
- Run quick tests: `./scripts/quick-test.sh`
- Review documentation: `docs/` directory

### Common Solutions
- Restart services: `docker-compose restart`
- Check resources: `docker stats`
- Update system: `docker-compose pull && docker-compose up -d`
- Check prerequisites: `./scripts/test-prerequisites.sh`

### Emergency Procedures
- System down: Check logs and restart
- Data loss: Restore from backups
- Performance issues: Monitor resources
- Security issues: Review security checklist

---

*This testing guide ensures comprehensive validation of the Content Repurposing Agent system. Follow these procedures to verify functionality, performance, and reliability.*
