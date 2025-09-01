# �� AI Vision Explorer - Multimodal Analysis

Advanced Computer Vision Analysis with Grad-CAM interpretability and multimodal AI capabilities using Gemini and Gemma models.

## 🌟 Features

### 🤖 AI Image Analysis
- **Gemini 1.5 Pro**: Google's most capable multimodal model
- **BLIP VQA (Local)**: Local Visual Question Answering model for offline use
- **Gemma 2 Models**: Open multimodal models via Hugging Face
- **Natural Language Questions**: Ask any question about uploaded images
- **Real-time Analysis**: Get instant AI-powered insights

### 🎯 Grad-CAM Analysis
- **Multiple Models**: ResNet-18, ResNet-50, VGG-16
- **Layer Analysis**: Analyze different convolutional layers
- **Interactive Visualizations**: Heatmaps, predictions, and confidence scores
- **Customizable Parameters**: Opacity, colormaps, blur effects

### 🎨 Modern UI
- **Dark Theme**: Professional dark color scheme
- **Responsive Design**: Works on desktop and mobile
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Real-time Feedback**: Loading states and progress indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- API keys for Gemini and/or Hugging Face (optional for local BLIP model)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd session3
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys (optional)**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_token_here
```

4. **Download local BLIP model (optional)**
```bash
python download_blip_model.py
```

5. **Run the application**
```bash
streamlit run image_analysis_app.py
```

6. **Access the app**
Open your browser and go to `http://localhost:8501`

## 🔑 API Setup Instructions

### Google Gemini API

1. **Visit Google AI Studio**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account

2. **Create a Project**
   - Click "Create Project" or select an existing project
   - Give your project a name

3. **Enable Gemini API**
   - In the project dashboard, go to "APIs & Services" → "Library"
   - Search for "Gemini API"
   - Click "Enable"

4. **Create API Key**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the generated API key

5. **Set Usage Limits (Optional)**
   - Go to "APIs & Services" → "Quotas"
   - Set daily limits to control costs

### Hugging Face API

1. **Create Account**
   - Visit [Hugging Face](https://huggingface.co/)
   - Click "Sign Up" and create an account

2. **Access Token Settings**
   - Click on your profile picture → "Settings"
   - Go to "Access Tokens" in the left sidebar

3. **Create New Token**
   - Click "New token"
   - Give it a name (e.g., "AI Vision Explorer")
   - Select "Read" role (minimum required)
   - Click "Generate token"

4. **Copy Token**
   - Copy the generated token immediately
   - Store it securely (you won't see it again)

## 🏗️ AWS EC2 Deployment

### Instance Setup

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS
   - Select t3.medium or larger for better performance
   - Configure security groups (see below)

2. **Security Group Configuration**
   ```
   Inbound Rules:
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom TCP (8501) - 0.0.0.0/0 (for Streamlit)
   
   Outbound Rules:
   - All Traffic - 0.0.0.0/0
   ```

3. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```

### Installation on EC2

1. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python and Dependencies**
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Application Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Environment Variables**
   ```bash
   echo "GEMINI_API_KEY=your_gemini_api_key_here" >> .env
   echo "HUGGINGFACE_API_KEY=your_huggingface_token_here" >> .env
   ```

6. **Run Application**
   ```bash
   streamlit run image_analysis_app.py --server.port 8501 --server.address 0.0.0.0
   ```

### Production Deployment (Optional)

For production use, consider using a process manager like `systemd`:

1. **Create Service File**
   ```bash
   sudo nano /etc/systemd/system/ai-vision-explorer.service
   ```

2. **Add Service Configuration**
   ```ini
   [Unit]
   Description=AI Vision Explorer
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/session3
   Environment=PATH=/home/ubuntu/session3/venv/bin
   ExecStart=/home/ubuntu/session3/venv/bin/streamlit run image_analysis_app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start Service**
   ```bash
   sudo systemctl enable ai-vision-explorer
   sudo systemctl start ai-vision-explorer
   ```

## 📊 Model Information

### Gemini 1.5 Pro
- **Provider**: Google
- **Capabilities**: Text, image, video, audio, code
- **Max Input**: 2M tokens
- **Pricing**: Pay per use (~$0.0025 per 1M input tokens)
- **Best For**: High-quality multimodal analysis
- **API Endpoint**: `https://generativelanguage.googleapis.com/`

### BLIP VQA (Local)
- **Provider**: Salesforce (local deployment)
- **Capabilities**: Visual Question Answering
- **Model Size**: ~990M parameters
- **Pricing**: Free (runs locally)
- **Best For**: Offline analysis, privacy-focused applications
- **Setup**: Download once with `python download_blip_model.py`

### Gemma 2 Models
- **Provider**: Google (via Hugging Face)
- **Capabilities**: Text and image understanding
- **Available Models**:
  - **Gemma 2 2B IT**: Fast, lightweight
  - **Gemma 2 9B IT**: Balanced performance
  - **Gemma 2 27B IT**: High accuracy
- **Pricing**: Free via Hugging Face
- **Best For**: Cost-effective analysis
- **API Endpoint**: `https://api-inference.huggingface.co/`

## 🎯 Usage Guide

### AI Image Analysis

1. **Select Analysis Mode**
   - Choose "AI Image Analysis" or "Both" from the sidebar

2. **Choose AI Model**
   - **Gemini**: For high-quality, comprehensive analysis
   - **BLIP Local**: For offline, privacy-focused analysis
   - **Gemma**: For cost-effective, open-source analysis

3. **Enter API Key (if using cloud models)**
   - Paste your API key in the sidebar
   - Keys are stored securely in session
   - Not required for local BLIP model

4. **Upload Image**
   - Supported formats: JPG, PNG, BMP, TIFF
   - High-resolution images work best

5. **Ask Questions**
   - Be specific: "What objects do you see in this image?"
   - Ask about relationships: "How are the objects arranged?"
   - Request descriptions: "Describe the scene in detail"

### Grad-CAM Analysis

1. **Select Analysis Mode**
   - Choose "Grad-CAM Analysis" or "Both"

2. **Configure Parameters**
   - **Model**: Choose ResNet-18, ResNet-50, or VGG-16
   - **Layer**: Select which convolutional layer to analyze
   - **Opacity**: Adjust heatmap transparency
   - **Colormap**: Choose visualization color scheme

3. **Upload and Analyze**
   - Upload an image
   - Select target class from predictions
   - View attention heatmaps and predictions

## 🔧 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify API key is correct and active
   - Check account billing status (Gemini)
   - Ensure token has proper permissions (Hugging Face)

2. **Model Loading Issues**
   - Check internet connection
   - Verify model names are correct
   - Try different model sizes

3. **Performance Issues**
   - Use smaller images for faster processing
   - Choose smaller models for better speed
   - Consider upgrading EC2 instance size

4. **Deployment Issues**
   - Check security group settings
   - Verify port 8501 is open
   - Ensure environment variables are set

### Error Messages

- **"API Error: 401"**: Invalid API key
- **"API Error: 429"**: Rate limit exceeded
- **"Model not found"**: Check model name spelling
- **"Connection timeout"**: Check network connectivity

## 📈 Performance Optimization

### For Better Speed
- Use smaller images (1024x1024 max)
- Choose smaller models (Gemma 2B vs 27B)
- Enable caching with `@st.cache_data`

### For Better Quality
- Use high-resolution images
- Choose larger models (Gemini Pro, Gemma 27B)
- Ask specific, detailed questions

### For Cost Optimization
- Use Gemma models (free) for testing
- Set usage limits in Google Cloud Console
- Monitor API usage regularly

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for Gemini API
- Hugging Face for model hosting
- Streamlit for the web framework
- PyTorch for deep learning capabilities

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation for your chosen model

---

**Happy Analyzing! 🚀**
