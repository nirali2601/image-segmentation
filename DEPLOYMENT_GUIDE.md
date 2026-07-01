# Vercel Deployment Guide

## Quick Start

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Deploy Your Project
```bash
# Navigate to your project directory
cd image-segmentation-tool

# Deploy to Vercel
vercel
```

### Step 3: Follow the Prompts
- **Project name:** Press Enter for default or type custom name
- **Link to existing project?** Select "No" for first deployment
- **Clone from a GitHub repository?** Select "No"
- **Directory:** Press Enter (default)
- **Override settings:** Select "No"

### Step 4: Access Your App
Your application will be deployed and available at:
```
https://your-project-name.vercel.app
```

---

## Testing Your Deployment

### Health Check
```bash
curl https://your-project-name.vercel.app/health
```

### Segment an Image
```bash
curl -F "image=@image.jpg" -F "threshold=0.5" \
  https://your-project-name.vercel.app/segment
```

### View API Documentation
```bash
curl https://your-project-name.vercel.app/
```

---

## Important Considerations

### ⚠️ Vercel Python Size Limits
- **Max function size:** 250MB uncompressed
- **PyTorch + TorchVision:** ~500MB+ (may exceed limit)
- **Workaround:** Use Railway or Render for better Python support

### Cold Start Times
Vercel serverless functions may have:
- **First request:** 10-30 seconds (model loading)
- **Subsequent requests:** 1-5 seconds (much faster)

---

## Better Alternatives for This Project

### 🚀 Railway (Recommended)
**Best for:** ML projects with large dependencies

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```
- Higher memory limits
- Better Python support
- Generous free tier

### 🎨 Render
**Best for:** Simple Python web apps

1. Connect GitHub repository at [render.com](https://render.com)
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn main:app`
4. Deploy with one click

### 🦸 Heroku
**Best for:** Production-grade deployments

```bash
heroku login
heroku create your-app-name
git push heroku main
```

---

## Troubleshooting

### Error: "Function too large"
**Solution:** Use Railway or Render instead

### Model loading timeout
**Solution:** Increase timeout in `vercel.json`
```json
"functions": {
  "api/*.py": {
    "maxDuration": 120
  }
}
```

### No module named 'torch'
**Solution:** Ensure `requirements.txt` is properly configured

---

## Next Steps

1. Test locally first: `python main.py`
2. Choose deployment platform based on your needs
3. For production, use Railway or Render
4. Monitor your app's performance and costs

Happy deploying! 🚀
