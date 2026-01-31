"""
WSGI entry point for production deployment
Used by gunicorn and other WSGI servers
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the Flask app
from server import app

if __name__ == "__main__":
    app.run()
