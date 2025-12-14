# SafeSQL-Lab Troubleshooting Guide

## Common Issues and Solutions

### 1. Docker Network Issues

**Problem**: `failed to resolve source metadata for docker.io/library/python:3.11-slim`

**Solutions**:
1. **Use Local Setup** (Recommended for network issues):
   ```bash
   python setup_local.py
   python app.py
   ```

2. **Try Alternative Docker Setup**:
   ```bash
   docker-compose -f docker-compose-simple.yml up --build
   ```

3. **Use Different Base Image**:
   - Edit `Dockerfile` to use `python:3.9-slim` instead of `python:3.11-slim`
   - Or use `python:3.9-alpine` for smaller size

### 2. Docker Compose Version Warning

**Problem**: `the attribute 'version' is obsolete`

**Solution**: The `version` field has been removed from `docker-compose.yml`. This warning can be ignored.

### 3. Service Not Running

**Problem**: `service "web" is not running`

**Solutions**:
1. **Start the service first**:
   ```bash
   docker-compose up --build
   ```

2. **Check if containers are running**:
   ```bash
   docker-compose ps
   ```

3. **View logs for debugging**:
   ```bash
   docker-compose logs web
   ```

### 4. Port Already in Use

**Problem**: Port 5000 is already in use

**Solutions**:
1. **Change the port** in `docker-compose.yml`:
   ```yaml
   ports:
     - "5001:5000"  # Use port 5001 instead
   ```

2. **Kill existing processes**:
   ```bash
   sudo lsof -ti:5000 | xargs kill -9
   ```

### 5. Database Issues

**Problem**: Database not found or corrupted

**Solutions**:
1. **Reset the database**:
   ```bash
   python reset_db.py
   ```

2. **Remove and recreate data directory**:
   ```bash
   rm -rf data/
   mkdir data
   python reset_db.py
   ```

### 6. Permission Issues

**Problem**: Permission denied errors

**Solutions**:
1. **Fix file permissions**:
   ```bash
   chmod +x setup_local.py
   chmod +x run_checks.sh
   ```

2. **Run with sudo if needed**:
   ```bash
   sudo python setup_local.py
   ```

### 7. Python Dependencies Issues

**Problem**: Module not found or import errors

**Solutions**:
1. **Install dependencies manually**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Use virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### 8. Application Won't Start

**Problem**: Application fails to start

**Solutions**:
1. **Check Python version** (requires 3.8+):
   ```bash
   python --version
   ```

2. **Check for syntax errors**:
   ```bash
   python -m py_compile app.py
   ```

3. **Run with debug mode**:
   ```bash
   python app.py --debug
   ```

## Alternative Setup Methods

### Method 1: Local Python Setup (Recommended for network issues)

```bash
# 1. Setup the environment
python setup_local.py

# 2. Start the application
python app.py

# 3. Access at http://localhost:5000
```

### Method 2: Simple Docker Setup

```bash
# 1. Use the simple Docker setup
docker-compose -f docker-compose-simple.yml up --build

# 2. Access at http://localhost:5000
```

### Method 3: Manual Docker Setup

```bash
# 1. Build the image manually
docker build -t safesql-lab .

# 2. Run the container
docker run -p 5000:5000 -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs safesql-lab

# 3. Access at http://localhost:5000
```

## Verification Steps

### 1. Check Application Health

```bash
# Test the health endpoint
curl http://localhost:5000/health

# Expected response: {"status": "healthy", "service": "safesql-lab"}
```

### 2. Run Tests

```bash
# Run the test suite
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_vulnerable_endpoints.py -v
```

### 3. Check Database

```bash
# Check if database exists and has data
sqlite3 data/lab.db "SELECT COUNT(*) FROM users;"

# Expected: Should return a number > 0
```

## Getting Help

### 1. Check Logs

```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f web
```

### 2. Environment Check

```bash
# Run the environment check script
./run_checks.sh
```

### 3. Common Commands

```bash
# Stop all containers
docker-compose down

# Remove all containers and images
docker-compose down --rmi all

# Rebuild everything
docker-compose up --build --force-recreate

# Reset database
python reset_db.py
```

## Network-Specific Solutions

### For Restricted Networks

1. **Use Local Setup**: `python setup_local.py`
2. **Download Images Manually**: Use `docker save` and `docker load`
3. **Use Corporate Proxy**: Configure Docker proxy settings
4. **Use Alternative Registries**: Configure Docker to use different registries

### For Offline Environments

1. **Pre-download Dependencies**: Use `pip download` to get all packages
2. **Use Local Docker Registry**: Set up local Docker registry
3. **Bundle Everything**: Create a complete offline package

## Security Considerations

### Always Remember

- ✅ Only run on localhost (127.0.0.1)
- ✅ Never deploy on public networks
- ✅ Keep instructor materials secure
- ✅ Monitor all activities
- ✅ Follow legal compliance requirements

### Emergency Procedures

1. **Stop the application immediately** if security issues are detected
2. **Check logs** for suspicious activities
3. **Reset database** if compromised
4. **Review access controls** and permissions
5. **Update security measures** as needed

---

For additional help, check the main README.md or contact the project maintainers.
