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
    run_complete_analysis,
    print_analysis_summary,
    check_api_key,
    get_setup_instructions,
    validate_environment
)


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
        print("\nExample:")
        print("  python test_pipeline.py waste_bottle.jpg")
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        print("ERROR: API key not configured\n")
        print(get_setup_instructions())
        sys.exit(1)
    
    # Load image
    print(f"Loading image: {args.image_path}")
    image = load_image_from_path(args.image_path)
    
    if image is None:
        print("ERROR: Failed to load image")
        sys.exit(1)
    
    print(f"✓ Image loaded successfully ({image.size[0]}x{image.size[1]} pixels)\n")
    
    # Run analysis
    print("Starting analysis pipeline...\n")
    result = run_complete_analysis(image)
    
    # Print results
    print_analysis_summary(result)
    
    # Return appropriate exit code
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()