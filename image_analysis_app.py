"""
AI Vision Explorer - Enhanced Version
Combines Grad-CAM analysis with multimodal AI image analysis using Gemini and Gemma models
"""

import io
import numpy as np
import streamlit as st
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms as T
from torchvision import models
import plotly.graph_objects as go
import plotly.express as px
from typing import Tuple, Dict, Any
import time
import os
from dotenv import load_dotenv

# Import our AI models module
from ai_models import AIModelFactory, validate_api_key, get_model_info

# Load environment variables
load_dotenv()

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="🔍 AI Vision Explorer - Multimodal Analysis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ai-vision-explorer/issues',
        'Report a bug': 'https://github.com/yourusername/ai-vision-explorer/issues',
        'About': '# AI Vision Explorer\nAdvanced Computer Vision Analysis with Multimodal AI'
    }
)

# ==================== CUSTOM CSS FOR WORLD-CLASS UI ====================
st.markdown("""
<style>
    /* Modern dark color scheme and typography */
    :root {
        --primary-color: #8b5cf6;
        --secondary-color: #a855f7;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-color: #0f0f23;
        --surface-color: #1a1a2e;
        --card-color: #16213e;
        --border-color: #2d3748;
        --text-primary: #f7fafc;
        --text-secondary: #a0aec0;
        --text-muted: #718096;
    }
    
    /* Custom styling for better visual hierarchy */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: var(--text-primary);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
        border: 1px solid var(--border-color);
    }
    
    .metric-card {
        background: var(--card-color);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        color: var(--text-primary);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);
        border-color: var(--primary-color);
    }
    
    .upload-area {
        border: 2px dashed var(--primary-color);
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        background: linear-gradient(135deg, var(--surface-color), var(--card-color));
        transition: all 0.3s ease;
        color: var(--text-primary);
    }
    
    .upload-area:hover {
        border-color: var(--secondary-color);
        background: linear-gradient(135deg, var(--card-color), var(--border-color));
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
    }
    
    .sidebar-section {
        background: var(--card-color);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .prediction-bar {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        height: 8px;
        border-radius: 4px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: var(--text-primary);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(139, 92, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
        background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
    }
    
    /* Custom slider styling */
    .stSlider > div > div > div > div {
        background: var(--primary-color);
    }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div > div > div {
        border-color: var(--primary-color);
    }
    
    /* Dark theme overrides for Streamlit components */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-primary);
    }
    
    .stMarkdown {
        color: var(--text-primary);
    }
    
    .stText {
        color: var(--text-primary);
    }
    
    /* Ensure all text is readable on dark background */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
    }
    
    p, span, div {
        color: var(--text-primary);
    }
    
    /* Dark theme for Streamlit sidebar */
    .css-1d391kg {
        background-color: var(--surface-color);
    }
    
    /* Dark theme for Streamlit main content */
    .main .block-container {
        background-color: var(--background-color);
        color: var(--text-primary);
    }
    
    /* Enhanced dark theme styling */
    .stSelectbox > div > div > div > div {
        background-color: var(--card-color);
        border-color: var(--border-color);
        color: var(--text-primary);
    }
    
    .stSlider > div > div > div > div {
        background-color: var(--primary-color);
    }
    
    .stSlider > div > div > div > div > div {
        background-color: var(--border-color);
    }
    
    /* File uploader dark theme */
    .stFileUploader > div > div > div {
        background-color: var(--card-color);
        border-color: var(--border-color);
        color: var(--text-primary);
    }
    
    /* Metrics dark theme */
    .stMetric > div > div > div {
        background-color: var(--card-color);
        border-color: var(--border-color);
        color: var(--text-primary);
    }
    
    /* Responsive grid improvements */
    .stColumns > div {
        gap: 2rem;
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid var(--border-color);
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Scrollbar styling for dark theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface-color);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-color);
    }
    
    /* AI Analysis Results Styling */
    .ai-analysis-card {
        background: var(--card-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .ai-analysis-card.success {
        border-left: 4px solid var(--success-color);
    }
    
    .ai-analysis-card.error {
        border-left: 4px solid var(--error-color);
    }
    
    .model-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent-color), var(--primary-color));
        color: var(--text-primary);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR CONFIGURATION ====================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h3>🎛️ Analysis Controls</h3>
        <p style="color: var(--text-secondary); font-size: 0.9rem;">
            Configure your analysis parameters
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analysis mode selection
    analysis_mode = st.selectbox(
        "🔍 Analysis Mode",
        ["Grad-CAM Analysis", "AI Image Analysis", "Both"],
        help="Choose between traditional Grad-CAM analysis, AI-powered image analysis, or both"
    )
    
    # AI Model Configuration (only show if AI analysis is selected)
    if analysis_mode in ["AI Image Analysis", "Both"]:
        st.markdown("""
        <div class="sidebar-section">
            <h4>🤖 AI Model Settings</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Model selection
        ai_model_type = st.selectbox(
            "🧠 AI Model",
            ["Gemini", "BLIP Local"],
            help="Choose between Gemini (cloud) or BLIP (local) for image analysis"
        )
        

        
        # API Key input (only for Gemini)
        if ai_model_type == "Gemini":
            api_key = st.text_input(
                "🔑 API Key",
                type="password",
                help="Enter your Gemini API key"
            )
        else:
            api_key = None  # Local model doesn't need API key
        

        
        # Show model info
        model_info = get_model_info(ai_model_type)
        if model_info:
            st.markdown(f"""
            <div class="sidebar-section">
                <h5>📊 Model Information</h5>
                <p style="font-size: 0.8rem; color: var(--text-secondary);">
                    <strong>Name:</strong> {model_info['name']}<br>
                    <strong>Description:</strong> {model_info['description']}<br>
                    <strong>Capabilities:</strong> {model_info['capabilities']}<br>
                    <strong>Max Input:</strong> {model_info['max_input']}<br>
                    <strong>Pricing:</strong> {model_info['pricing']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show setup instructions for local model
            if ai_model_type == "BLIP Local":
                st.markdown("""
                <div class="sidebar-section">
                    <h5>🔧 Local Model Setup</h5>
                    <p style="font-size: 0.8rem; color: var(--text-secondary);">
                        <strong>First time setup:</strong><br>
                        Run this command to download the model:<br>
                        <code>python download_blip_model.py</code>
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Grad-CAM Configuration (only show if Grad-CAM analysis is selected)
    if analysis_mode in ["Grad-CAM Analysis", "Both"]:
        st.markdown("""
        <div class="sidebar-section">
            <h4>🎯 Grad-CAM Settings</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Model selection
        model_option = st.selectbox(
            "🤖 Model Architecture",
            ["ResNet-18 (ImageNet)", "ResNet-50 (ImageNet)", "VGG-16 (ImageNet)"],
            help="Choose the pre-trained model for analysis"
        )
        
        # Layer selection with better descriptions
        LAYER_OPTIONS = {
            "layer4 (Final Conv)": "layer4",
            "layer3 (Mid-level Features)": "layer3", 
            "layer2 (Early Features)": "layer2",
            "layer1 (Basic Features)": "layer1",
        }
        
        layer_name = st.selectbox(
            "🎯 Target Layer",
            list(LAYER_OPTIONS.keys()),
            index=0,
            help="Select which convolutional layer to analyze. Later layers capture higher-level features."
        )
        
        # Enhanced controls
        alpha = st.slider(
            "🎨 Heatmap Opacity",
            0.0, 1.0, 0.6, 0.05,
            help="Adjust the transparency of the Grad-CAM overlay"
        )
        
        colormap = st.selectbox(
            "🌈 Color Scheme",
            ["jet", "viridis", "plasma", "inferno", "magma"],
            help="Choose the color scheme for the heatmap visualization"
        )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            blur_radius = st.slider("🔍 Blur Radius", 0, 10, 3, help="Apply Gaussian blur to smooth the heatmap")
            threshold = st.slider("📊 Confidence Threshold", 0.0, 1.0, 0.1, 0.05, help="Minimum confidence for predictions")

# ==================== MAIN HEADER ====================
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🔍 AI Vision Explorer</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
        Advanced Computer Vision Analysis with Multimodal AI
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.8;">
        Upload an image → Analyze with AI → Understand what the model sees
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== GRAD-CAM MODEL SETUP ====================
@st.cache_resource
def load_model():
    """Load the selected pre-trained model"""
    # Original code: m = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    if "ResNet-18" in model_option:
        m = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    elif "ResNet-50" in model_option:
        m = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    else:  # VGG-16
        m = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
    
    m.eval()
    return m

# ==================== ENHANCED GRAD-CAM IMPLEMENTATION ====================
activations = {}
gradients = {}

def hook_forward(module, inp, out):
    """Store activations for Grad-CAM computation"""
    # Original code: activations["value"] = out
    activations["value"] = out

def hook_backward(module, grad_in, grad_out):
    """Store gradients for Grad-CAM computation"""
    # Original code: gradients["value"] = grad_out[0]
    gradients["value"] = grad_out[0]

def get_target_layer(model, name: str):
    """Get the target layer from the model"""
    # Original code: return getattr(model, name)
    return getattr(model, name)

# ==================== IMAGE PREPROCESSING ====================
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

preprocess = T.Compose([
    T.Resize(256, interpolation=T.InterpolationMode.BICUBIC),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

@st.cache_data
def load_imagenet_labels():
    """Load ImageNet class labels"""
    # Original code: return models.ResNet18_Weights.IMAGENET1K_V1.meta["categories"]
    if "ResNet-18" in model_option:
        return models.ResNet18_Weights.IMAGENET1K_V1.meta["categories"]
    elif "ResNet-50" in model_option:
        return models.ResNet50_Weights.IMAGENET1K_V1.meta["categories"]
    else:  # VGG-16
        return models.VGG16_Weights.IMAGENET1K_V1.meta["categories"]

# ==================== ENHANCED UTILITY FUNCTIONS ====================
def tensor_to_pil(t: torch.Tensor) -> Image.Image:
    """Convert tensor to PIL image with enhanced processing"""
    # Original code: t = t.detach().cpu().clamp(0, 1)
    t = t.detach().cpu().clamp(0, 1)
    if t.ndim == 3:
        t = t.permute(1,2,0).numpy()
        t = (t * 255).astype(np.uint8)
        return Image.fromarray(t)
    raise ValueError("Expected 3D CHW tensor")

def overlay_heatmap(img: Image.Image, heat: np.ndarray, alpha=0.6, colormap="jet") -> Image.Image:
    """Create enhanced heatmap overlay with multiple colormap options"""
    # Original code: heat_rgb = np.uint8(255 * heat)
    heat_rgb = np.uint8(255 * heat)
    
    import matplotlib.cm as cm
    cmap = cm.get_cmap(colormap)
    colored = (cmap(heat_rgb)[:,:,:3] * 255).astype(np.uint8)
    colored = Image.fromarray(colored).resize(img.size, Image.BICUBIC)
    
    # Apply blur if specified
    if 'blur_radius' in locals() and blur_radius > 0:
        from PIL import ImageFilter
        colored = colored.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    blend = Image.blend(img.convert("RGB"), colored, alpha=alpha)
    return blend

def create_prediction_chart(top5_idx, top5_val, classes):
    """Create an interactive prediction chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[classes[idx] for idx in top5_idx],
        y=top5_val,
        marker_color='rgba(139, 92, 246, 0.8)',
        text=[f'{val:.3f}' for val in top5_val],
        textposition='auto',
        name='Confidence'
    ))
    
    fig.update_layout(
        title="Top-5 Predictions",
        xaxis_title="Classes",
        yaxis_title="Confidence",
        template="plotly_dark",
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f7fafc')
    )
    
    return fig

# ==================== ENHANCED UPLOAD INTERFACE ====================
st.markdown("### 📸 Image Upload & Analysis")

# Create a more engaging upload area
upload_col1, upload_col2 = st.columns([2, 1])

with upload_col1:
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Upload an image to analyze with AI. Supported formats: JPG, PNG, BMP, TIFF"
    )

with upload_col2:
    st.markdown("""
    <div class="metric-card">
        <h4>💡 Pro Tips</h4>
        <ul style="font-size: 0.9rem; color: var(--text-secondary);">
            <li>Use high-resolution images</li>
            <li>Clear, well-lit subjects work best</li>
            <li>Try different analysis modes</li>
            <li>Ask specific questions for AI analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if not uploaded_file:
    st.markdown("""
    <div class="upload-area">
        <h3>🚀 Ready to Explore AI Vision?</h3>
        <p>Upload an image above to start your analysis journey!</p>
        <p style="font-size: 0.9rem; color: var(--text-secondary);">
            Try uploading a photo with a clear object (dog, car, building, etc.) for best results.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Load the image
original_image = Image.open(uploaded_file).convert("RGB")

# ==================== AI IMAGE ANALYSIS SECTION ====================
if analysis_mode in ["AI Image Analysis", "Both"]:
    st.markdown("### 🤖 AI Image Analysis")
    
    # Validate API key (only for Gemini)
    if ai_model_type == "Gemini" and not validate_api_key(api_key):
        st.error("❌ Please enter a valid API key to use Gemini AI analysis features.")
        if analysis_mode == "AI Image Analysis":
            st.stop()
    else:
        # Question input
        question = st.text_area(
            "❓ Ask a question about the image",
            placeholder="e.g., What do you see in this image? Describe the objects and their relationships.",
            help="Ask any question about the uploaded image. Be specific for better results."
        )
        
        # Helpful tips for better questions
        with st.expander("💡 Tips for Better Questions"):
            st.markdown("""
            **Good questions to try:**
            - "What do you see in this image?"
            - "Describe the main objects in this image"
            - "What colors are prominent in this image?"
            - "What type of scene is this?"
            - "Are there any people or animals in this image?"
            
            **Avoid:**
            - Complex mathematical questions
            - Questions about text or numbers in images
            - Very specific technical questions
            """)
        
        if st.button("🔍 Analyze with AI", type="primary"):
            if not question.strip():
                st.warning("⚠️ Please enter a question to analyze the image.")
            else:
                with st.spinner("🧠 Analyzing image with AI..."):
                    try:
                        # Create AI model instance based on selection
                        if ai_model_type == "Gemini":
                            # Original code: ai_model = AIModelFactory.create_model("gemini", api_key)
                            ai_model = AIModelFactory.create_model("gemini", api_key)
                        else:  # BLIP Local
                            # Original code: ai_model = AIModelFactory.create_model("blip_local")
                            ai_model = AIModelFactory.create_model("blip_local")
                        
                        if ai_model:
                            # Perform analysis
                            # Original code: result = ai_model.analyze_image(original_image, question)
                            result = ai_model.analyze_image(original_image, question)
                            
                            # Display results
                            if result["success"]:
                                st.markdown(f"""
                                <div class="ai-analysis-card success">
                                    <div class="model-badge">{result["model"]}</div>
                                    <h4>🤖 AI Analysis Result</h4>
                                    <p style="font-size: 1.1rem; line-height: 1.6; margin: 1rem 0;">
                                        {result["answer"]}
                                    </p>
                                    <div style="font-size: 0.9rem; color: var(--text-secondary);">
                                        <strong>Question:</strong> {question}<br>
                                        {f'<strong>Response Time:</strong> {result.get("response_time", "Unknown"):.2f}s<br>' if "response_time" in result else ""}
                                        {f'<strong>Tokens Used:</strong> {result.get("tokens_used", "Unknown")}<br>' if "tokens_used" in result else ""}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="ai-analysis-card error">
                                    <div class="model-badge">{result["model"]}</div>
                                    <h4>❌ Analysis Failed</h4>
                                    <p style="color: var(--error-color);">
                                        {result["error"]}
                                    </p>

                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Failed to initialize AI model. Please check your API key and try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error during AI analysis: {str(e)}")

# ==================== GRAD-CAM ANALYSIS SECTION ====================
if analysis_mode in ["Grad-CAM Analysis", "Both"]:
    st.markdown("### 🎯 Grad-CAM Analysis")
    
    # Show loading state
    with st.spinner("🚀 Loading AI model..."):
        model = load_model()
        classes = load_imagenet_labels()
    
    # Register hooks for the selected layer
    target_layer = get_target_layer(model, LAYER_OPTIONS[layer_name])
    for h in getattr(model, "_gc_hooks", []):
        h.remove()
    model._gc_hooks = [
        target_layer.register_forward_hook(hook_forward),
        target_layer.register_full_backward_hook(hook_backward),
    ]
    
    with st.spinner("🔍 Analyzing image with Grad-CAM..."):
        # Load and preprocess image
        input_tensor = preprocess(original_image).unsqueeze(0)
        input_tensor.requires_grad_(True)
        
        # Model inference
        start_time = time.time()
        logits = model(input_tensor)
        inference_time = time.time() - start_time
        
        # Get predictions
        probabilities = F.softmax(logits, dim=1)[0]
        top5_indices = torch.topk(probabilities, k=5).indices.tolist()
        top5_values = torch.topk(probabilities, k=5).values.tolist()

    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⚡ Inference Time", f"{inference_time:.3f}s")
    with col2:
        st.metric("🎯 Top Prediction", f"{top5_values[0]:.3f}")
    with col3:
        st.metric("📊 Confidence Range", f"{top5_values[-1]:.3f} - {top5_values[0]:.3f}")
    with col4:
        st.metric("🔍 Model", model_option.split()[0])

    # Target class selection with better UX
    st.markdown("#### 🎯 Select Target Class for Analysis")
    top_labels = [f"{classes[i]} ({probabilities[i].item():.3f})" for i in top5_indices]
    target_choice = st.selectbox(
        "Choose which class to explain:",
        top_labels,
        index=0,
        help="Select the class you want to understand better. The model will show you what features it used to make this prediction."
    )

    target_idx = top5_indices[top_labels.index(target_choice)]

    # Grad-CAM computation
    with st.spinner("🧠 Computing Grad-CAM visualization..."):
        # Clear gradients and compute Grad-CAM
        model.zero_grad()
        target_score = logits[0, target_idx]
        target_score.backward(retain_graph=True)
        
        # Grad-CAM computation
        activations_tensor = activations["value"]
        gradients_tensor = gradients["value"]
        
        # Global average pooling on gradients
        weights = gradients_tensor.mean(dim=(2, 3), keepdim=True)
        
        # Weighted combination of activations
        cam = (weights * activations_tensor).sum(dim=1, keepdim=True)
        cam = F.relu(cam)
        cam = cam[0, 0].detach().cpu().numpy()
        
        # Normalize to [0, 1]
        if cam.max() > cam.min():
            cam = (cam - cam.min()) / (cam.max() - cam.min())
        else:
            cam = np.zeros_like(cam)

    # Enhanced visualization
    st.markdown("### 🔍 Visual Analysis")

    # Prepare images for display
    display_transform = T.Compose([T.Resize(512), T.CenterCrop(512)])
    display_image = display_transform(original_image)
    cam_image = Image.fromarray(np.uint8(cam * 255)).resize(display_image.size, Image.BICUBIC)
    cam_normalized = np.asarray(cam_image, dtype=np.uint8) / 255.0

    # Create enhanced visualization layout
    viz_col1, viz_col2, viz_col3 = st.columns([1, 1, 1])

    with viz_col1:
        st.markdown("#### 📷 Original Image")
        st.image(display_image, use_container_width=True, caption="Input image")

    with viz_col2:
        st.markdown("#### 🎨 Grad-CAM Heatmap")
        st.image(overlay_heatmap(display_image, cam_normalized, alpha=alpha, colormap=colormap), 
                 use_container_width=True, caption="AI attention visualization")

    with viz_col3:
        st.markdown("#### 🔥 Raw Heatmap")
        st.image(cam_image, use_container_width=True, caption="Raw attention map")

    # Enhanced predictions display
    st.markdown("### 📊 Detailed Predictions")

    # Interactive chart
    prediction_chart = create_prediction_chart(top5_indices, top5_values, classes)
    st.plotly_chart(prediction_chart, use_container_width=True)

    # Detailed predictions table
    st.markdown("#### 📋 Prediction Details")
    for i, (idx, val) in enumerate(zip(top5_indices, top5_values), start=1):
        confidence_bar = val
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0;">{i}. {classes[idx]}</h4>
                    <p style="margin: 0.25rem 0; color: var(--text-secondary);">
                        Confidence: {val:.3f} ({val*100:.1f}%)
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="width: 100px; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                        <div style="width: {confidence_bar*100}%; height: 100%; background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));"></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== SETUP INSTRUCTIONS ====================
with st.expander("🔧 Setup Instructions"):
    st.markdown("""
    ### 🔑 API Setup Instructions
    
    #### For Gemini API:
    1. **Get API Key**: Visit [Google AI Studio](https://aistudio.google.com/)
    2. **Create Project**: Create a new project or select existing one
    3. **Enable API**: Enable the Gemini API for your project
    4. **Generate Key**: Create an API key in the credentials section
    5. **Copy Key**: Copy the API key and paste it in the sidebar
    
    ### 🚀 AWS EC2 Deployment
    
    #### Security Group Configuration:
    - **Inbound Rules**: Allow HTTP (80) and HTTPS (443) for web access
    - **Outbound Rules**: Allow all traffic for API calls
    
    #### Environment Variables:
    Create a `.env` file with your API keys:
    ```
    GEMINI_API_KEY=your_gemini_api_key_here
    ```
    
    #### Installation Commands:
    ```bash
    # Update system
    sudo apt update && sudo apt upgrade -y
    
    # Install Python and pip
    sudo apt install python3 python3-pip -y
    
    # Install dependencies
    pip3 install -r requirements.txt
    
    # Run the application
    streamlit run image_analysis_app.py --server.port 8501 --server.address 0.0.0.0
    ```
    
    #### Access the App:
    - **Local**: http://localhost:8501
    - **Remote**: http://your-ec2-public-ip:8501
    
    ### 📊 Model Information
    
    #### Gemini 1.5 Pro:
    - **Capabilities**: Text, image, video, audio, code
    - **Max Input**: 2M tokens
    - **Pricing**: Pay per use
    - **Best For**: High-quality multimodal analysis
    
    #### BLIP VQA (Local):
    - **Capabilities**: Visual Question Answering
    - **Max Input**: No limit (local processing)
    - **Pricing**: Free (runs locally)
    - **Best For**: Offline VQA, privacy-focused analysis
    - **Setup**: Run `python download_blip_model.py` to download the model locally
    

    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); padding: 2rem;">
    <p>🔍 <strong>AI Vision Explorer</strong> - Making AI Interpretable, One Image at a Time</p>
    <p style="font-size: 0.9rem;">Built with Streamlit, PyTorch, and the latest in Multimodal AI research</p>
</div>
""", unsafe_allow_html=True)
