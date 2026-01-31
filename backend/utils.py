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
    Load image from bytes (e.g., from web camera input)
    
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


def run_complete_analysis(image: Image.Image, api_key: Optional[str] = None) -> tuple:
    """
    Run complete analysis pipeline on an image
    
    This is the main orchestration function that:
    1. Analyzes image with vision model
    2. Performs LLM-based reasoning
    3. Calculates scores and formats output
    4. Generates pricing for recycled product
    
    Args:
        image: PIL Image object
        api_key: Optional API key
        
    Returns:
        Tuple containing (vision_result, analysis_result, final_output)
    """
    from backend.vision import analyze_waste_object, validate_image
    from backend.reasoning import analyze_reuse_potential
    from backend.scoring import format_final_output
    from backend.transformation_engine import calculate_market_price
    
    # Validate image
    if not validate_image(image):
        return None, None, {
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
        return vision_result, None, {
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
    
    # Step 4: Calculate pricing for primary suggestion if available
    try:
        if analysis.get("suggestions") and len(analysis["suggestions"]) > 0:
            primary_suggestion = analysis["suggestions"][0]
            target_product = primary_suggestion.get("title", primary_suggestion.get("use_case", "recycled product"))
            
            # Create a simple quality assessment from available data
            quality_assessment = {
                "expected_lifespan_months": 12,
                "structural_integrity": analysis.get("condition_summary", "good")
            }
            
            # Create a simple procedure from suggestion
            procedure = {
                "difficulty_level": primary_suggestion.get("difficulty", "Medium"),
                "estimated_time_minutes": parse_time_to_minutes(primary_suggestion.get("time_required", "30 mins"))
            }
            
            print("\nStep 3: Calculating market price for recycled product...")
            pricing = calculate_market_price(
                target_product,
                quality_assessment,
                procedure,
                vision_result["object_type"]
            )
            
            final_output["pricing"] = pricing
            print(f"✓ Price range: ₹{pricing['suggested_price_range']['min']}-₹{pricing['suggested_price_range']['max']}")
    except Exception as e:
        print(f"⚠ Pricing calculation skipped: {str(e)}")
    
    return vision_result, analysis, final_output


def parse_time_to_minutes(time_str: str) -> int:
    """
    Parse time string like '30 mins' or '1 hour' to minutes
    
    Args:
        time_str: Time string
        
    Returns:
        Time in minutes
    """
    import re
    time_str = time_str.lower()
    
    # Extract numbers
    numbers = re.findall(r'\d+', time_str)
    if not numbers:
        return 30  # default
    
    value = int(numbers[0])
    
    if 'hour' in time_str:
        return value * 60
    elif 'min' in time_str:
        return value
    else:
        return value


def check_api_key() -> bool:
    """
    Check if Gemini API key is configured
    
    Returns:
        True if GEMINI_API_KEY is set in environment
    """
    api_key = os.getenv("GEMINI_API_KEY")
    return api_key is not None and len(api_key) > 0


def get_setup_instructions() -> str:
    """
    Get setup instructions for Gemini API
    
    Returns:
        Instruction string
    """
    return """
GEMINI API SETUP REQUIRED
===========================

This application requires a Google Gemini API key.

Steps to set up:
1. Get your free API key from: https://aistudio.google.com/app/apikey
2. Create or edit a .env file in the EcoScan-AI folder with:
   
   GEMINI_API_KEY=your_api_key_here

3. Restart the application

That's it! The app will use Google's cloud-based Gemini API.
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
        "flask": False,
        "google-generativeai": False,
        "gemini_api_key": False
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
    
    # Check flask
    try:
        import flask
        checks["flask"] = True
    except ImportError:
        pass
    
    # Check google-generativeai
    try:
        import google.generativeai
        checks["google-generativeai"] = True
    except ImportError:
        pass
    
    # Check Gemini API key
    checks["gemini_api_key"] = check_api_key()
    
    return checks