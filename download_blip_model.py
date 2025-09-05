#!/usr/bin/env python3
"""
BLIP Model Download Script
Downloads the BLIP VQA model locally for offline use
"""

import os
import sys
from transformers import BlipForQuestionAnswering, AutoProcessor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_blip_model():
    """Download BLIP VQA model to local directory"""
    
    # Model path
    model_path = "./models/Salesforce/blip-vqa-base"
    
    try:
        logger.info("Starting BLIP model download...")
        logger.info(f"Model will be saved to: {model_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(model_path, exist_ok=True)
        
        # Download model and processor
        logger.info("Downloading BLIP model...")
        # Original code: model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        
        logger.info("Downloading BLIP processor...")
        # Original code: processor = AutoProcessor.from_pretrained("Salesforce/blip-vqa-base")
        processor = AutoProcessor.from_pretrained("Salesforce/blip-vqa-base")
        
        # Save model and processor locally
        logger.info("Saving model to local directory...")
        # Original code: model.save_pretrained(model_path)
        model.save_pretrained(model_path)
        # Original code: processor.save_pretrained(model_path)
        processor.save_pretrained(model_path)
        
        logger.info("✅ BLIP model downloaded successfully!")
        logger.info(f"Model saved to: {os.path.abspath(model_path)}")
        
        # Print model info
        logger.info("\nModel Information:")
        logger.info(f"- Model type: BLIP VQA")
        logger.info(f"- Model size: {sum(p.numel() for p in model.parameters()):,} parameters")
        logger.info(f"- Local path: {model_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to download BLIP model: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔍 BLIP Model Downloader")
    print("=" * 50)
    
    # Check if model already exists
    model_path = "./models/Salesforce/blip-vqa-base"
    if os.path.exists(model_path):
        print(f"⚠️  Model already exists at: {model_path}")
        response = input("Do you want to re-download? (y/N): ").strip().lower()
        if response != 'y':
            print("Download cancelled.")
            return
    
    # Download model
    success = download_blip_model()
    
    if success:
        print("\n🎉 Setup complete!")
        print("You can now use the 'BLIP Local' option in the AI Vision Explorer app.")
        print("\nUsage:")
        print("1. Run the app: streamlit run image_analysis_app.py")
        print("2. Select 'BLIP Local' from the AI Model dropdown")
        print("3. Upload an image and ask questions!")
    else:
        print("\n❌ Setup failed. Please check your internet connection and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

