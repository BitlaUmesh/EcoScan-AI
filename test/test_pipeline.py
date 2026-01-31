"""
Terminal Test Runner for Waste Reuse Analysis Pipeline
Run this script to test the complete pipeline without Streamlit UI
"""

import sys
import os
import argparse

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.utils import (
    load_image_from_path,
    check_api_key,
    get_setup_instructions,
    validate_environment
)


def test_basic_analysis(image_path: str):
    """Test basic analysis pipeline"""
    from backend.utils import run_complete_analysis, print_analysis_summary
    
    # Load image
    print(f"Loading image: {image_path}")
    image = load_image_from_path(image_path)
    
    if image is None:
        print("ERROR: Failed to load image")
        return False
    
    print(f"✓ Image loaded successfully ({image.size[0]}x{image.size[1]} pixels)\n")
    
    # Run analysis
    print("Starting analysis pipeline...\n")
    result = run_complete_analysis(image)
    
    # Print results
    print_analysis_summary(result)
    
    return result.get("status") == "success"


def test_transformation_intelligence(image_path: str):
    """Test the complete transformation intelligence pipeline"""
    from backend.orchestrator import (
        run_complete_analysis_with_transformation,
        generate_transformation_intelligence
    )
    
    print("\n" + "=" * 60)
    print("TESTING TRANSFORMATION INTELLIGENCE")
    print("=" * 60 + "\n")
    
    # Load image
    print(f"Loading image: {image_path}")
    image = load_image_from_path(image_path)
    
    if not image:
        print("ERROR: Failed to load image")
        return False
    
    print(f"✓ Image loaded successfully ({image.size[0]}x{image.size[1]} pixels)\n")
    
    # Run basic analysis
    print("Running basic analysis...")
    basic_result = run_complete_analysis_with_transformation(image)
    
    if basic_result.get("status") != "success":
        print("❌ Basic analysis failed")
        return False
    
    print(f"✓ Basic analysis complete")
    print(f"  Object: {basic_result.get('object_type')}")
    print(f"  Score: {basic_result.get('score')}/100")
    print(f"  Verdict: {basic_result.get('verdict')}")
    
    # Generate transformation intelligence
    print("\nGenerating transformation intelligence...")
    full_result = generate_transformation_intelligence(basic_result)
    
    if 'transformation_intelligence' not in full_result:
        print("❌ Transformation intelligence generation failed")
        return False
    
    ti = full_result['transformation_intelligence']
    
    print("\n" + "-" * 60)
    print("TRANSFORMATION INTELLIGENCE RESULTS")
    print("-" * 60)
    
    print(f"\n🎯 Target Product: {ti['target_selection']['target_product']}")
    print(f"Reason: {ti['target_selection']['reason_for_selection']}")
    
    print(f"\n📋 Transformation Procedure ({len(ti['procedure']['procedure_steps'])} steps):")
    for i, step in enumerate(ti['procedure']['procedure_steps'], 1):
        print(f"  {i}. {step}")
    
    print(f"\n⏱️  Time: {ti['procedure']['estimated_time_minutes']} minutes")
    print(f"📊 Difficulty: {ti['procedure']['difficulty_level']}")
    
    print(f"\n🛠️  Tools: {', '.join(ti['procedure']['required_tools'])}")
    print(f"📦 Materials: {', '.join(ti['procedure']['required_materials'])}")
    
    print(f"\n⚠️  Safety: {ti['procedure']['safety_notes']}")
    
    print(f"\n📊 Quality Assessment:")
    print(f"  Lifespan: {ti['quality_assessment']['expected_lifespan_months']} months")
    print(f"  Stability: {ti['quality_assessment']['structural_stability']}")
    print(f"  Limitations: {ti['quality_assessment']['usage_limitations']}")
    
    price = ti['pricing']['suggested_price_range']
    print(f"\n💰 Market Price: ₹{price['min']} - ₹{price['max']}")
    print(f"Confidence: {ti['pricing']['pricing_confidence']}")
    
    print(f"\n💡 Pricing Reasoning:")
    for reason in ti['pricing']['pricing_reasoning']:
        print(f"  - {reason}")
    
    print("\n" + "=" * 60)
    print("✓ TRANSFORMATION INTELLIGENCE TEST COMPLETE")
    print("=" * 60 + "\n")
    
    return True


def main():
    """Main test function"""
    
    print("\n" + "=" * 60)
    print("WASTE REUSE INTELLIGENCE SYSTEM - TEST RUNNER")
    print("=" * 60 + "\n")
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Test waste reuse analysis pipeline")
    parser.add_argument(
        "image_path",
        nargs='?',
        help="Path to waste object image file"
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="Check environment and dependencies"
    )
    parser.add_argument(
        "--transformation",
        action="store_true",
        help="Test transformation intelligence pipeline"
    )
    
    args = parser.parse_args()
    
    # Environment check mode
    if args.check_env:
        print("Checking environment...")
        checks = validate_environment()
        
        print("\nDependency Status:")
        print("-" * 40)
        for dep, status in checks.items():
            status_icon = "✓" if status else "✗"
            print(f"{status_icon} {dep}: {'OK' if status else 'MISSING'}")
        
        if not checks["api_key"]:
            print("\n" + get_setup_instructions())
        
        all_ok = all(checks.values())
        print("\n" + ("✓ All checks passed!" if all_ok else "✗ Some checks failed"))
        sys.exit(0 if all_ok else 1)
    
    # Check if image path provided
    if not args.image_path:
        print("Usage: python test_pipeline.py <image_path>")
        print("       python test_pipeline.py --check-env")
        print("       python test_pipeline.py --transformation <image_path>")
        print("\nExamples:")
        print("  python test_pipeline.py waste_bottle.jpg")
        print("  python test_pipeline.py --transformation waste_bottle.jpg")
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        print("ERROR: API key not configured\n")
        print(get_setup_instructions())
        sys.exit(1)
    
    # Run appropriate test
    if args.transformation:
        success = test_transformation_intelligence(args.image_path)
    else:
        success = test_basic_analysis(args.image_path)
    
    # Return appropriate exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()