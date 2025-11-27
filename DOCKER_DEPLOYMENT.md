# 🐳 Docker Deployment Guide

## Why Use Docker?

✅ **Consistency**: Same environment locally and in production  
✅ **Portability**: Works on any platform (Windows, Mac, Linux)  
✅ **Isolation**: No conflicts with system dependencies  
✅ **Easy Deployment**: One command to build and run  
✅ **Better for Production**: Industry standard for cloud deployments

---

## 📦 Files Created

| File | Purpose |
|------|---------|
| `Dockerfile` | Instructions to build your Docker image |
| `.dockerignore` | Excludes unnecessary files from image |
| `docker-compose.yml` | Easy local development setup |
| `render.yaml` | Updated for Docker deployment |

---

## 🚀 Quick Start

### Prerequisites

Install Docker:
- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **Mac**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

---

## 🏠 Local Development with Docker

### Option 1: Using Docker Compose (Recommended)

```bash
# Make sure you have .env file with your API keys
cp .env.example .env
# Edit .env and add your real API keys

# Build and run
docker-compose up --build

# Your app will be available at: http://localhost:8000
```

**To stop**:
```bash
# Press Ctrl+C, then:
docker-compose down
```

### Option 2: Using Docker Commands Directly

```bash
# Build the image
docker build -t chainlit-ai-agent .

# Run the container
docker run -p 8000:8000 \
  --env-file .env \
  --name chainlit-app \
  chainlit-ai-agent

# Your app will be available at: http://localhost:8000
```

**To stop**:
```bash
docker stop chainlit-app
docker rm chainlit-app
```

---

## ☁️ Deploy to Render with Docker

### Method 1: Using render.yaml (Automated)

Your `render.yaml` is already configured for Docker deployment!

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Docker support"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com)
   - New → Blueprint
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Add environment variables:
     - `OPENAI_API_KEY`
     - `TAVILY_API_KEY`
     - `ALPHAVANTAGE_API_KEY`
   - Click "Apply"

3. **Done!** Render will:
   - Build your Docker image
   - Deploy the container
   - Your app will be live in ~5-10 minutes

### Method 2: Manual Docker Deployment

1. **Create Web Service on Render**:
   - New → Web Service
   - Connect your GitHub repo

2. **Configure**:
   - **Environment**: Select "Docker"
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `./`

3. **Add Environment Variables**:
   - `OPENAI_API_KEY`
   - `TAVILY_API_KEY`
   - `ALPHAVANTAGE_API_KEY`

4. **Deploy**: Click "Create Web Service"

---

## 🔧 Docker Commands Cheat Sheet

### Build & Run
```bash
# Build image
docker build -t chainlit-ai-agent .

# Run container
docker run -p 8000:8000 --env-file .env chainlit-ai-agent

# Run in background (detached)
docker run -d -p 8000:8000 --env-file .env --name chainlit-app chainlit-ai-agent

# Run with volume mount (for development)
docker run -p 8000:8000 --env-file .env -v $(pwd):/app chainlit-ai-agent
```

### Manage Containers
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop chainlit-app

# Remove container
docker rm chainlit-app

# View logs
docker logs chainlit-app

# Follow logs (real-time)
docker logs -f chainlit-app
```

### Manage Images
```bash
# List images
docker images

# Remove image
docker rmi chainlit-ai-agent

# Remove unused images
docker image prune
```

### Docker Compose
```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache
```

---

## 🐛 Troubleshooting

### Container Exits Immediately

**Check logs**:
```bash
docker logs chainlit-app
```

**Common causes**:
- Missing environment variables
- Port already in use
- Syntax error in code

### Port Already in Use

**Find and kill process**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

**Or use different port**:
```bash
docker run -p 8080:8000 --env-file .env chainlit-ai-agent
# Access at http://localhost:8080
```

### Build Fails

**Clear Docker cache**:
```bash
docker builder prune
docker-compose build --no-cache
```

### Environment Variables Not Working

**Verify .env file exists**:
```bash
ls -la .env
```

**Check environment variables in container**:
```bash
docker exec chainlit-app env
```

---

## 📊 Image Size Optimization

Current Dockerfile uses `python:3.11-slim` for smaller size.

**Check image size**:
```bash
docker images chainlit-ai-agent
```

**Further optimization** (optional):
- Use multi-stage builds
- Use Alpine Linux base image
- Remove unnecessary dependencies

---

## 🔒 Security Best Practices

✅ **Never commit `.env` file** - Already in `.gitignore` and `.dockerignore`  
✅ **Use environment variables** - Not hardcoded in Dockerfile  
✅ **Run as non-root user** (optional enhancement):

Add to Dockerfile:
```dockerfile
RUN useradd -m -u 1000 chainlit && chown -R chainlit:chainlit /app
USER chainlit
```

✅ **Scan for vulnerabilities**:
```bash
docker scan chainlit-ai-agent
```

---

## 🚀 Production Deployment Options

### 1. Render (Recommended for this project)
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy Docker support
- ✅ GitHub integration

### 2. Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### 4. Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/chainlit-ai-agent

# Deploy
gcloud run deploy chainlit-ai-agent \
  --image gcr.io/PROJECT_ID/chainlit-ai-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 5. AWS ECS/Fargate
- Use AWS Console or CLI
- Push image to ECR
- Create ECS task definition
- Deploy to Fargate

---

## 📈 Monitoring & Logs

### View Logs
```bash
# Docker
docker logs -f chainlit-app

# Docker Compose
docker-compose logs -f

# Render
# View in Render Dashboard → Your Service → Logs
```

### Health Check
```bash
# Check if container is healthy
docker ps

# Manual health check
curl http://localhost:8000
```

---

## 🎯 Next Steps

1. **Test Locally**:
   ```bash
   docker-compose up --build
   ```

2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Docker support for deployment"
   git push origin main
   ```

3. **Deploy to Render**:
   - Follow "Deploy to Render with Docker" section above

4. **Monitor**: Check logs and ensure app is running correctly

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Render Docker Deployment](https://render.com/docs/docker)
- [Chainlit Documentation](https://docs.chainlit.io/)
- [Best Practices for Python Docker Images](https://docs.docker.com/language/python/build-images/)

---

**Ready to containerize?** Start with `docker-compose up --build` and you're good to go! 🐳
