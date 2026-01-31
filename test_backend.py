"""
Quick test script to verify backend setup
"""
import os
import sys
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

print("=" * 50)
print("EcoScan-AI Backend Configuration Test")
print("=" * 50)

# Check API Key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print("[OK] GEMINI_API_KEY is set")
    print(f"     Key starts with: {api_key[:10]}...")
else:
    print("[ERROR] GEMINI_API_KEY is NOT set")
    print("\n     To fix this:")
    print("     1. Create a .env file in the project root")
    print("     2. Add: GEMINI_API_KEY=your_api_key_here")
    print("     3. Get a free key at: https://aistudio.google.com/app/apikey")

print("\n" + "=" * 50)
print("Checking Dependencies")
print("=" * 50)

# Check required packages
packages = {
    "flask": "Flask",
    "flask_cors": "Flask-CORS",
    "PIL": "Pillow",
    "google.generativeai": "google-generativeai",
    "dotenv": "python-dotenv"
}

for module_name, package_name in packages.items():
    try:
        __import__(module_name)
        print(f"[OK] {package_name} is installed")
    except ImportError:
        print(f"[ERROR] {package_name} is NOT installed")
        print(f"        Install with: pip install {package_name}")

print("\n" + "=" * 50)
print("Server Status")
print("=" * 50)
print("Backend server should be running at: http://localhost:5000")
print("Frontend HTML interface at: http://localhost:5000/")
print("\nIf you see errors, make sure:")
print("1. GEMINI_API_KEY is set in .env file")
print("2. All dependencies are installed: pip install -r requirements.txt")
print("3. Server is running: python server.py")
print("=" * 50)