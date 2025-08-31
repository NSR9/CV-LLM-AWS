"""
AI Models Integration Module
Handles Gemini API and Hugging Face Gemma models for multimodal image analysis
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
                error_msg = "Rate limit exceeded. Please try again later or switch to Gemma models (free, no limits)."
            elif "quota" in error_msg.lower():
                error_msg = "API quota exceeded. Consider upgrading your plan or using Gemma models (free)."
            elif "Unknown field" in error_msg:
                error_msg = "API response format issue. Please try again or switch to Gemma models."
            
            return {
                "success": False,
                "error": error_msg,
                "model": "Gemini 1.5 Pro"
            }

# ==================== HUGGING FACE GEMMA INTEGRATION ====================
class GemmaModel:
    """Handles interactions with Hugging Face Gemma models for multimodal analysis"""
    
    def __init__(self, api_key: str, model_name: str = "llava-hf/llava-1.5-7b-hf"):
        """
        Initialize Gemma model with API key and model name
        
        Args:
            api_key (str): Hugging Face API key
            model_name (str): Model name on Hugging Face (default: gemma-2-9b-it for multimodal)
        """
        # Original code: self.api_key = api_key
        self.api_key = api_key
        # Original code: self.model_name = model_name
        self.model_name = model_name
        # Original code: self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        # Original code: self.headers = {"Authorization": f"Bearer {api_key}"}
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def _encode_image(self, image: Image.Image) -> str:
        """
        Encode PIL image to base64 string
        
        Args:
            image (Image.Image): PIL image to encode
            
        Returns:
            str: Base64 encoded image
        """
        # Original code: buffer = io.BytesIO()
        buffer = io.BytesIO()
        # Original code: image.save(buffer, format="JPEG")
        image.save(buffer, format="JPEG")
        # Original code: img_str = base64.b64encode(buffer.getvalue()).decode()
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
    
    def analyze_image(self, image: Image.Image, question: str) -> Dict[str, Any]:
        """
        Analyze image with a question using Gemma
        
        Args:
            image (Image.Image): PIL image to analyze
            question (str): Question about the image
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            # Encode image to base64
            # Original code: img_base64 = self._encode_image(image)
            img_base64 = self._encode_image(image)
            
            # Prepare the payload for multimodal input
            # Original code: payload = {
            payload = {
                "inputs": {
                    "text": question,
                    "image": img_base64
                }
            }
            
            # Make API request
            # Original code: response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "answer": result.get("generated_text", "No text generated"),
                    "model": self.model_name,
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}",
                    "model": self.model_name
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model_name
            }

# ==================== MODEL FACTORY ====================
class AIModelFactory:
    """Factory class to create and manage AI models"""
    
    @staticmethod
    def create_model(model_type: str, api_key: str, **kwargs) -> Optional[Any]:
        """
        Create an AI model instance based on type
        
        Args:
            model_type (str): Type of model ('gemini' or 'gemma')
            api_key (str): API key for the model
            **kwargs: Additional arguments for model initialization
            
        Returns:
            Optional[Any]: Model instance or None if creation fails
        """
        try:
            if model_type.lower() == "gemini":
                # Original code: return GeminiModel(api_key)
                return GeminiModel(api_key)
            elif model_type.lower() == "gemma":
                # Original code: model_name = kwargs.get('model_name', 'google/gemma-2-9b-it')
                model_name = kwargs.get('model_name', 'google/gemma-2-9b-it')
                # Original code: return GemmaModel(api_key, model_name)
                return GemmaModel(api_key, model_name)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
        except Exception as e:
            st.error(f"Failed to create model: {str(e)}")
            return None

# ==================== SUPPORTED MODELS CONFIGURATION ====================
SUPPORTED_GEMMA_MODELS = {
    "LLaVA 1.5 7B": "llava-hf/llava-1.5-7b-hf",  # Multimodal, instruction-tuned
    "LLaVA 1.6 Mistral 7B": "llava-hf/llava-1.6-mistral-7b-hf",  # Enhanced multimodal
    "LLaVA v1.5 7B": "liuhaotian/llava-v1.5-7b",  # Original LLaVA model
}

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
        model_type (str): Type of model ('gemini' or 'gemma')
        
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
    elif model_type.lower() == "gemma":
        return {
            "name": "LLaVA Models",
            "description": "Open multimodal models for vision and language",
            "capabilities": "Text and image understanding",
            "max_input": "Varies by model size",
            "pricing": "Free via Hugging Face"
        }
    else:
        return {}
