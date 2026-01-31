# EcoScan-AI: Waste Reuse Intelligence System

An AI-powered system that analyzes waste objects and provides reuse/upcycling recommendations using Google Gemini API.

## Features
- 📸 **Object Identification**: Uses Gemini Vision to identify waste items.
- 🛡️ **Safety Assessment**: Analyzes materials and condition for human safety.
- ✨ **AI Recommendations**: Generates personalized upcycling ideas with step-by-step instructions.
- 🍃 **Impact Tracking**: Estimates CO₂ savings for each reuse case.
- 💻 **Modern HTML5 Frontend**: A clean, responsive web interface built with vanilla HTML/CSS/JavaScript and Flask.
- 💰 **Market Pricing**: Estimates fair market value for recycled products based on Indian market standards.

## Quick Start

1. **Get a Gemini API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. **Run the Application**:
   Double-click `start.bat`
   
   The app will be available at `http://localhost:5000`.

## Project Structure
- `server.py`: Flask backend serving the HTML frontend and API.
- `frontend/`: HTML, CSS, and JavaScript files.
- `backend/`: Core logic for vision, reasoning, scoring, and pricing.
- `requirements.txt`: Python dependencies.

## Technologies Used
- **Backend**: Python, Flask, Google Gemini API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Image Processing**: PIL/Pillow
- **Environment Management**: python-dotenv
