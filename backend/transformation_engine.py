"""
Transformation Engine - Waste-to-Product Conversion Intelligence
Generates step-by-step transformation procedures and quality assessments
"""

import os
from typing import Dict, List, Optional
import json
import re


def select_primary_reuse_target(
    suggestions: List[Dict],
    object_type: str,
    condition_summary: str,
    api_key: Optional[str] = None
) -> Dict:
    """
    Select the most practical reuse target from suggestions
    
    Args:
        suggestions: List of reuse suggestions from reasoning module
        object_type: Type of waste object
        condition_summary: Condition assessment
        api_key: Optional Gemini API key
        
    Returns:
        Dictionary with target product and selection reasoning
    """
    if not suggestions:
        return {
            "target_product": "General storage container",
            "reason_for_selection": "Default fallback for basic reuse"
        }
    
    try:
        import google.generativeai as genai
        
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            # Fallback to first suggestion
            return {
                "target_product": suggestions[0]["use_case"],
                "reason_for_selection": suggestions[0]["explanation"]
            }
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        suggestions_text = "\n".join([
            f"- {s['use_case']}: {s['explanation']}"
            for s in suggestions
        ])
        
        prompt = f"""
You are selecting the BEST reuse target for a waste object transformation project.

OBJECT TYPE: {object_type}
CONDITION: {condition_summary}

AVAILABLE REUSE OPTIONS:
{suggestions_text}

SELECT ONE option that is:
1. Most practical for individuals/small workshops
2. Achievable with basic tools
3. Safe and realistic
4. Has clear utility value

Respond in JSON format:
{{
  "target_product": "Specific product name",
  "reason_for_selection": "Why this is the best choice given the object's condition"
}}

Return ONLY valid JSON.
"""
        
        response = model.generate_content(prompt)
        result = parse_json_response(response.text)
        
        return result
        
    except Exception as e:
        # Fallback to first suggestion
        return {
            "target_product": suggestions[0]["use_case"],
            "reason_for_selection": suggestions[0]["explanation"]
        }


def generate_transformation_procedure(
    object_type: str,
    target_product: str,
    condition_summary: str,
    visual_description: str,
    api_key: Optional[str] = None
) -> Dict:
    """
    Generate detailed step-by-step transformation procedure
    
    This is the CORE ORIGINAL LOGIC that demonstrates system design.
    
    Args:
        object_type: Type of waste object
        target_product: Selected reuse target
        condition_summary: Object condition
        visual_description: Detailed visual analysis
        api_key: Optional API key
        
    Returns:
        Complete transformation procedure with tools, materials, time
    """
    try:
        import google.generativeai as genai
        
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            return generate_fallback_procedure(object_type, target_product)
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
You are a sustainability engineer and product designer.
Your task is to create a DETAILED, ACTIONABLE transformation procedure.

WASTE OBJECT:
Type: {object_type}
Condition: {condition_summary}
Visual Details: {visual_description}

TARGET PRODUCT:
{target_product}

Generate a step-by-step procedure that explains HOW to transform this waste object into the target product.

Requirements:
1. Steps must be clear and actionable
2. Consider the object's current condition
3. Use only basic household tools
4. Include safety precautions
5. Be realistic about skill level needed
6. Estimate time accurately

Respond in JSON format:
{{
  "procedure_steps": [
    "Step 1 description",
    "Step 2 description",
    "Step 3 description"
  ],
  "required_tools": ["Tool 1", "Tool 2"],
  "required_materials": ["Material 1", "Material 2"],
  "estimated_time_minutes": 30,
  "difficulty_level": "Low" or "Medium",
  "safety_notes": "Important safety considerations"
}}

IMPORTANT:
- Steps should be 5-10 detailed actions
- Tools should be common household items
- Time estimate should be realistic (15-120 minutes)
- Difficulty: "Low" for simple tasks, "Medium" for moderate skill

Return ONLY valid JSON.
"""
        
        response = model.generate_content(prompt)
        result = parse_json_response(response.text)
        
        # Validate and normalize
        return normalize_procedure(result)
        
    except Exception as e:
        return generate_fallback_procedure(object_type, target_product)


def assess_transformation_quality(
    target_product: str,
    object_type: str,
    condition_summary: str,
    procedure: Dict,
    api_key: Optional[str] = None
) -> Dict:
    """
    Assess expected quality and lifespan of transformed product
    
    Args:
        target_product: The reused product
        object_type: Original waste type
        condition_summary: Condition assessment
        procedure: Transformation procedure
        api_key: Optional API key
        
    Returns:
        Quality assessment with lifespan and limitations
    """
    try:
        import google.generativeai as genai
        
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            return generate_fallback_quality_assessment(target_product)
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
You are assessing the expected quality of a transformed waste product.

ORIGINAL WASTE: {object_type}
CONDITION: {condition_summary}
TRANSFORMED INTO: {target_product}
DIFFICULTY: {procedure.get('difficulty_level', 'Medium')}

Evaluate the expected quality of the FINAL PRODUCT after transformation:

1. Expected lifespan (in months)
2. Usage limitations
3. Structural stability after transformation

Respond in JSON format:
{{
  "expected_lifespan_months": 12,
  "usage_limitations": "Specific limitations based on material and transformation",
  "structural_stability": "High/Medium/Low"
}}

Be realistic and conservative in estimates.
Return ONLY valid JSON.
"""
        
        response = model.generate_content(prompt)
        result = parse_json_response(response.text)
        
        return normalize_quality_assessment(result)
        
    except Exception as e:
        return generate_fallback_quality_assessment(target_product)


def calculate_market_price(
    target_product: str,
    quality_assessment: Dict,
    procedure: Dict,
    object_type: str
) -> Dict:
    """
    Calculate fair market price for transformed product
    
    This uses ORIGINAL PRICING LOGIC based on multiple factors:
    - Product utility value
    - Expected lifespan
    - Transformation difficulty (labor value)
    - Material sustainability premium
    
    Args:
        target_product: Transformed product name
        quality_assessment: Quality and lifespan data
        procedure: Transformation procedure with time/difficulty
        object_type: Original waste type
        
    Returns:
        Price range with reasoning
    """
    # Base pricing logic for Indian market (realistic, down-to-earth prices)
    base_prices = {
        "storage": 80,
        "planter": 100,
        "organizer": 60,
        "holder": 50,
        "container": 70,
        "shelf": 150,
        "box": 90,
        "pot": 80,
        "vase": 120,
        "decoration": 70,
        "tool": 60,
        "basket": 75,
        "tray": 85,
        "chair": 300,
        "table": 400,
        "shelf unit": 200,
        "bench": 250,
    }
    
    # Determine base price from product category
    base_price = 75  # default for Indian market
    for category, price in base_prices.items():
        if category in target_product.lower():
            base_price = price
            break
    
    # Factor 1: Lifespan adjustment (more conservative)
    lifespan_months = quality_assessment.get("expected_lifespan_months", 12)
    lifespan_multiplier = 1.0
    if lifespan_months >= 24:
        lifespan_multiplier = 1.15
    elif lifespan_months >= 12:
        lifespan_multiplier = 1.05
    elif lifespan_months < 6:
        lifespan_multiplier = 0.9
    
    # Factor 2: Difficulty/labor adjustment (reduced for Indian market)
    difficulty = procedure.get("difficulty_level", "Medium")
    time_minutes = procedure.get("estimated_time_minutes", 30)
    
    labor_multiplier = 1.0
    if difficulty == "Easy":
        labor_multiplier = 1.05
    elif difficulty == "Medium":
        labor_multiplier = 1.1
    elif difficulty == "Hard":
        labor_multiplier = 1.15
    
    if time_minutes > 120:
        labor_multiplier += 0.1
    elif time_minutes > 60:
        labor_multiplier += 0.05
    
    # Factor 3: Sustainability premium (10% - modest for Indian market)
    sustainability_premium = 1.10
    
    # Calculate final price
    calculated_price = base_price * lifespan_multiplier * labor_multiplier * sustainability_premium
    
    # Generate range (±10% - tighter range for market realism)
    min_price = int(calculated_price * 0.90)
    max_price = int(calculated_price * 1.10)
    
    # Round to nearest 5 for Indian market affordability
    min_price = round(min_price / 5) * 5
    max_price = round(max_price / 5) * 5
    
    # Generate reasoning
    reasoning = []
    reasoning.append(f"Market rate for {target_product.lower()} in Indian second-hand/upcycled market")
    
    if lifespan_months >= 12:
        reasoning.append(f"Durability: Expected {lifespan_months}+ months lifespan")
    elif lifespan_months < 6:
        reasoning.append(f"Limited durability: {lifespan_months} months expected use")
    
    if difficulty == "Hard" and time_minutes > 60:
        reasoning.append("Significant craftsmanship and time investment")
    elif difficulty == "Medium":
        reasoning.append("Moderate effort required")
    else:
        reasoning.append("Simple transformation process")
    
    reasoning.append("Eco-friendly upcycled product value")
    
    if quality_assessment.get("structural_stability") == "High":
        reasoning.append("Structurally sound and reliable")
    
    # Determine confidence based on Indian market realism
    confidence = "Medium"
    if lifespan_months >= 12 and difficulty in ["Low", "Easy"]:
        confidence = "High"
    elif lifespan_months < 6 or difficulty == "Hard":
        confidence = "Low"
    else:
        confidence = "Medium"
    
    return {
        "suggested_price_range": {
            "min": min_price,
            "max": max_price,
            "currency": "INR"
        },
        "pricing_reasoning": reasoning,
        "pricing_confidence": confidence,
        "pricing_factors": {
            "base_price": base_price,
            "lifespan_multiplier": round(lifespan_multiplier, 2),
            "labor_multiplier": round(labor_multiplier, 2),
            "sustainability_premium": round(sustainability_premium, 2)
        }
    }


def generate_decision_trace(
    target_selection: Dict,
    procedure: Dict,
    quality_assessment: Dict,
    pricing: Dict,
    vision_description: str,
    condition_summary: str
) -> Dict:
    """
    Generate explainable decision trace showing EcoScan AI's reasoning
    
    This separates:
    - What the vision model observed
    - What EcoScan AI inferred
    - What EcoScan AI decided
    
    Args:
        target_selection: Selected reuse target
        procedure: Transformation procedure
        quality_assessment: Quality metrics
        pricing: Pricing calculation
        vision_description: Original vision output
        condition_summary: Condition analysis
        
    Returns:
        Structured decision trace
    """
    trace = {
        "observation_layer": {
            "title": "What the Vision AI Observed",
            "content": vision_description,
            "source": "Google Gemini Vision Model"
        },
        "inference_layer": {
            "title": "What EcoScan AI Inferred",
            "inferences": [
                f"Object condition: {condition_summary}",
                f"Structural suitability for transformation: {quality_assessment.get('structural_stability', 'Medium')}",
                f"Estimated transformation complexity: {procedure.get('difficulty_level', 'Medium')} difficulty"
            ]
        },
        "decision_layer": {
            "title": "What EcoScan AI Decided",
            "decisions": [
                {
                    "decision": f"Selected '{target_selection['target_product']}' as optimal reuse target",
                    "reasoning": target_selection['reason_for_selection']
                },
                {
                    "decision": f"Designed {len(procedure.get('procedure_steps', []))}-step transformation procedure",
                    "reasoning": f"Procedure optimized for {procedure.get('difficulty_level', 'medium')} skill level with estimated {procedure.get('estimated_time_minutes', 0)} minutes completion time"
                },
                {
                    "decision": f"Priced at ₹{pricing['suggested_price_range']['min']}-₹{pricing['suggested_price_range']['max']}",
                    "reasoning": " | ".join(pricing['pricing_reasoning'][:2])
                }
            ]
        },
        "transparency_note": "All decisions are AI-assisted estimates based on visual analysis and learned patterns. Final transformation results depend on user skill and execution."
    }
    
    return trace


# Helper functions

def parse_json_response(text: str) -> Dict:
    """Parse JSON from LLM response"""
    if "```json" in text:
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
    elif "```" in text:
        text = re.sub(r'```\s*', '', text)
    
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}


def normalize_procedure(procedure: Dict) -> Dict:
    """Normalize and validate procedure output"""
    return {
        "procedure_steps": procedure.get("procedure_steps", ["Procedure generation failed"]),
        "required_tools": procedure.get("required_tools", ["Basic tools"]),
        "required_materials": procedure.get("required_materials", ["As needed"]),
        "estimated_time_minutes": max(10, min(180, int(procedure.get("estimated_time_minutes", 30)))),
        "difficulty_level": procedure.get("difficulty_level", "Medium") if procedure.get("difficulty_level") in ["Low", "Medium"] else "Medium",
        "safety_notes": procedure.get("safety_notes", "Exercise caution during transformation")
    }


def normalize_quality_assessment(assessment: Dict) -> Dict:
    """Normalize quality assessment"""
    return {
        "expected_lifespan_months": max(3, min(60, int(assessment.get("expected_lifespan_months", 12)))),
        "usage_limitations": assessment.get("usage_limitations", "Use as intended for best results"),
        "structural_stability": assessment.get("structural_stability", "Medium")
    }


def generate_fallback_procedure(object_type: str, target_product: str) -> Dict:
    """Fallback procedure if AI fails"""
    return {
        "procedure_steps": [
            f"Clean the {object_type} thoroughly",
            "Assess structural integrity",
            f"Modify as needed for {target_product} use",
            "Add finishing touches",
            "Test functionality"
        ],
        "required_tools": ["Cleaning supplies", "Basic cutting tool"],
        "required_materials": ["As needed based on design"],
        "estimated_time_minutes": 30,
        "difficulty_level": "Medium",
        "safety_notes": "Use protective equipment when cutting or modifying materials"
    }


def generate_fallback_quality_assessment(target_product: str) -> Dict:
    """Fallback quality assessment"""
    return {
        "expected_lifespan_months": 12,
        "usage_limitations": f"Use {target_product} as intended for best longevity",
        "structural_stability": "Medium"
    }