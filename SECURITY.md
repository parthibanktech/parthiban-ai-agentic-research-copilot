# 🔒 Security Guide: API Key Management

## ⚠️ CRITICAL: Never Expose API Keys!

Your API keys are like passwords - they should **NEVER** be:
- ❌ Hardcoded in your source code
- ❌ Committed to Git/GitHub
- ❌ Shared in screenshots or logs
- ❌ Included in `.env.example` with real values

---

## ✅ Secure Setup for Local Development

### 1. Create Your Local `.env` File

```bash
# Copy the example file
cp .env.example .env
```

### 2. Add Your REAL Keys to `.env` (NOT .env.example!)

Open `.env` and add your actual keys:

```bash
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
TAVILY_API_KEY=tvly-YOUR_ACTUAL_KEY_HERE
ALPHAVANTAGE_API_KEY=YOUR_ACTUAL_KEY_HERE
```

### 3. Verify `.env` is in `.gitignore`

Check that `.gitignore` contains:
```
.env
.env.local
```

This ensures your `.env` file is **never** committed to Git.

---

## 🚀 Secure Setup for Render Deployment

### Option 1: Environment Variables in Render Dashboard (Recommended)

1. **Deploy your code WITHOUT the `.env` file**
   - The `.env` file stays on your local machine only
   - Never commit it to GitHub

2. **Add Environment Variables in Render**:
   - Go to your Render service dashboard
   - Click "Environment" tab
   - Add each key manually:
     - `OPENAI_API_KEY` = `your_actual_openai_key`
     - `TAVILY_API_KEY` = `your_actual_tavily_key`
     - `ALPHAVANTAGE_API_KEY` = `your_actual_alphavantage_key`

3. **Redeploy** (if needed)
   - Render will automatically use these environment variables
   - Your code uses `os.getenv()` which works both locally and on Render

### Option 2: Render Secret Files (Advanced)

For even more security, use Render's Secret Files feature:

1. In Render Dashboard → Your Service → "Environment"
2. Scroll to "Secret Files"
3. Add a file: `.env`
4. Content:
   ```
   OPENAI_API_KEY=your_key
   TAVILY_API_KEY=your_key
   ALPHAVANTAGE_API_KEY=your_key
   ```
5. This file is encrypted and only available at runtime

---

## 🔍 How Your Code Loads API Keys Securely

Your application already uses the secure approach:

### In `tools.py`:
```python
api_key = os.getenv("ALPHAVANTAGE_API_KEY")
if not api_key:
    return "Error: ALPHAVANTAGE_API_KEY not found in environment variables."
```

### In `agent.py`:
```python
llm = ChatOpenAI(model="gpt-4o", temperature=0)
# ChatOpenAI automatically reads OPENAI_API_KEY from environment
```

### How it works:
1. **Locally**: `python-dotenv` loads `.env` file → `os.getenv()` reads it
2. **On Render**: Render injects environment variables → `os.getenv()` reads them
3. **No code changes needed!** Same code works everywhere

---

## 🛡️ Security Checklist Before Deployment

- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` contains only placeholder values (no real keys)
- [ ] Real API keys are only in your local `.env` file
- [ ] API keys are added to Render's Environment Variables
- [ ] You've verified `.env` is NOT in your Git repository:
  ```bash
  git status
  # .env should NOT appear in the list
  ```

---

## 🚨 What to Do If You Accidentally Exposed Keys

If you accidentally committed API keys to Git:

### 1. **Rotate Your Keys Immediately**
   - **OpenAI**: https://platform.openai.com/api-keys → Revoke & Create New
   - **Tavily**: https://app.tavily.com/home → API Keys → Regenerate
   - **Alpha Vantage**: https://www.alphavantage.co/support/#api-key → Request new key

### 2. **Remove from Git History**
   ```bash
   # Remove the file from Git history (use with caution!)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push to remote
   git push origin --force --all
   ```

### 3. **Update Your Keys**
   - Update local `.env` with new keys
   - Update Render environment variables with new keys

---

## 📊 Monitoring API Usage

Regularly check your API usage to detect unauthorized access:

- **OpenAI**: https://platform.openai.com/usage
- **Tavily**: https://app.tavily.com/home
- **Alpha Vantage**: Check email for usage alerts

Set up usage alerts and spending limits where available.

---

## 🎯 Best Practices Summary

1. ✅ Use environment variables (`os.getenv()`)
2. ✅ Keep `.env` in `.gitignore`
3. ✅ Use `.env.example` with placeholders only
4. ✅ Add real keys in Render dashboard
5. ✅ Rotate keys periodically
6. ✅ Monitor API usage
7. ✅ Never share keys in chat, screenshots, or logs

---

## 📚 Additional Resources

- [Render Environment Variables Docs](https://render.com/docs/environment-variables)
- [OpenAI API Key Best Practices](https://platform.openai.com/docs/guides/production-best-practices/api-keys)
- [12-Factor App: Config](https://12factor.net/config)

---

**Remember**: Your API keys are YOUR responsibility. Treat them like passwords! 🔐
