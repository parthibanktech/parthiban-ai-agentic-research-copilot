# 🐳 Docker Quick Reference

## 🚀 One-Command Deployment

### Local Development
```bash
docker-compose up --build
```
**Access**: http://localhost:8000

### Stop
```bash
Ctrl+C
docker-compose down
```

---

## ☁️ Deploy to Render (Docker)

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Docker deployment"
git push origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. New → Blueprint
3. Connect GitHub repo
4. Add environment variables:
   - `OPENAI_API_KEY`
   - `TAVILY_API_KEY`
   - `ALPHAVANTAGE_API_KEY`
5. Click "Apply"

**Done!** Your app will be live in ~5-10 minutes 🎉

---

## 📋 Docker vs Native Deployment

| Feature | Docker | Native Python |
|---------|--------|---------------|
| **Consistency** | ✅ Same everywhere | ⚠️ May vary |
| **Dependencies** | ✅ Isolated | ⚠️ System-wide |
| **Portability** | ✅ Run anywhere | ⚠️ Platform-specific |
| **Setup Time** | ⚠️ Slightly longer | ✅ Faster |
| **Production** | ✅ Industry standard | ⚠️ Less common |
| **Debugging** | ⚠️ Requires Docker knowledge | ✅ Easier |

**Recommendation**: Use Docker for production, either works for development.

---

## 🔧 Common Commands

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild from scratch
docker-compose build --no-cache

# Remove everything
docker-compose down -v --rmi all
```

---

## 🐛 Quick Troubleshooting

### "Port already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
docker-compose up -p 8080:8000
```

### "Container exits immediately"
```bash
docker-compose logs
# Check for errors in output
```

### "Can't connect to Docker daemon"
- Make sure Docker Desktop is running
- Restart Docker Desktop

---

## 📚 Full Documentation

- **Docker Guide**: `DOCKER_DEPLOYMENT.md`
- **Security**: `SECURITY.md`
- **Deployment**: `DEPLOYMENT.md`

---

**Ready?** Run `docker-compose up --build` and you're live! 🚀
