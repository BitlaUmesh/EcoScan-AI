"""
Orchestrator - Complete EcoScan AI Intelligence Pipeline
Coordinates all analysis stages including transformation and pricing
"""

from typing import Dict, Optional
from PIL import Image

from backend.vision import analyze_waste_object, validate_image
from backend.reasoning import analyze_reuse_potential
from backend.scoring import format_final_output
from backend.transformation_engine import (
    select_primary_reuse_target,
    generate_transformation_procedure,
    assess_transformation_quality,
    calculate_market_price,
    generate_decision_trace
)


def run_complete_analysis_with_transformation(
    image: Image.Image,
    api_key: Optional[str] = None
) -> Dict:
    """
    Run complete EcoScan AI pipeline including transformation intelligence
    
    Pipeline stages:
    1. Vision analysis (existing)
    2. Reuse reasoning (existing)
    3. Scoring (existing)
    4. Target selection (NEW)
    5. Transformation procedure (NEW)
    6. Quality assessment (NEW)
    7. Market pricing (NEW)
    8. Decision trace (NEW)
    
    Args:
        image: PIL Image object
        api_key: Optional API key
        
    Returns:
        Complete analysis with transformation and pricing
    """
    # Validate image
    if not validate_image(image):
        return {
            "status": "error",
            "error": "Invalid image: Image too small or corrupted"
        }
    
    print("Step 1: Analyzing image with vision AI...")
    vision_result = analyze_waste_object(image, api_key)
    
    if vision_result["status"] != "success":
        return {
            "status": "error",
            "error": vision_result["description"]
        }
    
    print(f"✓ Vision analysis complete. Detected: {vision_result['object_type']}")
    
    print("Step 2: Performing reuse analysis with LLM...")
    analysis = analyze_reuse_potential(
        vision_result["description"],
        vision_result["object_type"],
        api_key
    )
    
    print(f"✓ Analysis complete. Verdict: {analysis['verdict']}")
    
    # Format basic output
    basic_output = format_final_output(vision_result, analysis)
    basic_output["status"] = "success"
    
    return basic_output


def generate_transformation_intelligence(
    basic_analysis: Dict,
    api_key: Optional[str] = None
) -> Dict:
    """
    Generate transformation and pricing intelligence
    
    This is the NEW intelligence layer that demonstrates original system design.
    
    Args:
        basic_analysis: Output from basic analysis pipeline
        api_key: Optional API key
        
    Returns:
        Extended analysis with transformation and pricing
    """
    if basic_analysis.get("status") != "success":
        return basic_analysis
    
    print("\n" + "="*60)
    print("TRANSFORMATION INTELLIGENCE LAYER")
    print("="*60)
    
    # Stage 1: Select primary reuse target
    print("\nStep 3: Selecting optimal reuse target...")
    target_selection = select_primary_reuse_target(
        basic_analysis.get("suggestions", []),
        basic_analysis.get("object_type", "unknown"),
        basic_analysis.get("condition_summary", ""),
        api_key
    )
    print(f"✓ Selected target: {target_selection['target_product']}")
    
    # Stage 2: Generate transformation procedure
    print("\nStep 4: Generating transformation procedure...")
    procedure = generate_transformation_procedure(
        basic_analysis.get("object_type", "unknown"),
        target_selection["target_product"],
        basic_analysis.get("condition_summary", ""),
        basic_analysis.get("visual_description", ""),
        api_key
    )
    print(f"✓ Procedure generated: {len(procedure['procedure_steps'])} steps, {procedure['estimated_time_minutes']} minutes")
    
    # Stage 3: Assess transformation quality
    print("\nStep 5: Assessing post-transformation quality...")
    quality_assessment = assess_transformation_quality(
        target_selection["target_product"],
        basic_analysis.get("object_type", "unknown"),
        basic_analysis.get("condition_summary", ""),
        procedure,
        api_key
    )
    print(f"✓ Quality assessed: {quality_assessment['expected_lifespan_months']} months lifespan")
    
    # Stage 4: Calculate market price
    print("\nStep 6: Calculating fair market price...")
    pricing = calculate_market_price(
        target_selection["target_product"],
        quality_assessment,
        procedure,
        basic_analysis.get("object_type", "unknown")
    )
    print(f"✓ Price calculated: ₹{pricing['suggested_price_range']['min']}-₹{pricing['suggested_price_range']['max']}")
    
    # Stage 5: Generate decision trace
    print("\nStep 7: Generating decision trace...")
    decision_trace = generate_decision_trace(
        target_selection,
        procedure,
        quality_assessment,
        pricing,
        basic_analysis.get("visual_description", ""),
        basic_analysis.get("condition_summary", "")
    )
    print("✓ Decision trace complete")
    
    print("\n" + "="*60)
    print("TRANSFORMATION INTELLIGENCE COMPLETE")
    print("="*60 + "\n")
    
    # Combine all results
    extended_analysis = basic_analysis.copy()
    extended_analysis.update({
        "transformation_intelligence": {
            "target_selection": target_selection,
            "procedure": procedure,
            "quality_assessment": quality_assessment,
            "pricing": pricing,
            "decision_trace": decision_trace
        }
    })
    
    return extended_analysis