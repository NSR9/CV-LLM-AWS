#!/bin/bash

# AI Vision Explorer - Launch Script
# ===================================
# This script launches the AI Vision Explorer application with optimal settings

echo "🔍 AI Vision Explorer - Launching..."
echo "====================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.10+ and try again"
    exit 1
fi

# Check if Streamlit is available
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "❌ Error: Streamlit is not installed"
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Check if the app directory exists
if [ ! -f "cv-kernel-playground/app.py" ]; then
    echo "❌ Error: Application file not found"
    echo "Please ensure you're in the correct directory"
    exit 1
fi

echo "✅ Dependencies checked"
echo "🚀 Launching AI Vision Explorer..."

# Launch the application with optimal settings
streamlit run cv-kernel-playground/app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless false \
    --browser.gatherUsageStats false \
    --theme.base light \
    --theme.primaryColor "#6366f1" \
    --theme.backgroundColor "#f8fafc" \
    --theme.secondaryBackgroundColor "#ffffff" \
    --theme.textColor "#1e293b"

echo "🌐 Application should open in your browser at: http://localhost:8501"
echo "📱 Mobile users can access at: http://YOUR_IP:8501"
echo ""
echo "💡 Tips:"
echo "   - Use Ctrl+C to stop the application"
echo "   - Check the terminal for any error messages"
echo "   - Ensure you have sufficient RAM (4GB+) for model loading"
