#!/bin/bash

# AI Vision Explorer - EC2 Deployment Script
# This script sets up the complete environment on an EC2 instance

set -e  # Exit on any error

echo "🚀 AI Vision Explorer - EC2 Deployment Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Use a regular user account."
    exit 1
fi

# Check initial disk space
print_status "Checking available disk space..."
TOTAL_SPACE=$(df /home/ubuntu | awk 'NR==2 {print $2}')
AVAILABLE_SPACE=$(df /home/ubuntu | awk 'NR==2 {print $4}')
USED_SPACE=$(df /home/ubuntu | awk 'NR==2 {print $3}')

print_status "Disk space summary:"
print_status "  Total: $((TOTAL_SPACE / 1024 / 1024))GB"
print_status "  Used: $((USED_SPACE / 1024 / 1024))GB"
print_status "  Available: $((AVAILABLE_SPACE / 1024 / 1024))GB"

if [ "$AVAILABLE_SPACE" -lt 3000000 ]; then  # Less than 3GB
    print_warning "Low disk space detected. Installation may fail."
    print_warning "Consider using an EC2 instance with more storage."
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    git \
    curl \
    wget \
    unzip \
    htop \
    ufw \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install CUDA if GPU is available (optional)
if command -v nvidia-smi &> /dev/null; then
    print_status "NVIDIA GPU detected. Installing CUDA support..."
    # Add NVIDIA repository
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt update
    sudo apt install -y cuda-toolkit-12-0
    print_success "CUDA installed successfully"
else
    print_warning "No NVIDIA GPU detected. Running on CPU only."
fi

# Create application directory
APP_DIR="/home/ubuntu/ai-vision-explorer"
print_status "Creating application directory: $APP_DIR"
mkdir -p $APP_DIR
cd $APP_DIR

# Clone repository (if not already present)
if [ ! -d ".git" ]; then
    print_status "Cloning repository..."
    git clone -b clean-dev https://github.com/NSR9/CV-LLM-AWS.git .
else
    print_status "Repository already exists. Pulling latest changes..."
    # Try to pull with merge strategy first
    if ! git pull origin clean-dev; then
        print_warning "Standard pull failed. Trying alternative strategies..."
        
        # Option 1: Try with allow-unrelated-histories
        if git pull origin clean-dev --allow-unrelated-histories; then
            print_success "Successfully pulled with unrelated histories merge"
        else
            print_warning "Pull with unrelated histories failed. Trying reset strategy..."
            
            # Option 2: Reset to remote branch
            git fetch origin clean-dev
            git reset --hard origin/clean-dev
            print_success "Reset to remote clean-dev branch"
        fi
    fi
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."

# Check available disk space before installation
AVAILABLE_SPACE=$(df /home/ubuntu | awk 'NR==2 {print $4}')
REQUIRED_SPACE=5000000  # 5GB in KB

if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
    print_warning "Low disk space detected: ${AVAILABLE_SPACE}KB available"
    print_warning "Recommended: At least 5GB free space for installation"
    
    # Try to free up some space
    print_status "Attempting to free up disk space..."
    sudo apt clean
    sudo apt autoremove -y
    
    # Check space again
    AVAILABLE_SPACE=$(df /home/ubuntu | awk 'NR==2 {print $4}')
    if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
        print_error "Insufficient disk space after cleanup. Please increase EC2 storage or use a larger instance."
        print_error "Available: ${AVAILABLE_SPACE}KB, Required: ${REQUIRED_SPACE}KB"
        exit 1
    fi
fi

# Install dependencies with space monitoring
print_status "Installing Python dependencies (this may take several minutes)..."

# Choose requirements file based on available space
if [ "$AVAILABLE_SPACE" -lt 8000000 ]; then  # Less than 8GB
    print_warning "Limited disk space detected. Using minimal requirements."
    REQUIREMENTS_FILE="requirements-minimal.txt"
    
    # Check if minimal requirements file exists
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_error "Minimal requirements file not found. Using standard requirements."
        REQUIREMENTS_FILE="requirements.txt"
    fi
else
    REQUIREMENTS_FILE="requirements.txt"
fi

print_status "Using requirements file: $REQUIREMENTS_FILE"

if ! pip install -r "$REQUIREMENTS_FILE"; then
    print_error "Failed to install Python dependencies"
    print_error "This may be due to insufficient disk space or network issues"
    print_error "Please check your EC2 instance storage and try again"
    
    # Try minimal installation as fallback
    if [ "$REQUIREMENTS_FILE" != "requirements-minimal.txt" ] && [ -f "requirements-minimal.txt" ]; then
        print_warning "Trying minimal installation as fallback..."
        if pip install -r requirements-minimal.txt; then
            print_success "Minimal installation successful"
        else
            print_error "Both standard and minimal installations failed"
            exit 1
        fi
    else
        exit 1
    fi
fi

# Install PyTorch separately if using minimal requirements
if [ "$REQUIREMENTS_FILE" = "requirements-minimal.txt" ]; then
    print_status "Installing PyTorch separately for local model support..."
    
    # Check if PyTorch is needed (if BLIP model will be downloaded)
    if [ -f "download_blip_model.py" ]; then
        print_status "Installing PyTorch for BLIP model..."
        if ! pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu; then
            print_warning "PyTorch installation failed. BLIP local model will not be available."
            print_warning "You can still use Gemini cloud model."
        else
            print_success "PyTorch installed successfully"
        fi
    fi
fi

# Download BLIP model (optional)
print_status "Setting up BLIP model..."
if [ -f "download_blip_model.py" ]; then
    # Check if PyTorch is available for BLIP
    if python -c "import torch; print('PyTorch available')" 2>/dev/null; then
        python download_blip_model.py
    else
        print_warning "PyTorch not available. Skipping BLIP model download."
        print_warning "You can still use Gemini cloud model for image analysis."
    fi
else
    print_warning "download_blip_model.py not found. Skipping BLIP model download."
fi

# Create environment file
print_status "Creating environment file..."
cat > .env << EOF
# AI Vision Explorer Environment Variables
# Add your API keys here (optional for local BLIP model)

# Google Gemini API (optional)
# GEMINI_API_KEY=your_gemini_api_key_here

# Hugging Face API (optional)
# HUGGINGFACE_API_KEY=your_huggingface_token_here

# Application settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
EOF

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/ai-vision-explorer.service > /dev/null << EOF
[Unit]
Description=AI Vision Explorer
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
Environment=HOME=/home/ubuntu
ExecStart=$APP_DIR/venv/bin/streamlit run image_analysis_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure firewall
print_status "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 8501

# Enable and start the service
print_status "Starting AI Vision Explorer service..."
sudo systemctl daemon-reload
sudo systemctl enable ai-vision-explorer
sudo systemctl start ai-vision-explorer

# Wait for service to start
sleep 5

# Check service status
if sudo systemctl is-active --quiet ai-vision-explorer; then
    print_success "AI Vision Explorer service is running!"
else
    print_error "Service failed to start. Check logs with: sudo journalctl -u ai-vision-explorer"
    exit 1
fi

# Get instance metadata
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Display deployment information
echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Application URL: http://$PUBLIC_IP:8501"
echo "Instance ID: $INSTANCE_ID"
echo "Application Directory: $APP_DIR"
echo ""
echo "📋 Useful Commands:"
echo "  Check service status: sudo systemctl status ai-vision-explorer"
echo "  View logs: sudo journalctl -u ai-vision-explorer -f"
echo "  Restart service: sudo systemctl restart ai-vision-explorer"
echo "  Stop service: sudo systemctl stop ai-vision-explorer"
echo ""
echo "🔧 Configuration:"
echo "  Environment file: $APP_DIR/.env"
echo "  Service file: /etc/systemd/system/ai-vision-explorer.service"
echo ""
echo "⚠️  Next Steps:"
echo "  1. Add your API keys to $APP_DIR/.env (optional)"
echo "  2. Test the application at http://$PUBLIC_IP:8501"
echo "  3. Access directly via port 8501 (no reverse proxy)"
echo ""

print_success "Deployment completed successfully!"
