# SafeSQL-Lab: Educational SQL Injection Training Site

## ⚠️ CRITICAL LEGAL AND SAFETY WARNING ⚠️

**THIS PROJECT IS FOR AUTHORIZED, LAWFUL, EDUCATIONAL USE ONLY**

- **DO NOT** deploy this application on the public internet
- **ALWAYS** run inside an isolated environment (local machine or private VM/container) behind a firewall
- **NEVER** use these techniques against systems you do not own or lack explicit permission to test
- This is intended for security training, education, and authorized penetration testing only

## Purpose

SafeSQL-Lab is a controlled educational environment designed to teach:
- Recognition of SQL injection vulnerabilities
- Exploitation techniques in a safe, isolated lab environment
- Proper mitigation strategies and secure coding practices
- Multi-level exercises from basic to advanced scenarios

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (for local development)

### Running the Lab

#### Option 1: Virtual Environment Setup (Recommended for Kali Linux)

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd safesql-lab
   ```

2. **Setup virtual environment:**
   ```bash
   python setup_venv.py
   ```

3. **Start the application:**
   ```bash
   ./start_safesql.sh
   # OR
   venv/bin/python app.py
   ```

4. **Access the application:**
   - Open your browser to `http://localhost:5000`
   - The application will only bind to localhost for security

#### Option 2: Docker Setup

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd safesql-lab
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Open your browser to `http://localhost:5000`
   - The application will only bind to localhost for security

4. **Reset the database (if needed):**
   ```bash
   docker-compose exec web python reset_db.py
   # OR for virtual environment:
   venv/bin/python reset_db.py
   ```

## Project Structure

```
safesql-lab/
├── app/                    # Main Flask application
│   ├── __init__.py
│   ├── routes/            # Route handlers
│   ├── models/            # Database models
│   └── templates/         # HTML templates
├── instructor/            # Instructor-only materials (NOT web-served)
│   ├── payloads.txt       # Example exploit payloads
│   ├── solutions.md       # Step-by-step solutions
│   └── instructor_guide.pdf
├── tests/                 # Automated tests
├── docker-compose.yml     # Container orchestration
├── Dockerfile            # Application container
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Exercises Overview

### Easy Level
- **Login Form Injection**: Basic string concatenation vulnerability
- **Product Search**: Simple parameter injection

### Medium Level
- **Boolean-based Injection**: Logical manipulation required
- **Union-based Injection**: Data extraction techniques

### Hard Level
- **Time-based Blind Injection**: Advanced timing attacks
- **Stacked Queries**: Multiple statement execution

## Security Features

- Application binds only to localhost (127.0.0.1)
- Docker network isolation
- Instructor materials excluded from web serving
- Comprehensive logging of all activities
- Rate limiting and resource restrictions

## Legal Compliance

This project includes:
- Prominent legal warnings on every page
- "I understand" gating prompts before exercises
- Clear documentation of authorized use only
- Instructor-only materials with restricted access

## Contributing

When contributing to this project:
1. Ensure all vulnerable code includes educational comments
2. Never include exploit payloads in public files
3. Maintain strict separation of instructor materials
4. Follow the security checklist in `SECURITY.md`

## License

This project is licensed for educational use only. See LICENSE file for details.

## Support

For questions about this educational tool, please contact the project maintainers through the appropriate channels.
