#!/usr/bin/env python3
"""
SafeSQL-Lab: Educational SQL Injection Training Site

This application is designed for authorized, lawful, educational use only.
DO NOT deploy on the public internet. Always run in an isolated environment.

Author: SafeSQL-Lab Team
License: Educational Use Only
"""

import os
import sys
import argparse
import logging
from app import create_app

def setup_directories():
    """Create necessary directories"""
    directories = ['data', 'logs', 'instructor']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='SafeSQL-Lab Educational Application')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Security check: Ensure we're binding to localhost only
    if args.host not in ['127.0.0.1', 'localhost']:
        print("SECURITY WARNING: This application should only bind to localhost!")
        print("Forcing host to 127.0.0.1 for security.")
        args.host = '127.0.0.1'
    
    # Setup directories
    setup_directories()
    
    # Create application
    app = create_app()
    
    # Configure logging
    if not args.debug:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    print("=" * 60)
    print("SafeSQL-Lab: Educational SQL Injection Training Site")
    print("=" * 60)
    print("⚠️  LEGAL WARNING: FOR EDUCATIONAL USE ONLY ⚠️")
    print("This application is designed for authorized security training.")
    print("DO NOT deploy on the public internet.")
    print("=" * 60)
    print(f"Starting server on {args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nShutting down SafeSQL-Lab...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
