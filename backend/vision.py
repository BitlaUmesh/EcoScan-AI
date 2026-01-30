#Image understanding (object type + condition)

"""
Vision Module - AI-Powered Image Understanding
Uses Google Gemini Vision API to analyze waste object images
"""

import os
from typing import Dict, Optional
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import time

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
    Analyze waste object image using Google Gemini Vision API
    
    Describes material type, condition, damage, contamination, and physical state.
    
    Args:
        image: PIL Image object of the waste item
        api_key: Optional Gemini API key (uses GEMINI_API_KEY env var if not provided)
        
    Returns:
        Dictionary containing:
            - description: Detailed natural language description
            - object_type: Identified material category
            - status: Success/error status
    """
    try:
        import google.generativeai as genai
        
        # Get API key
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return {
                "status": "error",
                "description": "GEMINI_API_KEY not found in environment variables",
                "object_type": "unknown"
            }
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
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
        
        # Call Gemini with vision capability with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content([prompt, image])
                break
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise e
        
        description = response.text.strip()
        
        # Extract object type
        object_type = extract_object_type(description)
        
        return {
            "status": "success",
            "description": description,
            "object_type": object_type
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