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

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="🔍 AI Vision Explorer - Grad-CAM Analysis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ai-vision-explorer/issues',
        'Report a bug': 'https://github.com/yourusername/ai-vision-explorer/issues',
        'About': '# AI Vision Explorer\nAdvanced Computer Vision Analysis with Grad-CAM Interpretability'
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
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR CONFIGURATION ====================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h3>🎛️ Analysis Controls</h3>
        <p style="color: var(--text-secondary); font-size: 0.9rem;">
            Configure your Grad-CAM analysis parameters
        </p>
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
    
    # Model info
    st.markdown("""
    <div class="sidebar-section">
        <h4>📊 Model Information</h4>
        <p style="font-size: 0.8rem; color: var(--text-secondary);">
            <strong>Architecture:</strong> ResNet-18<br>
            <strong>Dataset:</strong> ImageNet-1K<br>
            <strong>Parameters:</strong> 11.7M<br>
            <strong>Top-1 Accuracy:</strong> 69.8%
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN HEADER ====================
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🔍 AI Vision Explorer</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
        Advanced Computer Vision Analysis with Grad-CAM Interpretability
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.8;">
        Upload an image → Analyze with AI → Understand what the model sees
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== MODEL SETUP ====================
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

# Show loading state
with st.spinner("🚀 Loading AI model..."):
    model = load_model()

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

# Register hooks for the selected layer
target_layer = get_target_layer(model, LAYER_OPTIONS[layer_name])
for h in getattr(model, "_gc_hooks", []):
    h.remove()
model._gc_hooks = [
    target_layer.register_forward_hook(hook_forward),
    target_layer.register_full_backward_hook(hook_backward),
]

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

classes = load_imagenet_labels()

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
            <li>Try different layers for insights</li>
            <li>Adjust opacity for better visualization</li>
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

# ==================== IMAGE PROCESSING & ANALYSIS ====================
with st.spinner("🔍 Analyzing image with AI..."):
    # Load and preprocess image
    original_image = Image.open(uploaded_file).convert("RGB")
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

# ==================== ENHANCED RESULTS DISPLAY ====================
st.markdown("### 🎯 Analysis Results")

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

# ==================== GRAD-CAM COMPUTATION ====================
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

# ==================== ENHANCED VISUALIZATION ====================
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

# ==================== ENHANCED PREDICTIONS DISPLAY ====================
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

# ==================== TECHNICAL DETAILS ====================
with st.expander("🔬 Technical Details & Methodology"):
    st.markdown("""
    ### How Grad-CAM Works
    
    **Grad-CAM (Gradient-weighted Class Activation Mapping)** is a technique that provides visual explanations for decisions made by Convolutional Neural Networks (CNNs).
    
    #### The Process:
    1. **Forward Pass**: The image is processed through the network to get class predictions
    2. **Gradient Computation**: Gradients are computed with respect to the target class score
    3. **Feature Map Weighting**: Gradients are globally average pooled to get importance weights
    4. **Activation Combination**: Weights are combined with the feature maps from the target layer
    5. **Visualization**: The resulting attention map is upsampled and overlaid on the original image
    
    #### Mathematical Formula:
    ```
    Grad-CAM = ReLU(Σ(w_k * A_k))
    ```
    Where:
    - `w_k` = global average pooled gradients for channel k
    - `A_k` = activation map for channel k
    - `ReLU` = ensures only positive contributions are shown
    
    #### Why This Matters:
    - **Interpretability**: Understand what the AI "sees" when making decisions
    - **Debugging**: Identify potential biases or errors in the model
    - **Trust**: Build confidence in AI systems by making them explainable
    - **Research**: Advance the field of explainable AI
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); padding: 2rem;">
    <p>🔍 <strong>AI Vision Explorer</strong> - Making AI Interpretable, One Image at a Time</p>
    <p style="font-size: 0.9rem;">Built with Streamlit, PyTorch, and the latest in Computer Vision research</p>
</div>
""", unsafe_allow_html=True)
