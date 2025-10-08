# Content Repurposing Agent

A comprehensive, self-hosted, open-source system for automated content repurposing across multiple channels. Transform single pieces of content into LinkedIn posts, Twitter threads, Instagram carousels, newsletter sections, video scripts, and more.

## 🚀 Quick Start

Deploy the entire system in 30 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/content-repurposing-agent.git
cd content-repurposing-agent

# 2. Run the setup script
chmod +x scripts/setup-ubuntu.sh
sudo ./scripts/setup-ubuntu.sh

# 3. Deploy with Docker Compose
docker-compose up -d

# 4. Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Default credentials: admin/admin
```

## 📋 System Overview

### Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Workers       │
│   (Next.js)     │◄──►│   (Python)      │◄──►│   (RQ/Redis)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   PostgreSQL     │    │   Qdrant         │
│   (Reverse      │    │   (Metadata)     │    │   (Vector DB)    │
│    Proxy)       │    └─────────────────┘    └─────────────────┘
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   LLM Service   │
│   (vLLM/HF)     │
└─────────────────┘
```

### Key Features
- **Multi-format Input**: Text, audio, video, PDF files
- **AI-powered Transcription**: WhisperX for audio/video
- **Semantic Search**: Qdrant vector database
- **Content Generation**: Open-source LLMs (Llama, Mistral, etc.)
- **Human Review**: Web interface for approval/rejection
- **Multi-platform Publishing**: LinkedIn, Twitter, Instagram, Newsletter
- **Scheduling**: Content calendar and automated publishing
- **Analytics**: Performance tracking and insights

## 🏗️ System Components

### Core Services
- **FastAPI Backend**: REST API for all operations
- **Next.js Frontend**: React-based user interface
- **PostgreSQL**: Metadata and user data storage
- **Redis**: Job queue and caching
- **Qdrant**: Vector database for semantic search
- **Nginx**: Reverse proxy and load balancer

### AI/ML Services
- **LLM Inference**: Open-source language models
- **ASR Worker**: Audio/video transcription
- **Embedding Worker**: Text embedding generation
- **Generation Worker**: Content repurposing
- **LoRA Fine-tuning**: Model customization

### Monitoring & Security
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and visualization
- **Security Scanning**: Automated security checks
- **Backup System**: Automated data backups

## 📁 Project Structure

```
content-repurposing-agent/
├── app/                          # FastAPI application
│   ├── main.py                  # Main API endpoints
│   ├── models.py                # Database models
│   ├── schemas.py                # Pydantic schemas
│   ├── services.py              # Business logic
│   ├── workers/                  # Background workers
│   ├── prompts/                 # LLM prompt templates
│   ├── chunking/                 # Text chunking strategies
│   ├── embeddings/               # Embedding configuration
│   ├── llm/                      # LLM inference service
│   ├── finetuning/               # LoRA fine-tuning
│   ├── review/                   # Human review system
│   └── publishing/                # Publishing & scheduling
├── frontend/                     # Next.js frontend
├── scripts/                      # Setup and utility scripts
├── tests/                        # Comprehensive test suite
├── security/                     # Security configurations
├── docs/                         # Documentation
├── nginx/                        # Nginx configuration
├── docker-compose.yml            # Docker services
└── README.md                     # This file
```

## 🔧 Installation & Setup

### Prerequisites
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 4+ cores (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 16+ GB
- **GPU**: NVIDIA RTX 3080/4080 or better (12+ GB VRAM)
- **Storage**: 100+ GB free space

### Quick Installation
```bash
# 1. Run the setup script
sudo ./scripts/setup-ubuntu.sh

# 2. Configure environment
cp .env.template .env
# Edit .env with your settings

# 3. Download models
./scripts/download-models.sh

# 4. Start services
docker-compose up -d

# 5. Verify installation
./scripts/health-check.sh
```

### Manual Installation
See [deployment_runbook.md](./docs/deployment_runbook.md) for detailed step-by-step instructions.

## 🎯 Usage

### 1. Content Upload
```bash
# Upload a text file
curl -X POST http://localhost:8000/content/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.txt" \
  -F "title=My Document" \
  -F "content_type=text"
```

### 2. Content Generation
```bash
# Generate LinkedIn post
curl -X POST http://localhost:8000/content/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": "YOUR_SOURCE_ID",
    "content_types": ["linkedin"],
    "custom_prompts": {}
  }'
```

### 3. Review and Approval
```bash
# Get content for review
curl http://localhost:8000/review/pending \
  -H "Authorization: Bearer YOUR_TOKEN"

# Submit review
curl -X POST http://localhost:8000/review/submit \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "YOUR_CONTENT_ID",
    "status": "approved",
    "rating": 5,
    "feedback": "Great content!"
  }'
```

### 4. Publishing
```bash
# Schedule content for publishing
curl -X POST http://localhost:8000/content/schedule \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "YOUR_CONTENT_ID",
    "platform": "linkedin",
    "scheduled_time": "2024-01-15T10:00:00Z"
  }'
```

## 🧪 Testing

### Run Test Suite
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_transcription.py
pytest tests/test_chunking.py
pytest tests/test_embedding.py
pytest tests/test_generation.py
pytest tests/test_end_to_end.py
```

### Test Coverage
- **Transcription**: ASR worker functionality
- **Chunking**: Text segmentation strategies
- **Embeddings**: Vector generation and search
- **Generation**: LLM content creation
- **End-to-End**: Complete workflow testing

## 📊 Monitoring

### Health Checks
```bash
# Check system health
./scripts/health-check.sh

# Monitor services
docker-compose ps
docker-compose logs -f

# Check resource usage
docker stats
```

### Metrics & Dashboards
- **Grafana**: http://localhost:3001
- **Prometheus**: http://localhost:9090
- **API Documentation**: http://localhost:8000/docs

## 🔒 Security

### Security Features
- **Authentication**: JWT-based user authentication
- **Authorization**: Role-based access control
- **Encryption**: Data encryption at rest and in transit
- **Audit Logging**: Comprehensive activity logging
- **Security Scanning**: Automated vulnerability detection

### Security Checklist
See [security_checklist.md](./security/security_checklist.md) for comprehensive security guidelines.

## 💰 Cost Analysis

### Infrastructure Costs
- **Small Demo**: $100-300/month
- **Medium Production**: $300-1,200/month
- **Large Enterprise**: $1,150-4,600/month
- **Enterprise Scale**: $2,800-9,700/month

### ROI Analysis
- **Time Savings**: 80% reduction in content creation time
- **Cost per Content**: $5-10 per piece
- **ROI**: 300-500% return on investment
- **Engagement**: 20-30% higher engagement rates

See [cost_analysis.md](./docs/cost_analysis.md) for detailed cost breakdowns.

## 🚀 Deployment Options

### 1. On-Premises
- **Hardware**: $2,000-50,000 initial investment
- **Ongoing**: $100-5,000/month
- **Benefits**: Full control, data privacy, lower ongoing costs
- **Drawbacks**: Requires technical expertise

### 2. Cloud Deployment
- **AWS**: $200-9,000/month
- **Google Cloud**: $180-7,000/month
- **Azure**: $220-8,000/month
- **Benefits**: Managed infrastructure, scalability
- **Drawbacks**: Higher ongoing costs

### 3. Hybrid Approach
- **Best of Both**: Mix of on-premises and cloud
- **Cost Optimization**: Balance between control and cost
- **Flexibility**: Adapt to changing needs

## 📈 Scaling

### Horizontal Scaling
- **Load Balancer**: Distribute requests across instances
- **Database Sharding**: Split data across multiple databases
- **Vector DB Clustering**: Distribute embeddings across nodes
- **Worker Scaling**: Scale workers based on queue length

### Vertical Scaling
- **GPU Upgrades**: Move to more powerful GPUs
- **Memory Upgrades**: Increase RAM for larger models
- **Storage Upgrades**: Add more storage for larger datasets
- **Network Upgrades**: Increase bandwidth for faster transfers

## 🔄 Maintenance

### Daily Tasks
- [ ] Check system health
- [ ] Monitor resource usage
- [ ] Review error logs
- [ ] Check backup status

### Weekly Tasks
- [ ] Update system packages
- [ ] Review security logs
- [ ] Optimize performance
- [ ] Clean up old data

### Monthly Tasks
- [ ] Security audit
- [ ] Performance review
- [ ] Capacity planning
- [ ] Documentation update

## 📚 Documentation

### Comprehensive Guides
- [**Deployment Runbook**](./docs/deployment_runbook.md): 30-minute deployment guide
- [**Cost Analysis**](./docs/cost_analysis.md): Infrastructure and cost recommendations
- [**Business Criteria**](./docs/business_criteria.md): Acceptance criteria and pilot plan
- [**Security Checklist**](./security/security_checklist.md): Security best practices

### API Documentation
- **OpenAPI Spec**: http://localhost:8000/docs
- **Interactive Testing**: http://localhost:8000/redoc
- **Postman Collection**: Available in `docs/` directory

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/your-org/content-repurposing-agent.git
cd content-repurposing-agent

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Start development environment
docker-compose -f docker-compose.dev.yml up -d
```

### Code Standards
- **Python**: PEP 8 style guide
- **Type Hints**: Use type annotations
- **Documentation**: Docstrings for all functions
- **Testing**: Comprehensive test coverage
- **Security**: Follow security best practices

## 📞 Support

### Getting Help
- **Documentation**: Check the `docs/` directory
- **Issues**: GitHub Issues for bug reports
- **Community**: Join our community forum
- **Professional**: Enterprise support available

### Emergency Procedures
- **System Down**: Check logs and restart services
- **Data Loss**: Restore from backups
- **Security Incident**: Follow security incident response plan
- **Performance Issues**: Monitor resources and optimize

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Open Source Community**: For the amazing tools and libraries
- **Hugging Face**: For model hosting and transformers library
- **FastAPI**: For the excellent web framework
- **Docker**: For containerization technology
- **NVIDIA**: For GPU acceleration support

---

## 🎯 Quick Reference

### Key URLs
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Monitoring**: http://localhost:3001 (Grafana)

### Default Credentials
- **Username**: admin
- **Password**: admin
- **Remember**: Change these in production!

### Common Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Update services
docker-compose pull && docker-compose up -d
```

### File Locations
- **Configuration**: `.env` file
- **Logs**: `logs/` directory
- **Models**: `models/` directory
- **Uploads**: `uploads/` directory
- **Data**: `data/` directory

---

*Built with ❤️ for the open-source community. Transform your content creation workflow with AI-powered automation.*
