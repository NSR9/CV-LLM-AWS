#!/bin/bash

# AI Vision Explorer - Launch Script
# This script launches the enhanced AI Vision Explorer application

echo "🚀 Starting AI Vision Explorer..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure you're in the correct directory."
    exit 1
fi

# Check if the main app file exists
if [ ! -f "image_analysis_app.py" ]; then
    echo "❌ image_analysis_app.py not found. Please ensure you're in the correct directory."
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip3 install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# AI Vision Explorer - Environment Variables
# Add your API keys here

# Google Gemini API Key (optional)
GEMINI_API_KEY=your_gemini_api_key_here

# Hugging Face API Token (optional)
HUGGINGFACE_API_KEY=your_huggingface_token_here
EOF
    echo "📝 Created .env template. Please add your API keys before using AI features."
fi

# Launch the application
echo "🎯 Launching AI Vision Explorer..."
echo "🌐 The app will be available at: http://localhost:8501"
echo "🔄 Press Ctrl+C to stop the application"
echo ""

# Run Streamlit with proper configuration
streamlit run image_analysis_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless false \
    --browser.gatherUsageStats false
