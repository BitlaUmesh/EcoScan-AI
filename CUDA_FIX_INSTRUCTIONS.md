# Fixing Ollama CUDA Error

## Problem
You're seeing: `❌ Analysis Failed: Ollama error: {"error":"llama runner process has terminated: CUDA error"}`

This happens when Ollama tries to use your GPU but encounters CUDA driver issues.

## Quick Fix - Run Ollama in CPU Mode

### Option 1: Use the Fix Script (Easiest)
1. Run the provided script:
   ```bash
   fix_ollama_cuda.bat
   ```
2. This will restart Ollama in CPU-only mode
3. Then run your app normally:
   ```bash
   streamlit run frontend\app.py
   ```

### Option 2: Manual Fix
1. **Stop Ollama completely:**
   - Close any Ollama windows
   - Or run: `taskkill /F /IM ollama.exe`

2. **Start Ollama in CPU mode:**
   Open a new terminal and run:
   ```bash
   set OLLAMA_NUM_GPU=0
   ollama serve
   ```

3. **Keep that terminal open** and in a new terminal run:
   ```bash
   streamlit run frontend\app.py
   ```

## Permanent Fix - Update CUDA Drivers

If you want to use GPU acceleration (faster):

1. **Check your GPU:**
   ```bash
   nvidia-smi
   ```

2. **Update NVIDIA drivers:**
   - Visit: https://www.nvidia.com/Download/index.aspx
   - Download latest drivers for your GPU
   - Install and restart

3. **Verify CUDA installation:**
   ```bash
   nvcc --version
   ```

4. **Restart Ollama normally:**
   ```bash
   ollama serve
   ```

## Performance Comparison

| Mode | Speed | Setup |
|------|-------|-------|
| **CPU** | Slower (5-15 sec per analysis) | Works immediately |
| **GPU** | Faster (1-3 sec per analysis) | Requires CUDA drivers |

## Still Having Issues?

### Alternative: Use Smaller Models
Edit `backend/reasoning.py` and `backend/vision.py` to use lighter models:

```python
# In reasoning.py line 100, change:
"model": "mistral"
# to:
"model": "tinyllama"  # Much smaller, faster on CPU
```

Then pull the model:
```bash
ollama pull tinyllama
```

### Check Ollama Status
```bash
# See what models are loaded
curl http://localhost:11434/api/tags

# Test if Ollama is responding
curl http://localhost:11434/api/generate -d '{"model":"mistral","prompt":"test","stream":false}'
```

## Summary

**For immediate use:** Run Ollama in CPU mode using the fix script or manual steps above.

**For best performance:** Fix CUDA drivers and use GPU acceleration.