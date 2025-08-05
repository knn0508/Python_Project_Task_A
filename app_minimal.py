from flask import Flask, jsonify, request, session, redirect, url_for
import os
import sys
from datetime import datetime
from functools import wraps

# Create Flask app first
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-development')

# Global variables for components
file_manager = None
knowledge_base = None
user_manager = None
ai_assistant = None

def safe_import_and_init():
    """Safely import and initialize components with error handling"""
    global file_manager, knowledge_base, user_manager, ai_assistant
    
    try:
        # Try to import our modules one by one
        from file_manager import FileManager
        from models import EnhancedKnowledgeBase, UserManager, EnhancedAIAssistant
        
        # Create necessary directories for serverless
        os.makedirs('/tmp/documents', exist_ok=True)
        os.makedirs('/tmp', exist_ok=True)
        
        # Initialize file manager first
        file_manager = FileManager()
        print("✅ File manager initialized")
        
        # Initialize knowledge base
        knowledge_base = EnhancedKnowledgeBase(file_manager)
        print("✅ Knowledge base initialized")
        
        # Try to initialize AI assistant with API key
        try:
            api_key = os.environ.get('GEMINI_API_KEY')
            if api_key:
                ai_assistant = EnhancedAIAssistant(knowledge_base, api_key)
                print("✅ AI assistant initialized")
            else:
                print("⚠️ GEMINI_API_KEY not found")
                ai_assistant = None
        except Exception as e:
            print(f"⚠️ AI assistant failed: {e}")
            ai_assistant = None
            
        print("✅ Core components initialization completed")
        return True
        
    except Exception as e:
        print(f"❌ Critical error in initialization: {e}")
        import traceback
        traceback.print_exc()
        return False

# Initialize components
components_ready = safe_import_and_init()

@app.route('/')
def index():
    """Main route"""
    return jsonify({
        'message': 'AI Document Management System',
        'status': 'running',
        'components_ready': components_ready,
        'available_endpoints': {
            'health': '/health',
            'demo': '/demo',
            'ask_ai': '/demo-ask (POST)',
            'simple_login': '/simple-login',
            'components_test': '/test-components'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'components': {
                'file_manager': file_manager is not None,
                'knowledge_base': knowledge_base is not None,
                'user_manager': user_manager is not None,
                'ai_assistant': ai_assistant is not None,
                'components_ready': components_ready
            },
            'environment': {
                'python_version': sys.version,
                'flask_env': os.environ.get('FLASK_ENV', 'not_set'),
                'has_gemini_key': bool(os.environ.get('GEMINI_API_KEY')),
                'vercel_env': os.environ.get('VERCEL_ENV', 'not_vercel')
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'error_type': type(e).__name__,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/demo')
def demo_access():
    """Demo access without authentication"""
    try:
        return jsonify({
            'message': 'Demo mode - AI Document Management System',
            'status': 'ready' if ai_assistant else 'limited',
            'ai_available': ai_assistant is not None,
            'knowledge_base_ready': knowledge_base is not None,
            'demo_query_endpoint': '/demo-ask',
            'instructions': {
                'how_to_ask': 'POST to /demo-ask with JSON: {"question": "your question"}',
                'sample_questions': [
                    "What departments does the ministry have?",
                    "What are the contact details for HR?",
                    "How do I apply for vacation leave?",
                    "What are the working hours?"
                ]
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': 'Demo access failed',
            'message': str(e)
        }), 500

@app.route('/demo-ask', methods=['POST'])
def demo_ask():
    """Demo AI assistant without authentication"""
    try:
        if not ai_assistant:
            return jsonify({
                'error': 'AI Assistant not available',
                'message': 'AI components not properly initialized',
                'available_components': {
                    'file_manager': file_manager is not None,
                    'knowledge_base': knowledge_base is not None,
                    'ai_assistant': ai_assistant is not None
                }
            }), 503
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Missing question',
                'message': 'Please provide a question in JSON format: {"question": "your question"}',
                'example': '{"question": "What departments does the ministry have?"}'
            }), 400
        
        question = data['question']
        
        # Use the AI assistant to answer
        response = ai_assistant.ask_question(question)
        
        return jsonify({
            'question': question,
            'answer': response,
            'timestamp': datetime.now().isoformat(),
            'mode': 'demo'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'AI query failed',
            'message': str(e),
            'question': data.get('question', 'unknown') if 'data' in locals() else 'unknown',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/simple-login')
def simple_login():
    """Simple login form as HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Document Management - Login</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
            .form-group { margin: 10px 0; }
            input[type="text"], input[type="password"] { width: 100%; padding: 8px; margin: 5px 0; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            .demo-creds { background: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h2>AI Document Management System</h2>
        <form id="loginForm">
            <div class="form-group">
                <input type="text" id="username" placeholder="Username" required>
            </div>
            <div class="form-group">
                <input type="password" id="password" placeholder="Password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        
        <div class="demo-creds">
            <h4>Demo Credentials:</h4>
            <p><strong>Admin:</strong> admin / admin123</p>
            <p><strong>Minister:</strong> nazir / nazir123</p>
            <p><strong>Analyst:</strong> analitik / data123</p>
        </div>
        
        <script>
            document.getElementById('loginForm').onsubmit = function(e) {
                e.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                // Simple demo check
                const users = {
                    'admin': 'admin123',
                    'nazir': 'nazir123',
                    'analitik': 'data123'
                };
                
                if (users[username] === password) {
                    alert('Login successful! Redirecting to demo...');
                    window.location.href = '/demo';
                } else {
                    alert('Invalid credentials. Please use demo credentials.');
                }
            }
        </script>
    </body>
    </html>
    """
    return html

@app.route('/test-components')
def test_components():
    """Test individual components"""
    results = {}
    
    try:
        results['file_manager'] = 'working' if file_manager else 'not_initialized'
        results['knowledge_base'] = 'working' if knowledge_base else 'not_initialized'
        results['user_manager'] = 'working' if user_manager else 'not_initialized'
        results['ai_assistant'] = 'working' if ai_assistant else 'not_initialized'
    except Exception as e:
        results['error'] = str(e)
    
    return jsonify({
        'component_tests': results,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'available_endpoints': ['/', '/health', '/demo', '/demo-ask', '/simple-login', '/test-components'],
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred',
        'status_code': 500
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
