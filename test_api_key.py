"""
API Key Diagnostic Tool
Tests if the Gemini API key is properly configured and working
"""

import os
import sys
from pathlib import Path

def test_api_key():
    """Test API key configuration and validity"""
    
    print("=" * 60)
    print("API KEY DIAGNOSTIC TEST")
    print("=" * 60)
    print()
    
    # Test 1: Check if .env file exists
    print("Test 1: Checking .env file...")
    env_path = Path(".env")
    if env_path.exists():
        print("✓ .env file found")
        with open(env_path, 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY' in content:
                print("✓ GEMINI_API_KEY found in .env file")
            else:
                print("✗ GEMINI_API_KEY not found in .env file")
                return
    else:
        print("✗ .env file not found")
        return
    print()
    
    # Test 2: Check python-dotenv
    print("Test 2: Checking python-dotenv...")
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv is installed")
    except ImportError:
        print("✗ python-dotenv not installed")
        print("  Install with: pip install python-dotenv")
        return
    print()
    
    # Test 3: Load environment variables
    print("Test 3: Loading .env file...")
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        # Mask the key for security
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
        print(f"✓ API key loaded: {masked_key}")
        print(f"  Key length: {len(api_key)} characters")
    else:
        print("✗ API key not loaded from environment")
        print("  Make sure .env file has: GEMINI_API_KEY=your-key-here")
        return
    print()
    
    # Test 4: Check google-generativeai
    print("Test 4: Checking google-generativeai library...")
    try:
        import google.generativeai as genai
        print("✓ google-generativeai is installed")
    except ImportError:
        print("✗ google-generativeai not installed")
        print("  Install with: pip install google-generativeai")
        return
    print()
    
    # Test 5: Test API key with Gemini
    print("Test 5: Testing API key with Gemini API...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test prompt
        response = model.generate_content("Say 'API key is working' if you can read this.")
        
        print("✓ API key is VALID and working!")
        print(f"  Response: {response.text[:50]}...")
        print()
        print("=" * 60)
        print("SUCCESS! Your API key is properly configured.")
        print("=" * 60)
        
    except Exception as e:
        error_msg = str(e)
        print(f"✗ API key test FAILED")
        print(f"  Error: {error_msg}")
        print()
        
        if "API_KEY_INVALID" in error_msg or "expired" in error_msg.lower():
            print("=" * 60)
            print("ISSUE IDENTIFIED: Invalid or Expired API Key")
            print("=" * 60)
            print()
            print("Your API key is either invalid or has expired.")
            print()
            print("To fix this:")
            print("1. Visit: https://aistudio.google.com/app/apikey")
            print("2. Sign in with your Google account")
            print("3. Create a new API key")
            print("4. Update your .env file with the new key:")
            print("   GEMINI_API_KEY=your-new-key-here")
            print("5. Restart the application")
        else:
            print("=" * 60)
            print("UNEXPECTED ERROR")
            print("=" * 60)
            print()
            print("An unexpected error occurred. Please check:")
            print("- Your internet connection")
            print("- Google AI Studio service status")
            print("- API key format (no extra spaces or quotes)")

if __name__ == "__main__":
    test_api_key()