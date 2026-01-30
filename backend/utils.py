"""
Utilities Module - Helper Functions & Pipeline Orchestration
"""

import os
from typing import Dict, Optional
from PIL import Image
import io
from dotenv import load_dotenv

# Load .env file on module import
load_dotenv()


def load_image_from_path(image_path: str) -> Optional[Image.Image]:
    """
    Load image from file path
    
    Args:
        image_path: Path to image file
        
    Returns:
        PIL Image object or None if failed
    """
    try:
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return None
        
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        return None


def load_image_from_bytes(image_bytes: bytes) -> Optional[Image.Image]:
    """
    Load image from bytes (e.g., from Streamlit camera input)
    
    Args:
        image_bytes: Image data as bytes
        
    Returns:
        PIL Image object or None if failed
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        print(f"Error loading image from bytes: {str(e)}")
        return None


def run_complete_analysis(image: Image.Image, api_key: Optional[str] = None) -> Dict:
    """
    Run complete analysis pipeline on an image
    
    This is the main orchestration function that:
    1. Analyzes image with vision model
    2. Performs LLM-based reasoning
    3. Calculates scores and formats output
    
    Args:
        image: PIL Image object
        api_key: Optional API key
        
    Returns:
        Complete analysis dictionary
    """
    from backend.vision import analyze_waste_object, validate_image
    from backend.reasoning import analyze_reuse_potential
    from backend.scoring import format_final_output
    
    # Validate image
    if not validate_image(image):
        return {
            "status": "error",
            "error": "Invalid image: Image too small or corrupted",
            "object_type": "Unknown",
            "score": 0,
            "verdict": "Analysis Failed"
        }
    
    # Step 1: Vision analysis
    print("Step 1: Analyzing image with vision AI...")
    vision_result = analyze_waste_object(image, api_key)
    
    if vision_result["status"] != "success":
        return {
            "status": "error",
            "error": vision_result["description"],
            "object_type": "Unknown",
            "score": 0,
            "verdict": "Analysis Failed"
        }
    
    print(f"✓ Vision analysis complete. Detected: {vision_result['object_type']}")
    
    # Step 2: LLM reasoning
    print("Step 2: Performing reuse analysis with LLM...")
    analysis = analyze_reuse_potential(
        vision_result["description"],
        vision_result["object_type"],
        api_key
    )
    
    print(f"✓ Analysis complete. Verdict: {analysis['verdict']}")
    
    # Step 3: Format output
    final_output = format_final_output(vision_result, analysis)
    final_output["status"] = "success"
    
    return final_output


def check_api_key() -> bool:
    """
    Check if Ollama service is available
    
    Returns:
        True if Ollama is running
    """
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_setup_instructions() -> str:
    """
    Get setup instructions for Ollama
    
    Returns:
        Instruction string
    """
    return """
OLLAMA SETUP REQUIRED
====================

This application requires Ollama (local LLM service).

Steps to install and run:
1. Download from: https://ollama.ai
2. Install and run Ollama:
   ollama serve

3. In another terminal, pull required models:
   ollama pull llava      (for image analysis)
   ollama pull mistral    (for text reasoning)

4. Ollama will run on http://localhost:11434

That's it! No API keys needed, everything runs locally.
"""


def print_analysis_summary(result: Dict):
    """
    Print formatted analysis summary to console
    
    Args:
        result: Analysis result dictionary
    """
    from backend.scoring import generate_summary_report
    
    if result.get("status") == "error":
        print("\n❌ ANALYSIS FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")
        return
    
    print("\n" + generate_summary_report(result))


def validate_environment() -> Dict[str, bool]:
    """
    Validate that all required dependencies are available
    
    Returns:
        Dictionary of validation checks
    """
    checks = {
        "PIL": False,
        "requests": False,
        "streamlit": False,
        "ollama": False
    }
    
    # Check PIL
    try:
        import PIL
        checks["PIL"] = True
    except ImportError:
        pass
    
    # Check requests
    try:
        import requests
        checks["requests"] = True
    except ImportError:
        pass
    
    # Check streamlit
    try:
        import streamlit
        checks["streamlit"] = True
    except ImportError:
        pass
    
    # Check Ollama service
    checks["ollama"] = check_api_key()
    
    return checks