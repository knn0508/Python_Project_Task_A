#!/usr/bin/env python3
"""
Local development server for testing Vercel deployment locally
"""
import os
from app import app

if __name__ == "__main__":
    # Set environment variables for local testing
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('SECRET_KEY', 'dev-secret-key')
    os.environ.setdefault('DATABASE_PATH', 'users.db')
    
    print("🚀 Starting local development server...")
    print("📝 Make sure to set your GEMINI_API_KEY in environment variables")
    print("🌐 Server will be available at http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
