# Vercel Deployment Guide

## Prerequisites
1. A Vercel account (sign up at https://vercel.com)
2. Git repository with your project
3. Google Gemini API key

## Environment Variables Required
Before deploying, you need to set up the following environment variables in Vercel:

1. `SECRET_KEY` - A secure secret key for Flask sessions
2. `GEMINI_API_KEY` - Your Google Gemini API key
3. `FLASK_ENV` - Set to "production"
4. `DATABASE_PATH` - Set to "/tmp/users.db" (for Vercel's temporary filesystem)

## Deployment Steps

### Option 1: Deploy via Vercel CLI
1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from project directory:
   ```bash
   vercel
   ```

4. Follow the prompts and set up environment variables when asked.

### Option 2: Deploy via GitHub Integration
1. Push your code to a GitHub repository
2. Connect your GitHub account to Vercel
3. Import your repository in Vercel dashboard
4. Configure environment variables in the Vercel project settings
5. Deploy

## Environment Variables Setup in Vercel

1. Go to your project in Vercel dashboard
2. Navigate to Settings → Environment Variables
3. Add the following variables:

   | Name | Value | Environment |
   |------|-------|-------------|
   | SECRET_KEY | your-secret-key-here | Production |
   | GEMINI_API_KEY | your-gemini-api-key | Production |
   | FLASK_ENV | production | Production |
   | DATABASE_PATH | /tmp/users.db | Production |

## Important Notes

### Database Limitations
- Vercel's serverless functions use a read-only filesystem except for `/tmp`
- The SQLite database will be temporary and reset on each deployment
- For production use, consider using a persistent database service like:
  - Vercel Postgres
  - PlanetScale
  - Railway PostgreSQL
  - Supabase

### File Upload Limitations
- Uploaded files are stored in `/tmp` and will be lost between function invocations
- Consider using cloud storage services like:
  - Vercel Blob
  - AWS S3
  - Cloudinary
  - Google Cloud Storage

### Function Timeout
- Vercel free tier has a 10-second function timeout
- Hobby tier has 60 seconds
- Pro tier has 300 seconds
- Large file processing might need optimization

## Recommended Improvements for Production

1. **Use External Database**:
   ```python
   # Replace SQLite with PostgreSQL
   import psycopg2
   DATABASE_URL = os.environ.get('DATABASE_URL')
   ```

2. **Use Cloud Storage**:
   ```python
   # Use Vercel Blob for file storage
   from vercel_blob import put, del_
   ```

3. **Add Health Check**:
   ```python
   @app.route('/health')
   def health_check():
       return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
   ```

## Troubleshooting

### Common Issues:
1. **Import Errors**: Make sure all dependencies are in requirements.txt
2. **Database Errors**: Check if DATABASE_PATH is set correctly
3. **API Key Errors**: Verify GEMINI_API_KEY is set in environment variables
4. **Timeout Errors**: Optimize database queries and file processing

### Logs:
- Check Vercel function logs in the dashboard under "Functions" tab
- Use `vercel logs` CLI command for real-time logs

## Local Testing
To test locally with production-like settings:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your actual values in `.env`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Support
If you encounter issues, check:
- Vercel documentation: https://vercel.com/docs
- Flask documentation: https://flask.palletsprojects.com/
- Google Gemini API docs: https://ai.google.dev/docs
