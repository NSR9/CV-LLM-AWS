#!/bin/bash

# EC2 Storage Upgrade Guide
# This script provides instructions for upgrading EC2 storage

echo "💾 EC2 Storage Upgrade Guide"
echo "============================"

echo ""
echo "📊 Current disk usage:"
df -h

echo ""
echo "🔧 Storage Upgrade Options:"
echo ""
echo "Option 1: Stop Instance and Modify Volume"
echo "1. Stop your EC2 instance"
echo "2. Go to EC2 Console → Volumes"
echo "3. Select your root volume"
echo "4. Actions → Modify Volume"
echo "5. Increase size to 50GB or more"
echo "6. Start instance"
echo ""

echo "Option 2: Add New EBS Volume"
echo "1. Go to EC2 Console → Volumes"
echo "2. Create Volume (50GB recommended)"
echo "3. Attach to your instance"
echo "4. Mount the new volume"
echo ""

echo "Option 3: Use Larger Instance Type"
echo "1. Stop your EC2 instance"
echo "2. Actions → Instance Settings → Change Instance Type"
echo "3. Choose t3.large (8GB RAM, more storage)"
echo "4. Start instance"
echo ""

echo "Option 4: Continue with Minimal Installation"
echo "The deployment script now supports ultra-minimal installation"
echo "This will work with your current storage but with limited features"
echo ""

echo "💡 Recommended Action:"
echo "For best experience: Upgrade to t3.large with 50GB storage"
echo "For quick test: Use ultra-minimal installation"
echo ""

echo "🚀 To continue with minimal installation:"
echo "wget https://raw.githubusercontent.com/NSR9/CV-LLM-AWS/clean-dev/deploy_ec2.sh"
echo "chmod +x deploy_ec2.sh"
echo "./deploy_ec2.sh"
