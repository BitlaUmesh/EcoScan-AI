#Image understanding (object type + condition)

"""
Vision Module - AI-Powered Image Understanding
Uses pretrained vision models to analyze waste object images
"""

import os
from typing import Dict, Optional
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load .env file on module import
load_dotenv()


def encode_image_to_base64(image: Image.Image) -> str:
    """
    Convert PIL Image to base64 string for API transmission
    
    Args:
        image: PIL Image object
        
    Returns:
        Base64 encoded string
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def analyze_waste_object(image: Image.Image, api_key: Optional[str] = None) -> Dict[str, str]:
    """
    Analyze waste object image using vision AI
    
    Uses Google Gemini Vision API (free tier) for object analysis.
    Describes material type, condition, damage, contamination, and physical state.
    
    Args:
        image: PIL Image object of the waste item
        api_key: Optional Gemini API key (uses env var if not provided)
        
    Returns:
        Dictionary containing:
            - description: Detailed natural language description
            - object_type: Identified material category
            - status: Success/error status
    """
    try:
        import requests
        
        # Check Ollama service
        try:
            requests.get("http://localhost:11434/api/tags", timeout=2)
        except:
            return {
                "status": "error",
                "description": "Ollama service not running. Please start Ollama: ollama serve",
                "object_type": "unknown"
            }
        
        # Craft detailed prompt for waste object analysis
        prompt = """You are an expert material analyst examining a waste object for reuse potential.

Analyze this image and provide a DETAILED description including:

1. **Object Type**: What is this item? (plastic container, metal can, cardboard box, fabric, glass, etc.)
2. **Material Condition**: Describe the surface quality, visible wear, scratches, dents, or deformations
3. **Structural Integrity**: Does it appear intact, cracked, broken, or structurally compromised?
4. **Contamination**: Any visible dirt, stains, rust, mold, food residue, or other contamination?
5. **Color & Texture**: Note any fading, discoloration, or texture degradation
6. **Physical Damage**: Cracks, holes, tears, warping, or other damage
7. **Overall State**: Clean/dirty, old/new, functional/damaged

Be specific and observational. Focus on what you can SEE in the image.
Write in a clear, professional tone as if documenting for a sustainability assessment.

Format your response as a single detailed paragraph."""
        
        # Encode image to base64
        image_b64 = encode_image_to_base64(image)
        
        # Call Ollama with vision model
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": prompt,
                "images": [image_b64],
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code != 200:
            return {
                "status": "error",
                "description": f"Ollama error: {response.text}",
                "object_type": "unknown"
            }
        
        description = response.json().get("response", "").strip()
        
        # Extract object type (simple keyword detection)
        object_type = extract_object_type(description)
        
        return {
            "status": "success",
            "description": description,
            "object_type": object_type
        }
        
    except ImportError:
        return {
            "status": "error",
            "description": "Google Generative AI library not installed. Run: pip install google-generativeai",
            "object_type": "unknown"
        }
    except Exception as e:
        return {
            "status": "error",
            "description": f"Vision analysis failed: {str(e)}",
            "object_type": "unknown"
        }


def extract_object_type(description: str) -> str:
    """
    Extract object type from vision description using keyword matching
    
    Args:
        description: Vision model output text
        
    Returns:
        Identified material category
    """
    description_lower = description.lower()
    
    # Material type keywords (ordered by specificity)
    material_map = {
        "plastic bottle": ["plastic bottle", "pet bottle", "water bottle"],
        "plastic container": ["plastic container", "plastic box", "tupperware"],
        "plastic": ["plastic", "polymer"],
        "glass bottle": ["glass bottle", "wine bottle", "beer bottle"],
        "glass jar": ["glass jar", "mason jar"],
        "glass": ["glass"],
        "metal can": ["metal can", "aluminum can", "tin can", "soda can"],
        "metal container": ["metal container", "metal box"],
        "metal": ["metal", "aluminum", "steel", "iron"],
        "cardboard box": ["cardboard box", "carton box"],
        "cardboard": ["cardboard", "corrugated"],
        "paper": ["paper", "newspaper"],
        "fabric": ["fabric", "cloth", "textile", "clothing"],
        "wood": ["wood", "wooden"],
        "rubber": ["rubber", "tire"],
        "electronics": ["electronic", "device", "circuit"],
    }
    
    # Check in order of specificity
    for material_type, keywords in material_map.items():
        for keyword in keywords:
            if keyword in description_lower:
                return material_type
    
    return "unidentified object"


def validate_image(image: Image.Image) -> bool:
    """
    Validate that image is suitable for analysis
    
    Args:
        image: PIL Image object
        
    Returns:
        True if valid, False otherwise
    """
    if image is None:
        return False
    
    # Check minimum dimensions
    width, height = image.size
    if width < 100 or height < 100:
        return False
    
    return True