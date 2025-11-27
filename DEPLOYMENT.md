# Deployment Guide for Chainlit AI Agent

## Deploying to Render

### Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)
- Your API keys ready (keep them SECRET!):
  - `OPENAI_API_KEY`
  - `TAVILY_API_KEY`
  - `ALPHA_VANTAGE_API_KEY`

### 🔒 IMPORTANT: Security First!

**NEVER commit your `.env` file to Git!**

Your `.gitignore` is already configured to prevent this, but double-check:
```bash
git status
# Make sure .env is NOT listed (only .env.example should be tracked)
```

### Step-by-Step Deployment

#### 1. Prepare Your Local Environment

First, ensure your local `.env` file exists (this stays on your machine only):

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your REAL API keys
# (Use notepad, VS Code, or any text editor)
```

Your `.env` should look like:
```bash
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY
TAVILY_API_KEY=tvly-YOUR_ACTUAL_KEY
ALPHAVANTAGE_API_KEY=YOUR_ACTUAL_KEY
```

#### 2. Push Your Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files (your .gitignore will protect .env)
git add .

# Verify .env is NOT being committed
git status
# You should see .env.example but NOT .env

# Commit your changes
git commit -m "Ready for deployment - API keys secured"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

#### 3. Deploy on Render

1. **Sign up/Login** to [Render](https://render.com)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure the Service**
   - **Name**: `chainlit-ai-agent` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `chainlit run app.py --host 0.0.0.0 --port $PORT`
   - **Plan**: Select "Free" tier for testing

4. **🔑 Add Environment Variables (CRITICAL STEP!)**
   
   Click "Advanced" → Scroll to "Environment Variables" → Click "Add Environment Variable"
   
   Add these **one by one**:
   
   | Key | Value |
   |-----|-------|
   | `OPENAI_API_KEY` | Your actual OpenAI API key |
   | `TAVILY_API_KEY` | Your actual Tavily API key |
   | `ALPHAVANTAGE_API_KEY` | Your actual Alpha Vantage API key |

   **Important**: 
   - Copy-paste your REAL keys here (not the placeholders!)
   - These are stored securely by Render
   - They're never visible in your code or Git repository

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete (5-10 minutes)
   - Your app will be live at: `https://your-service-name.onrender.com`


### Alternative: Using render.yaml (Blueprint)

If you prefer automated deployment:

1. Push your code with the `render.yaml` file to GitHub
2. On Render dashboard, click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml` and configure everything
5. You'll only need to add your API keys in the environment variables section

### Important Notes

⚠️ **Free Tier Limitations**:
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds to wake up
- 750 hours/month of runtime (sufficient for testing)

💡 **Upgrade to Paid Plan** ($7/month) for:
- Always-on service (no spin-down)
- Faster performance
- Custom domains

### Troubleshooting

**Build Fails**:
- Check that `requirements.txt` is complete
- Verify Python version compatibility

**App Crashes on Start**:
- Ensure all environment variables are set correctly
- Check logs in Render dashboard

**WebSocket Connection Issues**:
- Render supports WebSockets by default
- Ensure you're using HTTPS (not HTTP) to access your app

### Monitoring

- View logs: Render Dashboard → Your Service → Logs
- Check metrics: Render Dashboard → Your Service → Metrics

---

## Alternative Deployment Options

### Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Select "Docker" as the SDK
3. Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
```

4. Push your code to the Space repository

---

## Testing Locally Before Deployment

Always test your app works correctly:

```bash
# Activate your virtual environment
# Windows:
.venv\Scripts\activate

# Run the app
chainlit run app.py

# Test all features:
# - Wikipedia search
# - Tavily search
# - Stock price lookup
# - Chat history
```

---

## Security Best Practices

✅ **Never commit API keys** to GitHub
✅ Use `.env` file locally (already in `.gitignore`)
✅ Set environment variables in Render dashboard
✅ Rotate API keys periodically
✅ Monitor usage on API provider dashboards

---

## Support

If you encounter issues:
- Render Docs: https://render.com/docs
- Chainlit Docs: https://docs.chainlit.io
- Check Render community forum
