#!/bin/bash

# Content Repurposing Agent - Security Scan Script
# Run this script regularly to check for security issues

set -e

echo "🔍 Starting security scan for Content Repurposing Agent..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root - consider using a non-root user for security"
fi

echo "📋 Checking system security..."

# Check for security updates
echo "🔍 Checking for security updates..."
if command -v apt &> /dev/null; then
    SECURITY_UPDATES=$(apt list --upgradable 2>/dev/null | grep -c "security" || true)
    if [ "$SECURITY_UPDATES" -gt 0 ]; then
        print_warning "Found $SECURITY_UPDATES security updates available"
    else
        print_status "No security updates available" 0
    fi
fi

# Check Docker security
echo "🔍 Checking Docker security..."
if command -v docker &> /dev/null; then
    # Check if Docker daemon is running
    if docker info &> /dev/null; then
        print_status "Docker daemon is running" 0
        
        # Check for running containers
        RUNNING_CONTAINERS=$(docker ps --format "{{.Names}}" | wc -l)
        echo "📊 Found $RUNNING_CONTAINERS running containers"
        
        # Check for containers running as root
        ROOT_CONTAINERS=$(docker ps --format "table {{.Names}}\t{{.User}}" | grep -c "root" || true)
        if [ "$ROOT_CONTAINERS" -gt 0 ]; then
            print_warning "Found containers running as root"
        else
            print_status "No containers running as root" 0
        fi
        
        # Check for privileged containers
        PRIVILEGED_CONTAINERS=$(docker ps --format "{{.Names}}\t{{.Privileged}}" | grep -c "true" || true)
        if [ "$PRIVILEGED_CONTAINERS" -gt 0 ]; then
            print_warning "Found privileged containers"
        else
            print_status "No privileged containers" 0
        fi
        
    else
        print_warning "Docker daemon is not running"
    fi
else
    print_warning "Docker is not installed"
fi

# Check file permissions
echo "🔍 Checking file permissions..."
if [ -d "/opt/content-agent" ]; then
    # Check for world-writable files
    WORLD_WRITABLE=$(find /opt/content-agent -type f -perm -002 2>/dev/null | wc -l)
    if [ "$WORLD_WRITABLE" -gt 0 ]; then
        print_warning "Found $WORLD_WRITABLE world-writable files"
    else
        print_status "No world-writable files found" 0
    fi
    
    # Check for files with SUID/SGID bits
    SUID_FILES=$(find /opt/content-agent -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null | wc -l)
    if [ "$SUID_FILES" -gt 0 ]; then
        print_warning "Found $SUID_FILES files with SUID/SGID bits"
    else
        print_status "No SUID/SGID files found" 0
    fi
else
    print_warning "Content agent directory not found"
fi

# Check network security
echo "🔍 Checking network security..."
if command -v netstat &> /dev/null; then
    # Check for listening ports
    LISTENING_PORTS=$(netstat -tlnp 2>/dev/null | grep LISTEN | wc -l)
    echo "📊 Found $LISTENING_PORTS listening ports"
    
    # Check for ports listening on all interfaces
    ALL_INTERFACE_PORTS=$(netstat -tlnp 2>/dev/null | grep "0.0.0.0:" | wc -l)
    if [ "$ALL_INTERFACE_PORTS" -gt 0 ]; then
        print_warning "Found $ALL_INTERFACE_PORTS ports listening on all interfaces"
    else
        print_status "No ports listening on all interfaces" 0
    fi
fi

# Check SSL/TLS configuration
echo "🔍 Checking SSL/TLS configuration..."
if [ -f "/opt/content-agent/nginx/ssl/cert.pem" ]; then
    if command -v openssl &> /dev/null; then
        CERT_EXPIRY=$(openssl x509 -in /opt/content-agent/nginx/ssl/cert.pem -noout -dates | grep "notAfter" | cut -d= -f2)
        CERT_EXPIRY_EPOCH=$(date -d "$CERT_EXPIRY" +%s 2>/dev/null || echo "0")
        CURRENT_EPOCH=$(date +%s)
        DAYS_UNTIL_EXPIRY=$(( (CERT_EXPIRY_EPOCH - CURRENT_EPOCH) / 86400 ))
        
        if [ "$DAYS_UNTIL_EXPIRY" -lt 30 ]; then
            print_warning "SSL certificate expires in $DAYS_UNTIL_EXPIRY days"
        else
            print_status "SSL certificate is valid for $DAYS_UNTIL_EXPIRY days" 0
        fi
    else
        print_warning "OpenSSL not available for certificate checking"
    fi
else
    print_warning "SSL certificate not found"
fi

# Check for common vulnerabilities
echo "🔍 Checking for common vulnerabilities..."
if [ -f "/opt/content-agent/.env" ]; then
    # Check for hardcoded secrets
    if grep -q "password.*=" /opt/content-agent/.env; then
        print_warning "Found potential hardcoded passwords in .env file"
    else
        print_status "No hardcoded passwords found in .env" 0
    fi
    
    # Check for weak secrets
    if grep -q "SECRET_KEY=.*123\|SECRET_KEY=.*test\|SECRET_KEY=.*demo" /opt/content-agent/.env; then
        print_warning "Found weak secret keys in .env file"
    else
        print_status "No weak secret keys found in .env" 0
    fi
else
    print_warning ".env file not found"
fi

# Check database security
echo "🔍 Checking database security..."
if command -v psql &> /dev/null; then
    if [ -n "$DATABASE_URL" ]; then
        # Check database connection
        if psql "$DATABASE_URL" -c "SELECT 1;" &> /dev/null; then
            print_status "Database connection successful" 0
            
            # Check for default passwords
            if psql "$DATABASE_URL" -c "SELECT 1;" 2>&1 | grep -q "password authentication failed"; then
                print_warning "Database authentication failed"
            fi
        else
            print_warning "Database connection failed"
        fi
    else
        print_warning "DATABASE_URL not set"
    fi
else
    print_warning "PostgreSQL client not available"
fi

# Check Redis security
echo "🔍 Checking Redis security..."
if command -v redis-cli &> /dev/null; then
    if [ -n "$REDIS_URL" ]; then
        # Check Redis connection
        if redis-cli -u "$REDIS_URL" ping &> /dev/null; then
            print_status "Redis connection successful" 0
            
            # Check if Redis requires authentication
            if redis-cli -u "$REDIS_URL" ping 2>&1 | grep -q "NOAUTH"; then
                print_warning "Redis requires authentication"
            fi
        else
            print_warning "Redis connection failed"
        fi
    else
        print_warning "REDIS_URL not set"
    fi
else
    print_warning "Redis client not available"
fi

# Check for malware
echo "🔍 Checking for malware..."
if command -v clamav &> /dev/null; then
    if [ -d "/opt/content-agent/uploads" ]; then
        MALWARE_FOUND=$(clamscan -r /opt/content-agent/uploads 2>/dev/null | grep -c "FOUND" || true)
        if [ "$MALWARE_FOUND" -gt 0 ]; then
            print_warning "Found $MALWARE_FOUND potential malware files"
        else
            print_status "No malware found in uploads" 0
        fi
    else
        print_warning "Uploads directory not found"
    fi
else
    print_warning "ClamAV not available for malware scanning"
fi

# Check log files for security issues
echo "🔍 Checking log files for security issues..."
if [ -d "/opt/content-agent/logs" ]; then
    # Check for failed login attempts
    FAILED_LOGINS=$(grep -c "Failed login" /opt/content-agent/logs/*.log 2>/dev/null || true)
    if [ "$FAILED_LOGINS" -gt 0 ]; then
        print_warning "Found $FAILED_LOGINS failed login attempts in logs"
    else
        print_status "No failed login attempts found in logs" 0
    fi
    
    # Check for error patterns
    ERROR_COUNT=$(grep -c "ERROR\|CRITICAL\|FATAL" /opt/content-agent/logs/*.log 2>/dev/null || true)
    if [ "$ERROR_COUNT" -gt 100 ]; then
        print_warning "Found $ERROR_COUNT errors in logs (high error rate)"
    else
        print_status "Error count in logs is acceptable" 0
    fi
else
    print_warning "Logs directory not found"
fi

# Generate security report
echo "📊 Generating security report..."
REPORT_FILE="/opt/content-agent/logs/security-report-$(date +%Y%m%d-%H%M%S).txt"
{
    echo "Content Repurposing Agent - Security Report"
    echo "Generated: $(date)"
    echo "=========================================="
    echo ""
    echo "System Information:"
    echo "OS: $(uname -a)"
    echo "User: $(whoami)"
    echo "Date: $(date)"
    echo ""
    echo "Security Checks:"
    echo "- Security updates: $SECURITY_UPDATES available"
    echo "- Running containers: $RUNNING_CONTAINERS"
    echo "- Root containers: $ROOT_CONTAINERS"
    echo "- Privileged containers: $PRIVILEGED_CONTAINERS"
    echo "- World-writable files: $WORLD_WRITABLE"
    echo "- SUID/SGID files: $SUID_FILES"
    echo "- Listening ports: $LISTENING_PORTS"
    echo "- All-interface ports: $ALL_INTERFACE_PORTS"
    echo "- SSL certificate expiry: $DAYS_UNTIL_EXPIRY days"
    echo "- Failed logins: $FAILED_LOGINS"
    echo "- Error count: $ERROR_COUNT"
    echo "- Malware found: $MALWARE_FOUND"
    echo ""
    echo "Recommendations:"
    echo "1. Keep system and dependencies updated"
    echo "2. Use non-root users for containers"
    echo "3. Implement proper authentication"
    echo "4. Monitor logs regularly"
    echo "5. Use strong passwords and secrets"
    echo "6. Enable SSL/TLS encryption"
    echo "7. Implement network segmentation"
    echo "8. Regular security audits"
} > "$REPORT_FILE"

echo "📄 Security report saved to: $REPORT_FILE"

# Final summary
echo ""
echo "🔍 Security scan completed!"
echo "📊 Summary:"
echo "  - System security: $(if [ $SECURITY_UPDATES -eq 0 ]; then echo "Good"; else echo "Needs attention"; fi)"
echo "  - Container security: $(if [ $ROOT_CONTAINERS -eq 0 ] && [ $PRIVILEGED_CONTAINERS -eq 0 ]; then echo "Good"; else echo "Needs attention"; fi)"
echo "  - File security: $(if [ $WORLD_WRITABLE -eq 0 ] && [ $SUID_FILES -eq 0 ]; then echo "Good"; else echo "Needs attention"; fi)"
echo "  - Network security: $(if [ $ALL_INTERFACE_PORTS -eq 0 ]; then echo "Good"; else echo "Needs attention"; fi)"
echo "  - SSL/TLS: $(if [ $DAYS_UNTIL_EXPIRY -gt 30 ]; then echo "Good"; else echo "Needs attention"; fi)"
echo ""
echo "📋 Next steps:"
echo "1. Review the security report: $REPORT_FILE"
echo "2. Address any warnings or issues found"
echo "3. Run this scan regularly (weekly recommended)"
echo "4. Implement additional security measures as needed"
echo "5. Consider professional security audit for production"
