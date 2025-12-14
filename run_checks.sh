#!/bin/bash

# SafeSQL-Lab Environment Check Script
# Verifies that the lab environment is properly set up and running

echo "=========================================="
echo "SafeSQL-Lab Environment Check"
echo "=========================================="

# Check if Docker is running
echo "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
else
    echo "✅ Docker is running"
fi

# Check if Docker Compose is available
echo "Checking Docker Compose..."
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
else
    echo "✅ Docker Compose is available"
fi

# Check if required directories exist
echo "Checking required directories..."
required_dirs=("data" "logs" "instructor")
for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Creating directory: $dir"
        mkdir -p "$dir"
    else
        echo "✅ Directory $dir exists"
    fi
done

# Check if application files exist
echo "Checking application files..."
required_files=("app.py" "requirements.txt" "Dockerfile" "docker-compose.yml")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file $file is missing"
        exit 1
    else
        echo "✅ File $file exists"
    fi
done

# Check if instructor materials exist
echo "Checking instructor materials..."
instructor_files=("instructor/payloads.txt" "instructor/solutions.md" "instructor/README.md")
for file in "${instructor_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Instructor file $file is missing"
        exit 1
    else
        echo "✅ Instructor file $file exists"
    fi
done

# Check if tests exist
echo "Checking test files..."
if [ ! -f "tests/test_vulnerable_endpoints.py" ]; then
    echo "❌ Test file tests/test_vulnerable_endpoints.py is missing"
    exit 1
else
    echo "✅ Test file tests/test_vulnerable_endpoints.py exists"
fi

# Check if the application is running
echo "Checking if application is running..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Application is running on localhost:5000"
else
    echo "⚠️  Application is not running. You may need to start it with: docker-compose up"
fi

# Check database
echo "Checking database..."
if [ -f "data/lab.db" ]; then
    echo "✅ Database file exists"
    
    # Check if database has data
    if sqlite3 data/lab.db "SELECT COUNT(*) FROM users;" > /dev/null 2>&1; then
        user_count=$(sqlite3 data/lab.db "SELECT COUNT(*) FROM users;")
        echo "✅ Database has $user_count users"
    else
        echo "⚠️  Database exists but may not be properly seeded"
    fi
else
    echo "⚠️  Database file does not exist. It will be created when the application starts."
fi

# Check logs
echo "Checking logs..."
if [ -d "logs" ] && [ -f "logs/app.log" ]; then
    echo "✅ Log file exists"
    log_size=$(wc -l < logs/app.log 2>/dev/null || echo "0")
    echo "✅ Log file has $log_size lines"
else
    echo "⚠️  Log file does not exist yet. It will be created when the application starts."
fi

# Security checks
echo "Checking security configuration..."
if grep -q "127.0.0.1" docker-compose.yml; then
    echo "✅ Application configured to bind to localhost only"
else
    echo "⚠️  Warning: Application may not be configured to bind to localhost only"
fi

if grep -q "instructor" .gitignore 2>/dev/null; then
    echo "✅ Instructor materials excluded from version control"
else
    echo "⚠️  Warning: Consider adding instructor/ to .gitignore"
fi

echo "=========================================="
echo "Environment check complete!"
echo "=========================================="

# Final recommendations
echo ""
echo "Next steps:"
echo "1. Start the application: docker-compose up"
echo "2. Access the lab: http://localhost:5000"
echo "3. Run tests: python -m pytest tests/"
echo "4. Reset database if needed: python reset_db.py"
echo ""
echo "Remember: This lab is for educational use only!"
echo "Never deploy on public networks."
