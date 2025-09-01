# 🚀 EC2 Setup Guide for AI Vision Explorer

## 📋 Instance Recommendations

### **Recommended EC2 Instance Types**

#### **For Development/Testing:**
- **t3.medium** (2 vCPU, 4 GB RAM)
  - Cost: ~$30/month
  - Good for: Testing, small workloads
  - Limitations: CPU-only, slower inference

#### **For Production (CPU-only):**
- **t3.large** (2 vCPU, 8 GB RAM)
  - Cost: ~$60/month
  - Good for: Production workloads
  - Better performance than t3.medium

- **c6i.large** (2 vCPU, 4 GB RAM)
  - Cost: ~$70/month
  - Good for: Compute-intensive workloads
  - Optimized for CPU performance

#### **For Production (with GPU):**
- **g4dn.xlarge** (4 vCPU, 16 GB RAM, 1 GPU)
  - Cost: ~$400/month
  - Good for: GPU-accelerated inference
  - NVIDIA T4 GPU included

- **g5.xlarge** (4 vCPU, 16 GB RAM, 1 GPU)
  - Cost: ~$500/month
  - Good for: Latest GPU acceleration
  - NVIDIA A10G GPU included

### **Storage Recommendations**

#### **Root Volume:**
- **Size**: 20-50 GB
- **Type**: gp3 (SSD)
- **IOPS**: 3000 (default)

#### **Additional Storage (for models):**
- **Size**: 50-100 GB
- **Type**: gp3 (SSD)
- **Purpose**: Store BLIP model and other large files

## 🔧 Step-by-Step EC2 Setup

### **Step 1: Launch EC2 Instance**

1. **Go to AWS Console** → **EC2** → **Launch Instance**

2. **Choose Instance Type:**
   ```
   Name: AI Vision Explorer
   Instance Type: t3.large (recommended for start)
   ```

3. **Configure Instance:**
   ```
   Number of instances: 1
   Network: Default VPC
   Subnet: Default subnet
   ```

4. **Storage Configuration:**
   ```
   Root volume: 50 GB gp3
   Additional volume: 100 GB gp3 (optional)
   ```

5. **Security Groups:**
   ```
   Name: ai-vision-explorer-sg
   Description: Security group for AI Vision Explorer
   
   Inbound Rules:
   - SSH (22) - 0.0.0.0/0 (your IP only)
   - Custom TCP (8501) - 0.0.0.0/0
   
   Outbound Rules:
   - All Traffic - 0.0.0.0/0
   ```

6. **Key Pair:**
   - Create new key pair or use existing
   - Download the .pem file securely

### **Step 2: Connect to Instance**

```bash
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# Make key file secure
chmod 400 your-key.pem
```

### **Step 3: Deploy Application**

#### **Option A: Automated Deployment (Recommended)**
```bash
# Download deployment script
wget https://raw.githubusercontent.com/yourusername/ai-vision-explorer/main/deploy_ec2.sh

# Make executable
chmod +x deploy_ec2.sh

# Run deployment
./deploy_ec2.sh
```

#### **Option B: Manual Deployment**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Clone repository
git clone https://github.com/yourusername/ai-vision-explorer.git
cd ai-vision-explorer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Download BLIP model
python download_blip_model.py

# Run application
streamlit run image_analysis_app.py --server.port 8501 --server.address 0.0.0.0
```

### **Step 4: Configure Environment**

```bash
# Create environment file
nano .env

# Add your API keys (optional)
GEMINI_API_KEY=your_gemini_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_token_here
```

### **Step 5: Test Application**

1. **Get your EC2 public IP**
2. **Open browser**: `http://your-ec2-public-ip:8501`
3. **Test features**:
   - Upload an image
   - Try Grad-CAM analysis
   - Test BLIP local model
   - Test Gemini (if API key provided)

**Note**: The application runs directly on port 8501 without a reverse proxy for simplicity.

## 🔒 Security Best Practices

### **Firewall Configuration**
```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 8501
```

### **SSH Security**
```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Restart SSH
sudo systemctl restart ssh
```

### **Regular Updates**
```bash
# Set up automatic updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 📊 Monitoring and Maintenance

### **System Monitoring**
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Check system resources
htop
df -h
free -h
```

### **Application Logs**
```bash
# View application logs
sudo journalctl -u ai-vision-explorer -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **Backup Strategy**
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p $BACKUP_DIR

# Backup application
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /home/ubuntu/ai-vision-explorer

# Backup models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz /home/ubuntu/ai-vision-explorer/models

echo "Backup completed: $BACKUP_DIR/app_$DATE.tar.gz"
EOF

chmod +x backup.sh
```

## 💰 Cost Optimization

### **Instance Scheduling**
```bash
# Create start/stop scripts
cat > start_instance.sh << 'EOF'
#!/bin/bash
aws ec2 start-instances --instance-ids i-1234567890abcdef0
echo "Instance starting..."
EOF

cat > stop_instance.sh << 'EOF'
#!/bin/bash
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
echo "Instance stopping..."
EOF
```

### **Spot Instances (for cost savings)**
- Use Spot Instances for non-critical workloads
- Set up Spot Fleet for high availability
- Monitor spot prices and availability

## 🚨 Troubleshooting

### **Common Issues**

1. **Application won't start**
   ```bash
   # Check logs
   sudo journalctl -u ai-vision-explorer -f
   
   # Check port availability
   sudo netstat -tlnp | grep 8501
   ```

2. **Model download fails**
   ```bash
   # Check disk space
   df -h
   
   # Check internet connectivity
   ping google.com
   
   # Retry download
   python download_blip_model.py
   ```

3. **High memory usage**
   ```bash
   # Check memory usage
   free -h
   
   # Restart application
   sudo systemctl restart ai-vision-explorer
   ```

### **Performance Tuning**

1. **Increase swap space**
   ```bash
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

2. **Optimize Python settings**
   ```bash
   # Add to .env
   export PYTHONOPTIMIZE=1
   export PYTHONUNBUFFERED=1
   ```

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review application logs
- Monitor system resources
- Consider upgrading instance type if needed

---

**Happy Deploying! 🚀**
