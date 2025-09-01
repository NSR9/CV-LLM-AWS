#!/usr/bin/env python3
"""
BLIP VQA Demo Script
Demonstrates Visual Question Answering using the local BLIP model
Based on Lesson 12: Visual Question & Answering
"""

import os
import sys
from PIL import Image
import torch
from transformers import BlipForQuestionAnswering, AutoProcessor
import warnings

# Suppress warnings for better user experience
warnings.filterwarnings("ignore", message="Using the model-agnostic default `max_length`")
from transformers.utils import logging as transformers_logging
transformers_logging.set_verbosity_error()

def load_blip_model():
    """Load the BLIP model and processor"""
    print("Loading BLIP model...")
    
    # Check if local model exists
    local_path = "./models/Salesforce/blip-vqa-base"
    if os.path.exists(local_path):
        print(f"Using local model from: {local_path}")
        model_path = local_path
    else:
        print("Local model not found, downloading from Hugging Face...")
        model_path = "Salesforce/blip-vqa-base"
    
    # Load model and processor
    model = BlipForQuestionAnswering.from_pretrained(model_path)
    processor = AutoProcessor.from_pretrained(model_path)
    
    # Set model to evaluation mode
    model.eval()
    
    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    print(f"Model loaded successfully on {device}")
    return model, processor, device

def analyze_image_with_question(model, processor, device, image_path, question):
    """Analyze image with a question using BLIP"""
    
    # Load image
    if os.path.exists(image_path):
        image = Image.open(image_path)
        print(f"Loaded image: {image_path}")
    else:
        print(f"Image not found: {image_path}")
        print("Creating a sample image for demonstration...")
        # Create a simple test image
        import numpy as np
        img_array = np.zeros((224, 224, 3), dtype=np.uint8)
        img_array[50:174, 50:174] = [255, 0, 0]  # Red square
        img_array[100:124, 100:124] = [0, 255, 0]  # Green square inside
        image = Image.fromarray(img_array)
    
    # Process inputs
    inputs = processor(image, question, return_tensors="pt")
    
    # Move inputs to device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Generate answer
    with torch.no_grad():
        out = model.generate(**inputs)
    
    # Decode the answer
    answer = processor.decode(out[0], skip_special_tokens=True)
    
    return answer

def main():
    """Main demo function"""
    print("🔍 BLIP VQA Demo - Lesson 12: Visual Question & Answering")
    print("=" * 60)
    
    try:
        # Load model
        model, processor, device = load_blip_model()
        
        # Demo questions and image
        image_path = "./beach.jpeg"  # From the lesson example
        questions = [
            "how many dogs are in the picture?",
            "What do you see in this image?",
            "What colors are prominent in this image?",
            "Describe the scene in this image"
        ]
        
        print(f"\n📸 Image: {image_path}")
        print("❓ Questions to analyze:")
        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q}")
        
        print("\n" + "="*60)
        
        # Analyze each question
        for i, question in enumerate(questions, 1):
            print(f"\n🔍 Question {i}: {question}")
            print("-" * 40)
            
            answer = analyze_image_with_question(model, processor, device, image_path, question)
            print(f"🤖 Answer: {answer}")
        
        print("\n" + "="*60)
        print("✅ Demo completed successfully!")
        print("\n💡 Tips:")
        print("- Try different types of questions")
        print("- Use specific questions for better results")
        print("- The model works best with clear, well-lit images")
        print("- You can now use this in the AI Vision Explorer app!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have the required dependencies:")
        print("   pip install transformers torch pillow")
        print("2. Download the model first:")
        print("   python download_blip_model.py")
        print("3. Check that the image file exists")
        sys.exit(1)

if __name__ == "__main__":
    main()
