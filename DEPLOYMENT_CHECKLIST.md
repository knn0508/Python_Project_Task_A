# Vercel Deployment Checklist

## Pre-Deployment Checklist

### ✅ Required Files Created
- [x] `vercel.json` - Vercel configuration
- [x] `runtime.txt` - Python version specification  
- [x] `requirements.txt` - Updated with all dependencies
- [x] `.env.example` - Environment variables template
- [x] `VERCEL_DEPLOYMENT.md` - Deployment instructions

### ✅ Code Modifications
- [x] Modified `app.py` for serverless compatibility
- [x] Updated `config.py` for environment variables
- [x] Modified `file_manager.py` for temporary storage
- [x] Updated `.gitignore` for environment files

### 🔧 Before Deployment

1. **Get Google Gemini API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy the key for environment variables

2. **Prepare Environment Variables**
   - `SECRET_KEY`: Generate a secure random string
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `FLASK_ENV`: Set to "production"
   - `DATABASE_PATH`: "/tmp/users.db"
   - `DB_PATH`: "/tmp/file_index.db"  
   - `STORAGE_DIR`: "/tmp/documents"

3. **Test Locally (Optional)**
   ```bash
   pip install -r requirements.txt
   python dev_server.py
   ```

### 🚀 Deployment Options

#### Option A: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login and deploy
vercel login
vercel

# Set environment variables when prompted
```

#### Option B: GitHub Integration
1. Push code to GitHub repository
2. Connect GitHub to Vercel
3. Import repository in Vercel dashboard
4. Configure environment variables
5. Deploy

### ⚠️ Important Limitations

1. **Database Persistence**
   - SQLite database resets on each deployment
   - User data is temporary
   - Consider external database for production

2. **File Storage**
   - Uploaded files are temporary
   - Files lost between function calls
   - Consider cloud storage for production

3. **Function Timeout**
   - Free tier: 10 seconds
   - May need optimization for large files

### 🔧 Production Recommendations

1. **Use External Database**
   - Vercel Postgres
   - PlanetScale  
   - Supabase
   - Railway

2. **Use Cloud Storage**
   - Vercel Blob
   - AWS S3
   - Cloudinary
   - Google Cloud Storage

3. **Monitor Performance**
   - Check Vercel function logs
   - Monitor response times
   - Optimize database queries

### 📋 Post-Deployment Testing

1. **Basic Functionality**
   - [ ] Home page loads
   - [ ] User registration works
   - [ ] User login works
   - [ ] File upload works
   - [ ] AI chat works

2. **Environment Variables**
   - [ ] GEMINI_API_KEY is working
   - [ ] SECRET_KEY is secure
   - [ ] Database connections work

3. **Error Handling**
   - [ ] Check Vercel function logs
   - [ ] Test error pages
   - [ ] Verify timeout handling

### 🆘 Troubleshooting

**Common Issues:**
- Import errors → Check requirements.txt
- Database errors → Verify environment variables
- Timeout errors → Optimize code or upgrade plan
- API errors → Check Gemini API key

**Get Help:**
- Vercel docs: https://vercel.com/docs
- Vercel Discord: https://vercel.com/discord
- GitHub Issues: Create issue in your repository
