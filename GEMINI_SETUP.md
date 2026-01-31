# EcoScan-AI - Gemini API Setup

This project now uses **Google Gemini API** exclusively for all AI operations (vision analysis + reasoning).

## Quick Setup

### 1. Get Your Gemini API Key (Free!)

1. Visit: **https://aistudio.google.com/app/apikey**
2. Click "Create API Key"
3. Select your project (create one if needed)
4. Copy the generated API key

### 2. Configure Your .env File

1. In the project root (`EcoScan-AI` folder), create or edit `.env`:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

2. Replace `your_api_key_here` with your actual API key from step 1

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` - For Gemini API access
- `flask` - Web server
- `pillow` - Image processing
- `python-dotenv` - Environment variable management

### 4. Run the Application

```bash
python server.py
```

The app will open at: **http://localhost:5000**

## How It Works

The system uses Google Gemini API for:

1. **Vision Analysis** (gemini-1.5-flash)
   - Analyzes uploaded waste object images
   - Identifies material type, condition, damage, contamination

2. **Reasoning & Scoring** (gemini-pro)
   - Evaluates reuse potential
   - Generates recommendations
   - Calculates viability scores

## Troubleshooting

### "GEMINI_API_KEY not found in environment variables"

- Make sure `.env` file exists in the project root
- Check that `GEMINI_API_KEY=your_key` is correctly set
- Restart the application after editing `.env`

### "google-generativeai library not installed"

Run:
```bash
pip install google-generativeai
```

### API Rate Limits

Google's free tier has rate limits. If you hit limits:
- Wait a few minutes before retrying
- Consider upgrading your Gemini API quota at: https://aistudio.google.com/app/apikey

## File Structure

```
backend/
  ├── reasoning.py  → LLM-based analysis (uses gemini-pro)
  ├── vision.py     → Image understanding (uses gemini-1.5-flash)
  ├── scoring.py    → Score calculation
  └── utils.py      → Helper functions

frontend/
  ├── index.html    → HTML UI
  ├── static/
  │   ├── css/      → Styling
  │   └── js/       → Interaction logic

server.py           → Flask entry point
.env                → Your API key (CREATE THIS!)
requirements.txt    → Dependencies
```

## Features

✅ **AI-Powered Analysis** - Uses Google's state-of-the-art Gemini models
✅ **No Local Setup** - No need to download/run local models
✅ **Fast & Accurate** - Cloud-based AI for reliable results
✅ **Free Tier Available** - No credit card required to start
✅ **Camera Input** - Analyze waste objects directly from your device

---

For more info about Gemini API: https://ai.google.dev/
