# Python Project Task A - AI Document Management System

## Overview
This is a Flask-based AI-powered document management and onboarding system that helps organizations manage their internal documents and provide intelligent assistance to users through AI integration.

## Features

### Core Functionality
- **Document Management**: Upload, store, and organize various document types (PDF, DOCX, MD, TXT)
- **AI Integration**: Powered by Google Gemini AI for intelligent document analysis and user assistance
- **User Management**: Secure user authentication and session management
- **Knowledge Base**: Enhanced knowledge base with document indexing and retrieval
- **File Processing**: Automatic file processing and content extraction
- **Web Interface**: User-friendly web interface with dashboard and file management

### AI Capabilities
- Document content analysis
- Intelligent Q&A based on document corpus
- Context-aware responses
- Multi-language support (including Azerbaijani)

### Security Features
- User authentication system
- Secure file upload handling
- Session management
- SQL injection protection

## Project Structure

```
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Core models (KnowledgeBase, UserManager, AIAssistant)
├── file_manager.py       # File handling and processing
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup configuration
├── .gitignore           # Git ignore rules
├── documents/           # Uploaded and processed documents
├── templates/           # HTML templates
│   ├── dashboard.html   # Main dashboard
│   ├── files.html       # File management interface
│   └── login.html       # Login page
├── test_documents/      # Sample test documents
├── simple_test_docs/    # Simple test documents
└── tests/               # Test files
    ├── simple_test.py
    ├── test_ai_integration.py
    └── test_large_files.py
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Python_Project_Task_A
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   FLASK_ENV=development
   ```

5. **Initialize the database**
   ```bash
   python -c "from models import UserManager; UserManager().create_tables()"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_SECRET_KEY`: Secret key for Flask sessions
- `FLASK_ENV`: Environment mode (development/production)

### File Upload Settings
- Maximum file size: 16MB
- Supported formats: PDF, DOCX, MD, TXT
- Upload directory: `documents/`

## Usage

### Web Interface
1. **Login**: Access the system through the login page
2. **Dashboard**: View system overview and statistics
3. **File Management**: Upload, view, and manage documents
4. **AI Assistant**: Ask questions about your documents

### API Endpoints
- `GET /`: Dashboard (login required)
- `GET /login`: User login page
- `POST /login`: Process login
- `GET /logout`: User logout
- `GET /files`: File management interface
- `POST /upload`: Upload new files
- `POST /ask`: AI assistant Q&A

## Testing

Run the test suite:
```bash
# Simple functionality test
python simple_test.py

# AI integration test
python test_ai_integration.py

# Large file handling test
python test_large_files.py
```

## Dependencies

### Core Dependencies
- **Flask 3.0.0**: Web framework
- **google-generativeai 0.3.2**: Google Gemini AI integration
- **Werkzeug 3.0.1**: WSGI utilities

### Production Dependencies
- **gunicorn 21.2.0**: Production WSGI server
- **python-dotenv 1.0.0**: Environment variable management

## Database

The application uses SQLite databases:
- `users.db`: User authentication data
- `file_index.db`: Document indexing and metadata

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact the development team.

## Changelog

### Version 1.0.0
- Initial release
- Basic document management
- AI integration with Google Gemini
- User authentication system
- Web interface implementation
