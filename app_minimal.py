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
        
        # Create dummy user info for demo mode
        demo_user_info = {
            'id': 'demo_user',
            'username': 'demo',
            'name': 'Demo User',
            'role': 'admin'  # Give admin access for demo
        }
        
        # Use the AI assistant to answer
        try:
            response = ai_assistant.generate_enhanced_response(question, demo_user_info)
            
            # Check if we got the generic error message
            if "texniki problem var" in response:
                # Try the simpler method instead
                response = ai_assistant.generate_response(question, demo_user_info)
                
            # If still getting error, try direct knowledge base search
            if "texniki problem var" in response:
                # Fallback to direct knowledge base search
                kb_response = knowledge_base.search(question)
                response = f"Tapılan məlumatlar:\n\n{kb_response}"
                
        except Exception as ai_error:
            # If AI fails completely, use knowledge base directly
            try:
                kb_response = knowledge_base.search(question)
                response = f"Məlumat bazasından tapılan nəticələr:\n\n{kb_response}"
            except Exception as kb_error:
                response = f"Xəta baş verdi: AI Error: {str(ai_error)}, KB Error: {str(kb_error)}"
        
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
                    alert('Login successful! Redirecting to AI interface...');
                    window.location.href = '/ai-interface';
                } else {
                    alert('Invalid credentials. Please use demo credentials.');
                }
            }
        </script>
    </body>
    </html>
    """
    return html

@app.route('/ai-interface')
def ai_interface():
    """Simple AI interface for testing"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Document Management - AI Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; }
            .chat-container { background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; max-height: 400px; overflow-y: auto; }
            .question-form { margin: 20px 0; }
            textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; resize: vertical; }
            button { background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px 0 0; }
            button:hover { background: #218838; }
            .loading { color: #007bff; font-style: italic; }
            .error { color: #dc3545; background: #f8d7da; padding: 10px; border-radius: 5px; margin: 10px 0; }
            .answer { background: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #28a745; }
            .question { background: #e2e3e5; padding: 10px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #6c757d; }
            .sample-questions { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .sample-btn { background: #ffc107; color: #212529; padding: 5px 10px; border: none; border-radius: 3px; cursor: pointer; margin: 5px; font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>🤖 AI Document Management Assistant</h1>
        <p>Ask questions about the ministry, departments, procedures, and documents.</p>
        
        <div class="sample-questions">
            <h3>📝 Sample Questions (Click to try):</h3>
            <button class="sample-btn" onclick="askQuestion('What departments does the ministry have?')">Ministry Departments</button>
            <button class="sample-btn" onclick="askQuestion('What are the contact details for HR?')">HR Contact Info</button>
            <button class="sample-btn" onclick="askQuestion('How do I apply for vacation leave?')">Vacation Leave</button>
            <button class="sample-btn" onclick="askQuestion('What are the working hours?')">Working Hours</button>
            <button class="sample-btn" onclick="askQuestion('How much is the daily allowance for business travel?')">Travel Allowance</button>
        </div>
        
        <div class="question-form">
            <textarea id="questionInput" placeholder="Ask your question here..." rows="3"></textarea><br>
            <button onclick="submitQuestion()">Ask AI</button>
            <button onclick="clearChat()">Clear Chat</button>
        </div>
        
        <div id="chatContainer" class="chat-container">
            <p>💡 Welcome! Ask me anything about the ministry, departments, procedures, or documents.</p>
        </div>
        
        <script>
            function askQuestion(question) {
                document.getElementById('questionInput').value = question;
                submitQuestion();
            }
            
            function submitQuestion() {
                const question = document.getElementById('questionInput').value.trim();
                if (!question) {
                    alert('Please enter a question');
                    return;
                }
                
                const chatContainer = document.getElementById('chatContainer');
                
                // Add question to chat
                chatContainer.innerHTML += '<div class="question"><strong>You:</strong> ' + question + '</div>';
                
                // Add loading indicator
                chatContainer.innerHTML += '<div class="loading" id="loading">🤖 AI is thinking...</div>';
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Make API call
                fetch('/demo-ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({question: question})
                })
                .then(response => response.json())
                .then(data => {
                    // Remove loading indicator
                    document.getElementById('loading').remove();
                    
                    if (data.error) {
                        chatContainer.innerHTML += '<div class="error"><strong>Error:</strong> ' + data.error + '<br><strong>Message:</strong> ' + data.message + '</div>';
                    } else {
                        chatContainer.innerHTML += '<div class="answer"><strong>🤖 AI Assistant:</strong><br>' + data.answer + '</div>';
                    }
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                })
                .catch(error => {
                    // Remove loading indicator
                    const loading = document.getElementById('loading');
                    if (loading) loading.remove();
                    
                    chatContainer.innerHTML += '<div class="error"><strong>Network Error:</strong> Could not connect to AI service. Please try again.</div>';
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                });
                
                // Clear input
                document.getElementById('questionInput').value = '';
            }
            
            function clearChat() {
                document.getElementById('chatContainer').innerHTML = '<p>💡 Welcome! Ask me anything about the ministry, departments, procedures, or documents.</p>';
            }
            
            // Allow Enter key to submit
            document.getElementById('questionInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    submitQuestion();
                }
            });
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
