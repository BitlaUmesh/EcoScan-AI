#LLM-based reuse analysis

"""
Reasoning Module - LLM-Based Condition Analysis & Reuse Intelligence
Performs higher-level reasoning on vision outputs to determine reusability
Uses Google Gemini API for analysis
"""

import os
from typing import Dict, List, Optional
import json
import re
from dotenv import load_dotenv
import time

# Load .env file on module import
load_dotenv()


def analyze_reuse_potential(
    vision_description: str,
    object_type: str,
    api_key: Optional[str] = None
) -> Dict:
    """
    Use Google Gemini API to analyze reuse potential based on vision description
    
    Args:
        vision_description: Detailed description from vision model
        object_type: Type of object identified
        api_key: Optional Gemini API key (uses GEMINI_API_KEY env var if not provided)
        
    Returns:
        Dictionary containing:
            - reuse_feasible: bool
            - confidence: float (0-100)
            - condition_summary: str
            - reasoning: str
            - suggestions: List[Dict]
            - verdict: str (Reusable/Conditionally Reusable/Not Reusable)
    """
    try:
        import google.generativeai as genai
        
        # Get API key
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return generate_error_response("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Construct reasoning prompt
        prompt = f"""You are a material sustainability analyst evaluating waste objects for reuse potential.

OBJECT INFORMATION:
Type: {object_type}

VISUAL INSPECTION REPORT:
{vision_description}

YOUR TASK:
Based on the visual inspection, analyze whether this object can be safely and practically reused.

Consider:
1. **Structural Integrity**: Is it intact enough for reuse?
2. **Safety**: Any hazards (sharp edges, toxic residue, breakage risk)?
3. **Cleanliness**: Can contamination be cleaned, or is it permanent?
4. **Functionality**: Can it still serve a useful purpose?
5. **Practical Viability**: Would someone realistically reuse this?

Provide your analysis in the following JSON format:

{{
  "reuse_feasible": true/false,
  "confidence": 0-100,
  "verdict": "Reusable" OR "Conditionally Reusable" OR "Not Reusable",
  "condition_summary": "One sentence summary of overall condition",
  "reasoning": "Clear explanation of why it is/isn't reusable based on observed condition",
  "safety_score": 0-100 (Assessment of handling safety),
  "recyclability": true/false,
  "material_composition": ["material1", "material2"],
  "estimated_co2_saved_kg": 0.0 (float estimate),
  "suggestions": [
    {{
      "id": "unique_id",
      "title": "Short title of reuse idea",
      "description": "Brief description",
      "difficulty": "Easy" OR "Medium" OR "Hard",
      "time_required": "e.g. 15 mins",
      "materials": ["list", "of", "materials"],
      "steps": ["step 1", "step 2", "step 3"],
      "co2_saved": 0.0 (float estimate),
      "category": "Upcycle" OR "Recycle" OR "Repurpose" OR "Compost",
      "safety_notes": ["note 1", "note 2"]
    }}
  ]
}}

IMPORTANT GUIDELINES:
- Be realistic and practical
- If damaged but cleanable, mark as "Conditionally Reusable"
- Only mark "Not Reusable" if truly unsafe or non-functional
- Provide 3-4 specific reuse suggestions if feasible
- Base reasoning ONLY on what was observed in the image
- Do NOT make claims about chemical safety or food safety without clear evidence

Return ONLY valid JSON, no additional text."""
        
        # Generate analysis using Gemini with retry logic
        max_retries = 3
        response_text = ""
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                response_text = response.text.strip()
                break
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise e
        
        # Extract JSON from response
        analysis = parse_llm_json_response(response_text)
        
        # Validate and normalize
        return normalize_analysis(analysis)
        
    except ImportError:
        return generate_error_response("google-generativeai library not installed. Run: pip install google-generativeai")
    except Exception as e:
        return generate_error_response(f"LLM analysis failed: {str(e)}")


def parse_llm_json_response(response_text: str) -> Dict:
    """
    Parse JSON from LLM response, handling markdown code blocks
    
    Args:
        response_text: Raw LLM response
        
    Returns:
        Parsed dictionary
    """
    # Remove markdown code blocks if present
    if "```json" in response_text:
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text)
    elif "```" in response_text:
        response_text = re.sub(r'```\s*', '', response_text)
    
    # Try to parse JSON
    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError:
        # Fallback: try to extract JSON object
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("Could not parse JSON from LLM response")


def normalize_analysis(analysis: Dict) -> Dict:
    """
    Normalize and validate LLM analysis output
    
    Args:
        analysis: Raw LLM output
        
    Returns:
        Validated and normalized analysis
    """
    # Ensure required fields
    normalized = {
        "reuse_feasible": analysis.get("reuse_feasible", False),
        "confidence": max(0, min(100, float(analysis.get("confidence", 50)))),
        "verdict": analysis.get("verdict", "Unknown"),
        "condition_summary": analysis.get("condition_summary", "Analysis unavailable"),
        "reasoning": analysis.get("reasoning", "No reasoning provided"),
        "key_factors": analysis.get("key_factors", []),
        "suggestions": analysis.get("suggestions", [])
    }
    
    # Validate verdict
    valid_verdicts = ["Reusable", "Conditionally Reusable", "Not Reusable"]
    if normalized["verdict"] not in valid_verdicts:
        # Infer verdict from reuse_feasible
        if normalized["reuse_feasible"]:
            normalized["verdict"] = "Reusable" if normalized["confidence"] > 70 else "Conditionally Reusable"
        else:
            normalized["verdict"] = "Not Reusable"
    
    return normalized


def generate_error_response(error_msg: str) -> Dict:
    """
    Generate fallback response for errors
    
    Args:
        error_msg: Error message
        
    Returns:
        Error response dictionary
    """
    return {
        "reuse_feasible": False,
        "confidence": 0,
        "verdict": "Analysis Failed",
        "condition_summary": "Unable to analyze object",
        "reasoning": error_msg,
        "key_factors": [],
        "suggestions": []
    }


def generate_simple_suggestions(object_type: str, condition: str = "moderate") -> List[Dict]:
    """
    Fallback: Generate basic reuse suggestions based on object type
    
    Args:
        object_type: Type of object
        condition: General condition (good/moderate/poor)
        
    Returns:
        List of suggestion dictionaries
    """
    suggestions_map = {
        "plastic": [
            {"use_case": "Storage container", "explanation": "Can hold non-food items", "category": "storage"},
            {"use_case": "Plant pot", "explanation": "Water-resistant material suitable for plants", "category": "outdoor"},
            {"use_case": "Organizer", "explanation": "Can organize small items or craft supplies", "category": "home_utility"}
        ],
        "glass": [
            {"use_case": "Flower vase", "explanation": "Glass is suitable for holding water and flowers", "category": "home_utility"},
            {"use_case": "Storage jar", "explanation": "Can store dry goods or craft materials", "category": "storage"},
            {"use_case": "Candle holder", "explanation": "Heat-resistant and decorative", "category": "diy"}
        ],
        "metal": [
            {"use_case": "Pen holder", "explanation": "Sturdy material for desk organization", "category": "home_utility"},
            {"use_case": "Planter", "explanation": "Can be repurposed for small plants", "category": "outdoor"},
            {"use_case": "Tool storage", "explanation": "Durable for workshop or garage use", "category": "storage"}
        ],
        "cardboard": [
            {"use_case": "Storage box", "explanation": "Lightweight and stackable for organizing", "category": "storage"},
            {"use_case": "DIY project base", "explanation": "Can be cut and modified for crafts", "category": "diy"},
            {"use_case": "Drawer organizer", "explanation": "Can divide and organize drawer spaces", "category": "home_utility"}
        ]
    }
    
    # Find matching suggestions
    for key in suggestions_map:
        if key in object_type.lower():
            return suggestions_map[key][:3]
    
    # Default generic suggestions
    return [
        {"use_case": "Repurpose for storage", "explanation": "Most objects can hold or organize items", "category": "storage"},
        {"use_case": "Upcycle project", "explanation": "Can be modified for creative reuse", "category": "diy"}
    ]