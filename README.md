# EcoScan-AI: Waste Reuse Intelligence System

An AI-powered system that analyzes waste objects and provides reuse/upcycling recommendations using Google Gemini API.

## Features
- 📸 **Object Identification**: Uses Gemini Vision to identify waste items.
- 🛡️ **Safety Assessment**: Analyzes materials and condition for human safety.
- ✨ **AI Recommendations**: Generates personalized upcycling ideas with step-by-step instructions.
- 🍃 **Impact Tracking**: Estimates CO₂ savings for each reuse case.
- 💻 **Modern HTML Frontend**: A clean, responsive web interface built with HTML/CSS/JS and Flask.

## Quick Start

1. **Get a Gemini API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. **Run the Application**:
   Double-click `start.bat` and select option **1** (Launch Web Application).
   The app will be available at `http://localhost:5000`.

## Project Structure
- `server.py`: Flask backend serving the HTML frontend and API.
- `frontend/`: HTML, CSS, and JS files.
- `backend/`: Core logic for vision, reasoning, and scoring.
- `requirements.txt`: Python dependencies.
