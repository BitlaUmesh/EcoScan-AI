# Ollama Setup Guide

This project now uses **Ollama** for local AI models instead of Gemini API.

## Benefits
✅ No API keys needed  
✅ Everything runs locally (100% private)  
✅ Free and open-source  
✅ No rate limits  

## Installation

### 1. Download & Install Ollama
- **Website**: https://ollama.ai
- **Windows**: Download the installer and run it
- **Mac/Linux**: Follow instructions on the website

### 2. Start Ollama Service
Open a terminal and run:
```bash
ollama serve
```
This will start the Ollama service at `http://localhost:11434`

### 3. Pull Required Models
In a **new terminal**, run:
```bash
# Vision model (for analyzing images)
ollama pull llava

# Reasoning model (for text analysis)
ollama pull mistral
```

This downloads the models (~5-10 GB total). You only need to do this once.

### 4. Run the Application
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the Streamlit app
streamlit run frontend/app.py
```

## Models Used

| Model | Purpose | Size |
|-------|---------|------|
| **llava** | Image vision analysis | ~5 GB |
| **mistral** | Text reasoning/analysis | ~5 GB |

## Troubleshooting

### "Ollama service not running"
- Make sure you ran `ollama serve` in a terminal
- Check that Ollama is accessible at `http://localhost:11434`

### Model download fails
- Requires ~10 GB disk space
- Check your internet connection
- Retry: `ollama pull llava` or `ollama pull mistral`

### Slow performance
- First run takes longer as models are loaded
- Subsequent runs are faster
- Response time depends on your CPU/GPU

## Performance Tips

1. **Enable GPU acceleration** (if you have NVIDIA GPU):
   - Ollama automatically uses GPU if available
   - Install CUDA drivers for faster processing

2. **Use a faster model** (optional):
   - Replace `mistral` with `neural-chat` (smaller, faster)
   - Update in `.env` file: `OLLAMA_REASONING_MODEL=neural-chat`
   - Then: `ollama pull neural-chat`

3. **Keep models in memory**:
   - Once loaded, models stay in memory
   - Subsequent analyses are faster

## API Reference

The app communicates with Ollama at `http://localhost:11434`:

### Generate Text
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "mistral",
    "prompt": "Your prompt here",
    "stream": false
  }'
```

### Generate with Image
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llava",
    "prompt": "Analyze this image",
    "images": ["base64_encoded_image"],
    "stream": false
  }'
```

## Disable Ollama (Go Back to Gemini)

If you want to use Gemini API instead:

1. Update `requirements.txt`:
   ```
   google-generativeai>=0.3.0
   ```

2. Restore original `backend/vision.py` and `backend/reasoning.py`

3. Update `.env` with your Gemini API key:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

---

**Happy waste analyzing with local AI! ♻️**
