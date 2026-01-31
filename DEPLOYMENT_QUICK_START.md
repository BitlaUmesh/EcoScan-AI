# 5-Minute Free Deployment - EcoScan-AI

Choose ONE platform below and follow the steps. All are completely FREE.

---

## EASIEST: Render.com (No Credit Card)

1. **Sign up**: Go to [render.com](https://render.com) → "Sign Up with GitHub"
2. **New Web Service**: Dashboard → "New +" → "Web Service"
3. **Select repo**: Choose **EcoScan-AI**
4. **Configure**:
   - Name: `ecoscan-ai`
   - Environment: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn wsgi:app`
   - Instance: `Free`
5. **Add Variables**:
   - `GEMINI_API_KEY` = Your API key from [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
6. **Deploy**: Click "Create Web Service" and wait 3-5 minutes
7. **Done**: You get a live URL like `https://ecoscan-ai-xxxxx.onrender.com`

---

## FAST: Google Cloud Run (5 seconds cold start)

```bash
# 1. Install gcloud: https://cloud.google.com/sdk/docs/install
# 2. Then run:
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud run deploy ecoscan-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here
```

Done! You get URL like `https://ecoscan-ai-xxxxx.run.app`

---

## SIMPLE: PythonAnywhere

1. **Sign up**: [pythonanywhere.com](https://www.pythonanywhere.com) (free account)
2. **Upload files**: Files tab → Upload your project
3. **Create web app**: Web tab → Add new web app → Python 3.10 + Flask
4. **Point WSGI to** `wsgi.py`
5. **Set environment variables**: Add `GEMINI_API_KEY=your_key`
6. **Click Reload**: Done in 2 minutes

Your app: `https://yourusername.pythonanywhere.com`

---

## Get Your FREE API Key (5 seconds)

1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with Google
3. Click "Create API Key"
4. Copy it
5. Paste in platform environment variables

---

## Test Your Live App

Once deployed:
1. ✅ Upload an image
2. ✅ Capture with camera  
3. ✅ See analysis
4. ✅ Check pricing
5. ✅ Done!

---

## Troubleshooting

**"API key not working"**
→ Make sure variable is named exactly `GEMINI_API_KEY`

**"App won't start"**
→ Check logs in platform dashboard

**"Website times out"**  
→ Normal on free tier, may take 10-30 seconds

---

**That's it! Your app is live for FREE. 🚀**
