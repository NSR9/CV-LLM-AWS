#!/bin/bash

# Quick Disk Space Fix Script for EC2
# Run this on your EC2 instance to free up space

echo "🔧 EC2 Disk Space Fix Script"
echo "============================"

# Check current disk usage
echo "📊 Current disk usage:"
df -h

echo ""
echo "🧹 Cleaning up system..."

# Clean package cache
echo "Cleaning package cache..."
sudo apt clean
sudo apt autoremove -y

# Remove old log files
echo "Removing old log files..."
sudo find /var/log -name "*.log" -mtime +7 -delete 2>/dev/null || true

# Clear pip cache
echo "Clearing pip cache..."
pip cache purge 2>/dev/null || true

# Remove temporary files
echo "Removing temporary files..."
sudo rm -rf /tmp/* 2>/dev/null || true

# Check disk usage after cleanup
echo ""
echo "📊 Disk usage after cleanup:"
df -h

echo ""
echo "💡 Recommendations:"
echo "1. If still low on space, consider upgrading to t3.large with 50GB+ storage"
echo "2. Or add an additional EBS volume"
echo "3. The deployment script now includes automatic disk space management"

echo ""
echo "🚀 Ready to retry deployment!"

