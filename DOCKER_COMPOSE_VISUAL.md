# 🎨 Docker Compose Visual Guide

## 📊 How Docker Compose Works

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Project Directory (c:\study\AI\Agent\first_agent)   │  │
│  │                                                       │  │
│  │  📄 docker-compose.yml  ← Configuration file         │  │
│  │  📄 Dockerfile          ← Build instructions         │  │
│  │  📄 .env                ← Your API keys (secret!)    │  │
│  │  📄 app.py              ← Your code                  │  │
│  │  📄 agent.py            ← Your code                  │  │
│  │  📄 tools.py            ← Your code                  │  │
│  │  📄 requirements.txt    ← Dependencies               │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           │ docker-compose up --build       │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           DOCKER COMPOSE PROCESS                     │  │
│  │                                                       │  │
│  │  1. Reads docker-compose.yml                         │  │
│  │  2. Reads .env file                                  │  │
│  │  3. Builds image using Dockerfile                    │  │
│  │  4. Creates container                                │  │
│  │  5. Injects environment variables                    │  │
│  │  6. Mounts volumes (if specified)                    │  │
│  │  7. Maps ports                                       │  │
│  │  8. Starts container                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         DOCKER CONTAINER (chainlit-ai-agent)         │  │
│  │                                                       │  │
│  │  🐍 Python 3.11                                      │  │
│  │  📦 Installed packages (from requirements.txt)       │  │
│  │  🔑 Environment variables (from .env)                │  │
│  │  📁 Your app code (from volumes or baked in)         │  │
│  │  🚀 Running: chainlit run app.py                     │  │
│  │  🌐 Listening on port 8000                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           │ Port mapping: 8000:8000         │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         YOUR BROWSER                                 │  │
│  │                                                       │  │
│  │  🌐 http://localhost:8000                            │  │
│  │                                                       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  💬 Chainlit Chat Interface                    │  │  │
│  │  │                                                 │  │  │
│  │  │  User: What's the price of Apple stock?        │  │  │
│  │  │  AI: Let me check...                           │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

```
┌─────────────┐
│   .env      │  Your API keys
│   file      │  (OPENAI_API_KEY, etc.)
└──────┬──────┘
       │
       │ Read by docker-compose
       ▼
┌─────────────────────┐
│ docker-compose.yml  │  Configuration
│                     │  (ports, volumes, etc.)
└──────┬──────────────┘
       │
       │ Instructs Docker
       ▼
┌─────────────────────┐
│   Dockerfile        │  Build instructions
│                     │  (install Python, packages, etc.)
└──────┬──────────────┘
       │
       │ Creates
       ▼
┌─────────────────────┐
│  Docker Image       │  Snapshot of your app
│  (chainlit-ai-agent)│  (ready to run)
└──────┬──────────────┘
       │
       │ Runs as
       ▼
┌─────────────────────┐
│  Docker Container   │  Running instance
│  (chainlit-ai-agent)│  (your app is live!)
└──────┬──────────────┘
       │
       │ Accessible via
       ▼
┌─────────────────────┐
│  localhost:8000     │  Your browser
└─────────────────────┘
```

---

## 🎯 Command Flow

### **Starting Up**

```
You type: docker-compose up --build
           │
           ├─→ Step 1: Read docker-compose.yml
           │           ✓ Found service: chainlit-app
           │
           ├─→ Step 2: Read .env file
           │           ✓ Loaded API keys
           │
           ├─→ Step 3: Build Docker image
           │           ├─→ Read Dockerfile
           │           ├─→ Download Python 3.11
           │           ├─→ Install dependencies
           │           ├─→ Copy app code
           │           ✓ Image built: chainlit-ai-agent
           │
           ├─→ Step 4: Create container
           │           ├─→ Name: chainlit-ai-agent
           │           ├─→ Port: 8000:8000
           │           ├─→ Env vars: Injected
           │           ├─→ Volumes: Mounted
           │           ✓ Container created
           │
           ├─→ Step 5: Start container
           │           ├─→ Run: chainlit run app.py
           │           ├─→ Wait for startup (40s grace period)
           │           ├─→ Health check: OK
           │           ✓ Container running
           │
           └─→ Output: "Chainlit is running on http://localhost:8000"
```

### **Stopping**

```
You type: Ctrl+C
           │
           ├─→ Sends stop signal to container
           │   ✓ Container stopped gracefully
           │
You type: docker-compose down
           │
           ├─→ Stop container (if still running)
           ├─→ Remove container
           ├─→ Remove network
           └─→ ✓ Cleanup complete
```

---

## 🏗️ File Relationships

```
┌─────────────────────────────────────────────────────────┐
│  DEVELOPMENT (Your Computer)                            │
│                                                         │
│  docker-compose.yml ─────┐                             │
│         │                │                             │
│         │ references     │ reads                       │
│         ▼                ▼                             │
│    Dockerfile         .env                             │
│         │                │                             │
│         │ copies         │ provides                    │
│         ▼                ▼                             │
│    app.py, agent.py  API keys                          │
│    tools.py, etc.                                      │
└─────────────────────────────────────────────────────────┘
                           │
                           │ docker-compose up --build
                           ▼
┌─────────────────────────────────────────────────────────┐
│  DOCKER CONTAINER                                       │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  /app/                                          │   │
│  │    ├── app.py                                   │   │
│  │    ├── agent.py                                 │   │
│  │    ├── tools.py                                 │   │
│  │    ├── requirements.txt                         │   │
│  │    └── ...                                      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Environment Variables:                                 │
│    OPENAI_API_KEY=sk-proj-xxx                          │
│    TAVILY_API_KEY=tvly-xxx                             │
│    ALPHAVANTAGE_API_KEY=xxx                            │
│                                                         │
│  Running Process:                                       │
│    chainlit run app.py --host 0.0.0.0 --port 8000      │
└─────────────────────────────────────────────────────────┘
```

---

## 🔀 Development vs Production Mode

### **Development Mode** (Current Setup)

```
┌─────────────────────────────────────────────────────────┐
│  YOUR COMPUTER                                          │
│                                                         │
│  ┌─────────────────┐                                   │
│  │  app.py         │ ◄─────┐                           │
│  │  (you edit)     │       │                           │
│  └─────────────────┘       │                           │
│         │                  │                           │
│         │ Volume mount     │ Changes reflect           │
│         │ (.:/app)         │ immediately!              │
│         ▼                  │                           │
│  ┌─────────────────────────┴───────────────────────┐   │
│  │  DOCKER CONTAINER                               │   │
│  │                                                 │   │
│  │  /app/app.py (same file!)                      │   │
│  │  Chainlit auto-reloads on changes              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

Benefits:
✅ Edit code → See changes immediately
✅ No rebuild needed
✅ Fast development cycle
```

### **Production Mode** (No Volumes)

```
┌─────────────────────────────────────────────────────────┐
│  YOUR COMPUTER                                          │
│                                                         │
│  ┌─────────────────┐                                   │
│  │  app.py         │                                   │
│  │  (source code)  │                                   │
│  └─────────────────┘                                   │
│         │                                               │
│         │ Copied during build                          │
│         │ (baked into image)                           │
│         ▼                                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │  DOCKER IMAGE                                   │   │
│  │  Contains snapshot of code                      │   │
│  └─────────────────────────────────────────────────┘   │
│         │                                               │
│         │ Runs as                                      │
│         ▼                                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │  DOCKER CONTAINER                               │   │
│  │                                                 │   │
│  │  /app/app.py (copy, not linked)                │   │
│  │  Code is frozen in image                       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

Benefits:
✅ Consistent, reproducible
✅ Smaller attack surface
✅ Better for production
```

---

## 🎮 Interactive Example

Let's walk through what happens when you run `docker-compose up --build`:

### **Terminal Output Explained**

```bash
$ docker-compose up --build

# Step 1: Building
Building chainlit-app
[+] Building 45.2s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/6] FROM docker.io/library/python:3.11-slim
 => [2/6] WORKDIR /app
 => [3/6] COPY requirements.txt .
 => [4/6] RUN pip install --no-cache-dir -r requirements.txt
 => [5/6] COPY . .
 => [6/6] RUN mkdir -p .chainlit .files
 => exporting to image
 => => naming to docker.io/library/first_agent_chainlit-app

# Step 2: Creating container
Creating chainlit-ai-agent ... done

# Step 3: Attaching to container
Attaching to chainlit-ai-agent

# Step 4: Your app starts
chainlit-ai-agent | 2025-11-27 11:12:00 - Loaded .env file
chainlit-ai-agent | 2025-11-27 11:12:01 - Starting Chainlit...
chainlit-ai-agent | 2025-11-27 11:12:02 - Your app is available at http://localhost:8000

# Step 5: Health check passes
chainlit-ai-agent | 2025-11-27 11:12:42 - Health check: OK

# Now you can use your app!
```

---

## 🎯 Quick Reference

### **Most Common Commands**

| What you want | Command |
|---------------|---------|
| Start app | `docker-compose up --build` |
| Start in background | `docker-compose up -d` |
| Stop app | `Ctrl+C` then `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Restart | `docker-compose restart` |
| Fresh start | `docker-compose down -v && docker-compose up --build` |

### **File Purposes**

| File | Used by | Purpose |
|------|---------|---------|
| `docker-compose.yml` | Docker Compose | Runtime configuration |
| `Dockerfile` | Docker | Build instructions |
| `.env` | Docker Compose | Your API keys |
| `.dockerignore` | Docker | Build exclusions |

---

## 🎓 Summary

**Docker Compose** is your **one-stop shop** for running your Dockerized app:

1. **Reads** `docker-compose.yml` for configuration
2. **Loads** `.env` for secrets
3. **Builds** image using `Dockerfile`
4. **Creates** and **starts** container
5. **Maps** ports so you can access it
6. **Monitors** health and auto-restarts if needed

**One command to rule them all**: `docker-compose up --build` 🚀

---

**Ready to try it?** Make sure you have a `.env` file with your API keys, then run:

```bash
docker-compose up --build
```

Visit http://localhost:8000 and chat with your AI agent! 🤖
