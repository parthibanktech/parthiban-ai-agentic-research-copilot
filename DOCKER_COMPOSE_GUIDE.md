# 🐳 Docker Compose Usage Guide

## 📖 What is Docker Compose?

**Docker Compose** is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services, networks, and volumes.

### **The Problem It Solves**

**Without Docker Compose**, you'd need to run:
```bash
# Build the image
docker build -t chainlit-ai-agent .

# Run the container with all options
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-proj-xxx \
  -e TAVILY_API_KEY=tvly-xxx \
  -e ALPHAVANTAGE_API_KEY=xxx \
  -v $(pwd):/app \
  --name chainlit-app \
  --restart unless-stopped \
  chainlit-ai-agent
```

**With Docker Compose**, you just run:
```bash
docker-compose up --build
```

---

## 📋 Your `docker-compose.yml` Explained

Let's break down your file section by section:

### **1. Version**
```yaml
version: '3.8'
```
- Specifies Docker Compose file format version
- `3.8` is a stable, modern version
- Determines which features are available

---

### **2. Services**
```yaml
services:
  chainlit-app:
```
- Defines the containers to run
- `chainlit-app` is the service name (you can have multiple services)
- Each service becomes one container

---

### **3. Build Configuration**
```yaml
build:
  context: .
  dockerfile: Dockerfile
```
- **`context: .`** - Build from current directory
- **`dockerfile: Dockerfile`** - Use this Dockerfile
- Tells Docker Compose how to build your image

---

### **4. Container Name**
```yaml
container_name: chainlit-ai-agent
```
- Names the running container
- Without this, Docker generates random names like `first_agent_chainlit-app_1`
- Makes it easier to reference: `docker logs chainlit-ai-agent`

---

### **5. Port Mapping**
```yaml
ports:
  - "8000:8000"
```
- **Format**: `"HOST_PORT:CONTAINER_PORT"`
- **`8000:8000`** means:
  - Container exposes port 8000
  - Maps to port 8000 on your computer
  - Access at: `http://localhost:8000`

**Example variations**:
```yaml
ports:
  - "8080:8000"  # Access at http://localhost:8080
  - "80:8000"    # Access at http://localhost
```

---

### **6. Environment Variables**
```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - TAVILY_API_KEY=${TAVILY_API_KEY}
  - ALPHAVANTAGE_API_KEY=${ALPHAVANTAGE_API_KEY}
  - PORT=8000
```
- Sets environment variables inside the container
- **`${VARIABLE_NAME}`** reads from your `.env` file
- These are passed to your Python app via `os.getenv()`

**How it works**:
```
.env file → Docker Compose → Container → Your Python app
```

---

### **7. Environment File**
```yaml
env_file:
  - .env
```
- Automatically loads all variables from `.env` file
- Simpler than listing each variable individually
- **Important**: `.env` must exist in the same directory

---

### **8. Volumes (Development Mode)**
```yaml
volumes:
  - .:/app
  - /app/__pycache__
  - /app/.chainlit
```

**What this does**:
- **`.:/app`** - Mounts current directory to `/app` in container
  - **Benefit**: Changes to code are reflected immediately (hot reload!)
  - **Use case**: Development only
  
- **`/app/__pycache__`** - Excludes Python cache from mount
  - Prevents conflicts between host and container

- **`/app/.chainlit`** - Excludes Chainlit data from mount
  - Keeps runtime data separate

**Development vs Production**:
```yaml
# Development (with volumes) - Code changes reflect immediately
volumes:
  - .:/app

# Production (no volumes) - Code is baked into image
# volumes: []  # Comment out or remove
```

---

### **9. Restart Policy**
```yaml
restart: unless-stopped
```

**Options**:
- **`no`** - Never restart (default)
- **`always`** - Always restart if stopped
- **`on-failure`** - Restart only if container exits with error
- **`unless-stopped`** - Always restart unless manually stopped

**Your setting** (`unless-stopped`):
- Container restarts automatically if it crashes
- Won't restart if you manually stop it with `docker-compose down`
- Good for development and production

---

### **10. Health Check**
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000', timeout=5)"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**What each option means**:

| Option | Value | Meaning |
|--------|-------|---------|
| `test` | Python command | How to check if app is healthy |
| `interval` | 30s | Check every 30 seconds |
| `timeout` | 10s | Wait max 10 seconds for response |
| `retries` | 3 | Try 3 times before marking unhealthy |
| `start_period` | 40s | Grace period on startup |

**How it works**:
1. Container starts
2. Waits 40 seconds (start_period)
3. Every 30 seconds, runs the test command
4. If test fails 3 times in a row → marks container as unhealthy
5. Docker can auto-restart unhealthy containers

**Check health status**:
```bash
docker ps
# Look for "healthy" or "unhealthy" in STATUS column
```

---

## 🚀 Common Docker Compose Commands

### **Basic Commands**

```bash
# Build and start containers
docker-compose up --build

# Start in background (detached mode)
docker-compose up -d

# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f chainlit-app
```

### **Build Commands**

```bash
# Build without starting
docker-compose build

# Build without cache (fresh build)
docker-compose build --no-cache

# Build and start
docker-compose up --build
```

### **Management Commands**

```bash
# List running services
docker-compose ps

# Restart services
docker-compose restart

# Stop services (without removing)
docker-compose stop

# Start stopped services
docker-compose start

# Execute command in running container
docker-compose exec chainlit-app bash

# View resource usage
docker-compose top
```

### **Cleanup Commands**

```bash
# Remove stopped containers
docker-compose rm

# Remove everything (containers, networks, volumes)
docker-compose down -v --rmi all

# Remove orphaned containers
docker-compose down --remove-orphans
```

---

## 🎯 Common Use Cases

### **Use Case 1: Local Development**

**Scenario**: You're developing and want code changes to reflect immediately.

**Setup**: Use the current `docker-compose.yml` (with volumes)

```bash
# Start development environment
docker-compose up --build

# Edit your code (app.py, agent.py, tools.py)
# Changes are reflected immediately!

# View logs
docker-compose logs -f

# Stop when done
Ctrl+C
docker-compose down
```

---

### **Use Case 2: Testing Production Build**

**Scenario**: You want to test how your app will run in production.

**Setup**: Comment out the volumes section

```yaml
# volumes:
#   - .:/app
#   - /app/__pycache__
#   - /app/.chainlit
```

```bash
# Build production-like image
docker-compose build --no-cache

# Run
docker-compose up

# Test at http://localhost:8000
```

---

### **Use Case 3: Running in Background**

**Scenario**: You want the app running while you do other work.

```bash
# Start in background
docker-compose up -d

# Check status
docker-compose ps

# View logs when needed
docker-compose logs -f

# Stop when done
docker-compose down
```

---

### **Use Case 4: Debugging Issues**

**Scenario**: Container keeps crashing, need to investigate.

```bash
# View logs
docker-compose logs

# Check last 50 lines
docker-compose logs --tail=50

# Follow logs in real-time
docker-compose logs -f

# Execute shell in running container
docker-compose exec chainlit-app bash

# Inside container, you can:
# - Check environment variables: env
# - Test Python: python
# - Check files: ls -la
# - Run commands: chainlit run app.py
```

---

### **Use Case 5: Fresh Start**

**Scenario**: Something's broken, want to start completely fresh.

```bash
# Stop and remove everything
docker-compose down -v --rmi all

# Remove Docker cache
docker builder prune -a

# Rebuild from scratch
docker-compose up --build
```

---

## 🔧 Customizing Your `docker-compose.yml`

### **Change Port**

```yaml
ports:
  - "8080:8000"  # Access at http://localhost:8080
```

### **Add Environment Variables**

```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - TAVILY_API_KEY=${TAVILY_API_KEY}
  - ALPHAVANTAGE_API_KEY=${ALPHAVANTAGE_API_KEY}
  - PORT=8000
  - DEBUG=true              # Add custom variable
  - LOG_LEVEL=info          # Add another
```

### **Add Another Service (e.g., Database)**

```yaml
services:
  chainlit-app:
    # ... existing config ...
    depends_on:
      - postgres
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: chainlit_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### **Add Resource Limits**

```yaml
services:
  chainlit-app:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 🐛 Troubleshooting

### **Problem: "Cannot connect to Docker daemon"**

**Solution**:
```bash
# Make sure Docker Desktop is running
# Restart Docker Desktop if needed
```

---

### **Problem: "Port 8000 is already in use"**

**Solution 1**: Stop the conflicting process
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# You have chainlit running on port 8000!
# Stop it first: Ctrl+C in that terminal
```

**Solution 2**: Use different port
```yaml
ports:
  - "8080:8000"  # Use port 8080 instead
```

---

### **Problem: "Environment variables not working"**

**Solution**:
```bash
# 1. Check .env file exists
ls .env

# 2. Verify .env file has correct format
cat .env
# Should be:
# OPENAI_API_KEY=your_key
# (no quotes, no spaces around =)

# 3. Rebuild
docker-compose down
docker-compose up --build
```

---

### **Problem: "Container exits immediately"**

**Solution**:
```bash
# Check logs for errors
docker-compose logs

# Common causes:
# - Missing .env file
# - Syntax error in code
# - Missing dependencies
```

---

### **Problem: "Changes to code not reflecting"**

**Solution**:
```bash
# Make sure volumes are enabled in docker-compose.yml
# Should have:
volumes:
  - .:/app

# If still not working, rebuild:
docker-compose down
docker-compose up --build
```

---

## 📊 Docker Compose vs Dockerfile

| Aspect | Dockerfile | docker-compose.yml |
|--------|------------|-------------------|
| **Purpose** | Define image | Define services |
| **Contains** | Build instructions | Runtime configuration |
| **Creates** | Docker image | Running containers |
| **Used for** | Building | Running |
| **Command** | `docker build` | `docker-compose up` |

**Analogy**:
- **Dockerfile** = Recipe for making a cake
- **docker-compose.yml** = Instructions for serving the cake

---

## 🎯 Best Practices

### ✅ **Do's**

1. **Use `.env` file** for sensitive data
2. **Use volumes** for development
3. **Remove volumes** for production
4. **Add health checks** for reliability
5. **Use specific versions** (`version: '3.8'`)
6. **Name your containers** for easy reference
7. **Set restart policies** for resilience

### ❌ **Don'ts**

1. **Don't hardcode secrets** in docker-compose.yml
2. **Don't commit `.env`** to Git
3. **Don't use `latest` tags** in production
4. **Don't run as root** (add `user:` directive)
5. **Don't expose unnecessary ports**

---

## 🚀 Quick Start Workflow

```bash
# 1. Make sure .env file exists with your API keys
cp .env.example .env
# Edit .env and add your real keys

# 2. Build and start
docker-compose up --build

# 3. Access your app
# Open browser: http://localhost:8000

# 4. View logs (in another terminal)
docker-compose logs -f

# 5. Stop when done
# Press Ctrl+C in the first terminal, then:
docker-compose down
```

---

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Compose Best Practices](https://docs.docker.com/compose/production/)

---

## 🎓 Summary

**Docker Compose** simplifies Docker workflows by:
- ✅ Defining all configuration in one YAML file
- ✅ Running complex setups with one command
- ✅ Managing multiple containers easily
- ✅ Providing consistent development environments
- ✅ Making deployment reproducible

**Your next command**: `docker-compose up --build` 🚀
