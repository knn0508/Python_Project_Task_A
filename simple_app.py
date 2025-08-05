from flask import Flask, jsonify
from datetime import datetime
import os

# Create a simple Flask app for testing
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Vercel!',
        'status': 'success',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'app': 'AI Document Management System',
        'environment': os.environ.get('VERCEL_ENV', 'unknown'),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test')
def test():
    return '<h1>Flask App is Working on Vercel!</h1><p>Your deployment is successful.</p>'

if __name__ == '__main__':
    app.run(debug=True)
