# FREE Deployment Guide - EcoScan-AI

Deploy your app completely FREE using Render.com. Takes 5 minutes, zero credit card needed for free tier.

---

## Deploy to Render.com (100% FREE)

Render.com offers a free tier - no credit card required, completely free forever for hobby projects.

### Step 1: Prepare Your Repository
```bash
# Make sure everything is committed to git
git add .
git commit -m "Production ready"
git push origin main
```

### Step 2: Sign Up to Render
1. Go to [render.com](https://render.com)
2. Click "Sign Up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your GitHub account

### Step 3: Create New Web Service
1. Dashboard → "New +" → "Web Service"
2. Select your **EcoScan-AI** repository
3. Click "Connect"

### Step 4: Configure Deployment

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | ecoscan-ai |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:app` |
| **Instance Type** | Free |

### Step 5: Add Environment Variables

1. Scroll to "Environment" section
2. Click "Add Environment Variable"
3. Add these variables:

```
GEMINI_API_KEY = your_actual_api_key_here
---

## Alternative: Google Cloud Run (FREE)

Another completely free option with even faster performance.

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project (name: EcoScan-AI)
3. Wait for creation to complete

### Step 2: Enable Required APIs
1. Search for "Cloud Run API"
2. Click Enable
3. Search for "Container Registry API"
4. Click Enable

### Step 3: Deploy Using gcloud CLI

```bash
# 1. Install Google Cloud SDK
# From: https://cloud.google.com/sdk/docs/install

# 2. Initialize gcloud
gcloud init

# 3. Login
gcloud auth login

# 4. Set project
gcloud config set project YOUR_PROJECT_ID

# 5. Build and deploy
gcloud run deploy ecoscan-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_actual_key_here
```

You'll get a URL like: `https://ecoscan-ai-xxxxx.run.app`

---

## Alternative: PythonAnywhere (FREE Tier)

Free tier with 100MB storage. Good for testing.

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Click "Sign up for free account"
3. Create account

### Step 2: Upload Code
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Python 3.10" with Flask
4. Go to "Files" tab
5. Upload your project files

### Step 3: Configure WSGI
1. Go to "Web" tab
2. Under "WSGI configuration file", click the path
3. Replace content with:
```python
import sys
sys.path.append('/home/yourusername/mysite')

from wsgi import app
application = app
```

### Step 4: Set Environment Variables
1. Web tab → Scroll to "Environment variables"
2. Add:
   - `GEMINI_API_KEY=your_key`
   - `FLASK_ENV=production`

### Step 5: Reload
Click "Reload" button. Your app is at: `https://yourusername.pythonanywhere.com`

---

## Alternative: Railway.app (FREE - $5 Credit)

Railway gives $5 free credit monthly. Enough for a hobby project.

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: Create Project
1. Dashboard → "New Project"
2. Select "Deploy from GitHub repo"
3. Choose **EcoScan-AI** repository
4. Authorize Railway

### Step 3: Add Variables
1. Go to "Variables" tab
2. Add:
   - `GEMINI_API_KEY=your_key_here`
   - `FLASK_ENV=production`

### Step 4: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes
3. Get your URL from "Deployments" tab

---

## Which One Should I Choose?

| Platform | Setup Time | Free Tier | Cold Start | Best For |
|----------|-----------|-----------|-----------|----------|
| **Render** | 5 min | ✅ Yes | 30s | Easiest & Reliable |
| **Google Cloud Run** | 10 min | ✅ Yes | 5s | Best Performance |
| **PythonAnywhere** | 10 min | ✅ Limited | 2s | Python-Focused |
| **Railway** | 5 min | $5/mo | 10s | Modern & Fast |

**RECOMMENDATION: Start with Render** - Easiest setup, no credit card, most reliable.

---

## Troubleshooting

### "Build failed"
- Check requirements.txt has all dependencies
- Verify Python version is 3.8 or higher
- Look at deployment logs for specific error

### "API key not working"
- Verify key is correct at [aistudio.google.com](https://aistudio.google.com/app/apikey)
- Make sure environment variable name is exactly `GEMINI_API_KEY`
- Restart the app after adding variable

### "App won't start"
- Check "Start Command" is `gunicorn wsgi:app`
- Verify wsgi.py file exists
- Check logs in deployment dashboard

### "Website times out"
- Render free tier has resource limits
- Image analysis may take 10-30 seconds
- This is normal - increase timeout in frontend

---

## Getting Your API Key (Required)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with Google account (free)
3. Click "Create API Key"
4. Copy the key
5. Paste it in deployment platform's environment variables

**That's it! You have Gemini API access for free.** (Some usage limits apply, but fine for hobby projects)

---

## Testing Your Deployment

Once deployed, visit your URL and test:

1. ✅ Upload an image
2. ✅ Capture photo with camera
3. ✅ See analysis results
4. ✅ Check pricing calculation
5. ✅ View CO₂ savings

If all work, you're done! 🎉

---

## Important Notes

- **Free tier apps sleep after 15 min inactivity** (Render) - normal, will wake up when accessed
- **Keep your API key secret** - never commit it to git
- **Change SECRET_KEY** in production - generate random string with:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- **Monitor free tier usage** - most platforms show dashboard

---

## Need More Help?

- Render Support: https://render.com/docs
- Google Cloud Run: https://cloud.google.com/run/docs
- PythonAnywhere: https://help.pythonanywhere.com
- Railway: https://docs.railway.app
- **PythonAnywhere**: $5-35/month
- **AWS**: $5-30/month (highly variable)

---

## Next Steps

1. Choose your platform
2. Follow platform-specific instructions
3. Test thoroughly
4. Monitor performance
5. Set up error tracking
6. Configure custom domain
7. Enable HTTPS
8. Set up backups

For support: Document issues and check platform documentation.
