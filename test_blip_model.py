#!/usr/bin/env python3
"""
BLIP Model Test Script
Tests the local BLIP VQA model with a sample image
"""

import os
import sys
from PIL import Image
import numpy as np
from ai_models import AIModelFactory

def create_test_image():
    """Create a simple test image"""
    # Create a simple colored square as a test image
    img_array = np.zeros((224, 224, 3), dtype=np.uint8)
    img_array[50:174, 50:174] = [255, 0, 0]  # Red square
    img_array[100:124, 100:124] = [0, 255, 0]  # Green square inside
    return Image.fromarray(img_array)

def test_blip_model():
    """Test the BLIP model with a sample image and question"""
    
    print("🧪 Testing BLIP Local Model")
    print("=" * 40)
    
    try:
        # Create AI model instance
        print("Loading BLIP model...")
        ai_model = AIModelFactory.create_model("blip_local")
        
        if not ai_model:
            print("❌ Failed to create BLIP model")
            return False
        
        # Create test image
        print("Creating test image...")
        test_image = create_test_image()
        
        # Test question
        test_question = "What colors do you see in this image?"
        
        print(f"Question: {test_question}")
        print("Analyzing image...")
        
        # Perform analysis
        result = ai_model.analyze_image(test_image, test_question)
        
        if result["success"]:
            print("✅ Test successful!")
            print(f"Answer: {result['answer']}")
            print(f"Model: {result['model']}")
            print(f"Response time: {result.get('response_time', 'Unknown'):.2f}s")
            print(f"Device: {result.get('device', 'Unknown')}")
            return True
        else:
            print("❌ Test failed!")
            print(f"Error: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔍 BLIP Model Tester")
    print("=" * 50)
    
    # Check if model exists
    model_path = "./models/Salesforce/blip-vqa-base"
    if not os.path.exists(model_path):
        print(f"❌ BLIP model not found at: {model_path}")
        print("Please run 'python download_blip_model.py' first to download the model.")
        sys.exit(1)
    
    # Run test
    success = test_blip_model()
    
    if success:
        print("\n🎉 BLIP model is working correctly!")
        print("You can now use it in the AI Vision Explorer app.")
    else:
        print("\n❌ BLIP model test failed.")
        print("Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

