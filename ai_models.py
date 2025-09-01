"""
AI Models Integration Module
Handles Gemini API for multimodal image analysis and local BLIP model for VQA
"""

import os
import base64
import io
import requests
import google.generativeai as genai
from PIL import Image
import streamlit as st
from typing import Optional, Dict, Any
import json
import logging
import time
import torch
from transformers import BlipForQuestionAnswering, AutoProcessor
import warnings

# Suppress warnings for better user experience
warnings.filterwarnings("ignore", message="Using the model-agnostic default `max_length`")
from transformers.utils import logging as transformers_logging
transformers_logging.set_verbosity_error()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== LOCAL BLIP MODEL FOR VQA ====================
class BLIPLocalModel:
    """Handles local BLIP model for Visual Question Answering"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize BLIP model locally
        
        Args:
            model_path (str): Path to local model directory (optional)
        """
        # Original code: self.model_path = model_path or "./models/Salesforce/blip-vqa-base"
        self.model_path = model_path or "./models/Salesforce/blip-vqa-base"
        
        try:
            # Load model and processor
            # Original code: self.model = BlipForQuestionAnswering.from_pretrained(self.model_path)
            self.model = BlipForQuestionAnswering.from_pretrained(self.model_path)
            # Original code: self.processor = AutoProcessor.from_pretrained(self.model_path)
            self.processor = AutoProcessor.from_pretrained(self.model_path)
            
            # Set model to evaluation mode
            # Original code: self.model.eval()
            self.model.eval()
            
            # Move to GPU if available
            # Original code: self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            # Original code: self.model.to(self.device)
            self.model.to(self.device)
            
            logger.info(f"BLIP model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load BLIP model: {str(e)}")
            raise Exception(f"Failed to load BLIP model: {str(e)}")
    
    def analyze_image(self, image: Image.Image, question: str) -> Dict[str, Any]:
        """
        Analyze image with a question using local BLIP model
        
        Args:
            image (Image.Image): PIL image to analyze
            question (str): Question about the image
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            start_time = time.time()
            
            # Process inputs
            # Original code: inputs = self.processor(image, question, return_tensors="pt")
            inputs = self.processor(image, question, return_tensors="pt")
            
            # Move inputs to device
            # Original code: inputs = {k: v.to(self.device) for k, v in inputs.items()}
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate answer
            # Original code: with torch.no_grad():
            with torch.no_grad():
                # Original code: out = self.model.generate(**inputs)
                out = self.model.generate(**inputs)
            
            # Decode the answer
            # Original code: answer = self.processor.decode(out[0], skip_special_tokens=True)
            answer = self.processor.decode(out[0], skip_special_tokens=True)
            
            response_time = time.time() - start_time
            
            return {
                "success": True,
                "answer": answer,
                "model": "BLIP VQA (Local)",
                "response_time": response_time,
                "device": str(self.device)
            }
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"BLIP analysis failed: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "model": "BLIP VQA (Local)"
            }

# ==================== GEMINI API INTEGRATION ====================
class GeminiModel:
    """Handles interactions with Google's Gemini API for multimodal analysis"""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini model with API key
        
        Args:
            api_key (str): Google AI Studio API key
        """
        # Original code: self.api_key = api_key
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize the model - using Gemini 1.5 Pro for multimodal capabilities
        # Original code: self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def analyze_image(self, image: Image.Image, question: str) -> Dict[str, Any]:
        """
        Analyze image with a question using Gemini
        
        Args:
            image (Image.Image): PIL image to analyze
            question (str): Question about the image
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            # Original code: response = self.model.generate_content([question, image])
            response = self.model.generate_content([question, image])
            
            if response.text:
                # Safely extract usage metadata
                tokens_used = 'Unknown'
                try:
                    if hasattr(response, 'usage_metadata') and response.usage_metadata:
                        tokens_used = getattr(response.usage_metadata, 'total_token_count', 'Unknown')
                except:
                    tokens_used = 'Unknown'
                
                return {
                    "success": True,
                    "answer": response.text,
                    "model": "Gemini 1.5 Pro",
                    "tokens_used": tokens_used
                }
            else:
                return {
                    "success": False,
                    "error": "No response generated",
                    "model": "Gemini 1.5 Pro"
                }
                
        except Exception as e:
            error_msg = str(e)
            
            # Handle specific Gemini API errors
            if "429" in error_msg:
                error_msg = "Rate limit exceeded. Please try again later."
            elif "quota" in error_msg.lower():
                error_msg = "API quota exceeded. Consider upgrading your plan."
            elif "Unknown field" in error_msg:
                error_msg = "API response format issue. Please try again."
            
            return {
                "success": False,
                "error": error_msg,
                "model": "Gemini 1.5 Pro"
            }

# ==================== MODEL FACTORY ====================
class AIModelFactory:
    """Factory class to create and manage AI models"""
    
    @staticmethod
    def create_model(model_type: str, api_key: str = None, **kwargs) -> Optional[Any]:
        """
        Create an AI model instance based on type
        
        Args:
            model_type (str): Type of model ('gemini', 'blip_local')
            api_key (str): API key for the model (not needed for local models)
            **kwargs: Additional arguments for model initialization
            
        Returns:
            Optional[Any]: Model instance or None if creation fails
        """
        try:
            if model_type.lower() == "gemini":
                # Original code: return GeminiModel(api_key)
                return GeminiModel(api_key)
            elif model_type.lower() == "blip_local":
                # Original code: return BLIPLocalModel(**kwargs)
                return BLIPLocalModel(**kwargs)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
        except Exception as e:
            logger.error(f"Failed to create model: {str(e)}")
            st.error(f"Failed to create model: {str(e)}")
            return None

# ==================== UTILITY FUNCTIONS ====================
def validate_api_key(api_key: str) -> bool:
    """
    Basic validation for API keys
    
    Args:
        api_key (str): API key to validate
        
    Returns:
        bool: True if key appears valid
    """
    # Original code: return api_key and len(api_key) > 10
    return api_key and len(api_key) > 10

def get_model_info(model_type: str) -> Dict[str, str]:
    """
    Get information about supported models
    
    Args:
        model_type (str): Type of model ('gemini', 'blip_local')
        
    Returns:
        Dict[str, str]: Model information
    """
    if model_type.lower() == "gemini":
        return {
            "name": "Gemini 1.5 Pro",
            "description": "Google's most capable multimodal model",
            "capabilities": "Text, image, video, audio, code",
            "max_input": "2M tokens",
            "pricing": "Pay per use"
        }
    elif model_type.lower() == "blip_local":
        return {
            "name": "BLIP VQA (Local)",
            "description": "Local Visual Question Answering model",
            "capabilities": "Image understanding and question answering",
            "max_input": "No limit (local processing)",
            "pricing": "Free (runs locally)"
        }
    else:
        return {}
