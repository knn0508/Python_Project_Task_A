import os
import sys
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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
        # Try to import our modules
        from models import EnhancedKnowledgeBase, UserManager, EnhancedAIAssistant
        from file_manager import FileManager
        from config import Config
        
        # Initialize components
        file_manager = FileManager()
        knowledge_base = EnhancedKnowledgeBase(file_manager)
        user_manager = UserManager()
        
        # Try to initialize AI assistant with API key
        api_key = os.environ.get('GEMINI_API_KEY')
        if api_key:
            ai_assistant = EnhancedAIAssistant(knowledge_base, api_key)
        else:
            print("Warning: GEMINI_API_KEY not found")
            
        print("✅ All components initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing components: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Initialize minimal components
        try:
            from file_manager import FileManager
            file_manager = FileManager()
            print("✅ Basic file manager initialized")
        except:
            print("❌ Failed to initialize even basic components")
        
        return False

# Initialize components
components_ready = safe_import_and_init()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Main route"""
    return jsonify({
        'message': 'AI Document Management System',
        'status': 'running',
        'components_ready': components_ready,
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

@app.route('/login')
def login():
    """Login page"""
    try:
        if components_ready and user_manager:
            return render_template('login.html')
        else:
            return jsonify({
                'error': 'User management system not available',
                'message': 'Components not properly initialized'
            }), 503
    except Exception as e:
        return jsonify({
            'error': 'Template rendering failed',
            'message': str(e)
        }), 500

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    try:
        if components_ready:
            return render_template('dashboard.html')
        else:
            return jsonify({
                'error': 'System not fully initialized',
                'message': 'Please check system health'
            }), 503
    except Exception as e:
        return jsonify({
            'error': 'Dashboard unavailable',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
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
