#!/bin/bash

# Content Repurposing Agent - Ubuntu 22.04 Setup Script
# Run with: sudo bash setup-ubuntu.sh

set -e

echo "🚀 Setting up Content Repurposing Agent on Ubuntu 22.04..."

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install essential packages
echo "🔧 Installing essential packages..."
apt install -y curl wget git build-essential software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Install NVIDIA drivers and CUDA
echo "🎮 Installing NVIDIA drivers and CUDA..."
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
dpkg -i cuda-keyring_1.0-1_all.deb
apt update
apt install -y cuda-drivers-535 cuda-toolkit-12-2

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Install NVIDIA Container Toolkit
echo "🔧 Installing NVIDIA Container Toolkit..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
apt update
apt install -y nvidia-docker2
systemctl restart docker

# Install Python 3.11 and pip
echo "🐍 Installing Python 3.11..."
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Create application user
echo "👤 Creating application user..."
useradd -m -s /bin/bash contentagent || true
usermod -aG docker contentagent

# Create directories
echo "📁 Creating application directories..."
mkdir -p /opt/content-agent/{models,uploads,logs,data}
mkdir -p /opt/content-agent/models/{llm,embedding,whisper}
chown -R contentagent:contentagent /opt/content-agent

# Download model weights (placeholders for actual URLs)
echo "📥 Setting up model download script..."
cat > /opt/content-agent/download-models.sh << 'EOF'
#!/bin/bash

# Model download script - Replace URLs with actual model download links
MODELS_DIR="/opt/content-agent/models"

# LLM Models (choose one based on GPU memory)
# 7B model (requires ~14GB VRAM)
# wget -O $MODELS_DIR/llm/model.tar.gz "REPLACE_WITH_7B_MODEL_URL"
# tar -xzf $MODELS_DIR/llm/model.tar.gz -C $MODELS_DIR/llm/

# 13B model (requires ~26GB VRAM) 
# wget -O $MODELS_DIR/llm/model.tar.gz "REPLACE_WITH_13B_MODEL_URL"
# tar -xzf $MODELS_DIR/llm/model.tar.gz -C $MODELS_DIR/llm/

# Embedding model
wget -O $MODELS_DIR/embedding/sentence-transformers.tar.gz "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/pytorch_model.bin"
wget -O $MODELS_DIR/embedding/config.json "https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json"

# Whisper model
wget -O $MODELS_DIR/whisper/whisper-base.tar.gz "https://openaipublic.azureedge.net/whisper/models/ed3a0b6b1c0cedf700ca950eb064b3262f373565/whisper-base.tar.gz"
tar -xzf $MODELS_DIR/whisper/whisper-base.tar.gz -C $MODELS_DIR/whisper/

echo "✅ Models downloaded successfully"
EOF

chmod +x /opt/content-agent/download-models.sh
chown contentagent:contentagent /opt/content-agent/download-models.sh

# Create systemd service
echo "⚙️ Creating systemd service..."
cat > /etc/systemd/system/content-agent.service << 'EOF'
[Unit]
Description=Content Repurposing Agent
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/content-agent
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=contentagent
Group=contentagent

[Install]
WantedBy=multi-user.target
EOF

# Create environment file template
echo "🔐 Creating environment file template..."
cat > /opt/content-agent/.env.template << 'EOF'
# Database Configuration
POSTGRES_PASSWORD=your_secure_postgres_password_here
DATABASE_URL=postgresql://content_agent:your_secure_postgres_password_here@postgres:5432/content_agent

# Security
SECRET_KEY=your_secret_key_here_minimum_32_characters
NEXTAUTH_SECRET=your_nextauth_secret_here

# Model Configuration
MODEL_NAME=microsoft/DialoGPT-medium
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Monitoring
GRAFANA_PASSWORD=your_grafana_password_here

# Optional: External Services
# BUFFER_API_KEY=your_buffer_api_key
# HOOTSUITE_API_KEY=your_hootsuite_api_key
EOF

# Set up log rotation
echo "📝 Setting up log rotation..."
cat > /etc/logrotate.d/content-agent << 'EOF'
/opt/content-agent/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 contentagent contentagent
}
EOF

# Create health check script
echo "🏥 Creating health check script..."
cat > /opt/content-agent/health-check.sh << 'EOF'
#!/bin/bash

# Health check script for Content Repurposing Agent
echo "🔍 Checking Content Repurposing Agent health..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

# Check if all services are running
services=("content-agent-qdrant" "content-agent-redis" "content-agent-postgres" "content-agent-api" "content-agent-llm")
for service in "${services[@]}"; do
    if ! docker ps --format "table {{.Names}}" | grep -q "$service"; then
        echo "❌ Service $service is not running"
        exit 1
    fi
done

# Check API health
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ API health check failed"
    exit 1
fi

echo "✅ All services are healthy"
EOF

chmod +x /opt/content-agent/health-check.sh
chown contentagent:contentagent /opt/content-agent/health-check.sh

# Create backup script
echo "💾 Creating backup script..."
cat > /opt/content-agent/backup.sh << 'EOF'
#!/bin/bash

# Backup script for Content Repurposing Agent
BACKUP_DIR="/opt/content-agent/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup in $BACKUP_DIR..."

# Backup PostgreSQL
docker exec content-agent-postgres pg_dump -U content_agent content_agent > "$BACKUP_DIR/postgres.sql"

# Backup Qdrant
docker exec content-agent-qdrant tar -czf - /qdrant/storage > "$BACKUP_DIR/qdrant.tar.gz"

# Backup Redis
docker exec content-agent-redis redis-cli --rdb "$BACKUP_DIR/redis.rdb"

# Backup application data
cp -r /opt/content-agent/uploads "$BACKUP_DIR/"
cp -r /opt/content-agent/logs "$BACKUP_DIR/"

echo "✅ Backup completed: $BACKUP_DIR"
EOF

chmod +x /opt/content-agent/backup.sh
chown contentagent:contentagent /opt/content-agent/backup.sh

echo "✅ Ubuntu 22.04 setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your application files to /opt/content-agent/"
echo "2. Copy .env.template to .env and configure your environment variables"
echo "3. Run: sudo -u contentagent /opt/content-agent/download-models.sh"
echo "4. Start the service: sudo systemctl enable content-agent && sudo systemctl start content-agent"
echo "5. Check health: sudo -u contentagent /opt/content-agent/health-check.sh"
echo ""
echo "🔗 Access URLs:"
echo "- API: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo "- Grafana: http://localhost:3001"
echo "- Prometheus: http://localhost:9090"
