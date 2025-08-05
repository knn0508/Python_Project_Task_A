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
        # Try to import our modules one by one
        from file_manager import FileManager
        from models import EnhancedKnowledgeBase, UserManager, EnhancedAIAssistant
        from config import Config
        
        # Create necessary directories for serverless
        os.makedirs('/tmp/documents', exist_ok=True)
        os.makedirs('/tmp', exist_ok=True)
        
        # Initialize file manager first
        file_manager = FileManager()
        print("✅ File manager initialized")
        
        # Initialize knowledge base
        knowledge_base = EnhancedKnowledgeBase(file_manager)
        print("✅ Knowledge base initialized")
        
        # Try to initialize user manager with error handling
        try:
            # Set the database path for serverless environment
            os.environ['DATABASE_PATH'] = '/tmp/users.db'
            user_manager = UserManager()
            print("✅ User manager initialized")
        except Exception as e:
            print(f"⚠️ User manager failed: {e}")
            # Try to create a minimal user manager without database
            user_manager = None
        
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
            
        print("✅ Components initialization completed")
        return True
        
    except Exception as e:
        print(f"❌ Critical error in initialization: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Initialize minimal components as fallback
        try:
            from file_manager import FileManager
            file_manager = FileManager()
            print("✅ Fallback: Basic file manager initialized")
        except Exception as fallback_error:
            print(f"❌ Fallback failed: {fallback_error}")
        
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

@app.route('/demo')
def demo_access():
    """Demo access without authentication"""
    try:
        if knowledge_base and ai_assistant:
            return jsonify({
                'message': 'Demo mode - AI Document Management System',
                'status': 'ready',
                'ai_available': True,
                'knowledge_base_ready': True,
                'demo_query_endpoint': '/demo-ask',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'message': 'Demo mode - Limited functionality',
                'status': 'partial',
                'ai_available': ai_assistant is not None,
                'knowledge_base_ready': knowledge_base is not None,
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
                'message': 'AI components not properly initialized'
            }), 503
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Missing question',
                'message': 'Please provide a question in JSON format: {"question": "your question"}'
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
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/simple')
def simple_endpoint():
    """Simple endpoint that always works"""
    return jsonify({
        'message': 'AI Document Management System - Simple Mode',
        'status': 'working',
        'info': 'This endpoint works regardless of component status',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test-components')
def test_components():
    """Test individual components"""
    results = {}
    
    # Test file manager
    try:
        if file_manager:
            results['file_manager'] = 'working'
        else:
            results['file_manager'] = 'not_initialized'
    except Exception as e:
        results['file_manager'] = f'error: {str(e)}'
    
    # Test knowledge base
    try:
        if knowledge_base:
            results['knowledge_base'] = 'working'
        else:
            results['knowledge_base'] = 'not_initialized'
    except Exception as e:
        results['knowledge_base'] = f'error: {str(e)}'
    
    # Test user manager
    try:
        if user_manager:
            results['user_manager'] = 'working'
        else:
            results['user_manager'] = 'not_initialized'
    except Exception as e:
        results['user_manager'] = f'error: {str(e)}'
    
    # Test AI assistant
    try:
        if ai_assistant:
            results['ai_assistant'] = 'working'
        else:
            results['ai_assistant'] = 'not_initialized'
    except Exception as e:
        results['ai_assistant'] = f'error: {str(e)}'
    
    return jsonify({
        'component_tests': results,
        'timestamp': datetime.now().isoformat()
    })

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
