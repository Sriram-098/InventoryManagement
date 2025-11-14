# Deployment Guide

## Deploy to Render

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Set Environment Variables:**
   In Render dashboard, add these environment variables for the backend:
   ```
   DATABASE_URL=postgresql://postgres.guutfvgljkjwiojqdpij:Sriram938137@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres
   SUPABASE_URL=https://guutfvgljkjwiojqdpij.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Option 2: Manual Deployment

#### Backend Deployment

1. **Create a new Web Service on Render:**
   - Runtime: Python 3
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Add Environment Variables:**
   - `DATABASE_URL` - Your Supabase PostgreSQL URL
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon key

3. **Deploy!**

#### Frontend Deployment

1. **Update API URL:**
   Create `frontend/.env.production`:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

2. **Update frontend/src/services/api.js:**
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
   ```

3. **Create a new Static Site on Render:**
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

## Deploy to Heroku

### Backend

1. **Install Heroku CLI and login:**
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create inventory-backend
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set DATABASE_URL="your-database-url"
   heroku config:set SUPABASE_URL="your-supabase-url"
   heroku config:set SUPABASE_KEY="your-supabase-key"
   ```

4. **Deploy:**
   ```bash
   git subtree push --prefix backend heroku main
   ```

### Frontend

1. **Deploy to Vercel:**
   ```bash
   cd frontend
   npm install -g vercel
   vercel
   ```

2. **Or deploy to Netlify:**
   ```bash
   cd frontend
   npm install -g netlify-cli
   netlify deploy --prod
   ```

## Deploy to Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and initialize:**
   ```bash
   railway login
   railway init
   ```

3. **Deploy backend:**
   ```bash
   cd backend
   railway up
   ```

4. **Set environment variables in Railway dashboard**

## Troubleshooting

### Build Fails with pip errors

**Solution 1:** Update requirements.txt to use specific versions without extras:
```
python-jose==3.3.0
cryptography==41.0.7
email-validator==2.1.0
```

**Solution 2:** Add a `runtime.txt` file:
```
python-3.11.7
```

**Solution 3:** Upgrade pip in build command:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Database Connection Issues

- Ensure `DATABASE_URL` is set correctly
- Check if Supabase allows connections from Render's IP
- Verify the connection string format

### CORS Errors

Update `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend Can't Connect to Backend

1. Update `frontend/src/services/api.js`:
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
   ```

2. Set environment variable in deployment platform:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```

## Post-Deployment

1. **Run database migrations:**
   ```bash
   # SSH into your backend service or run locally
   python migrate_db.py
   ```

2. **Create admin user:**
   The default admin user is created automatically on first run:
   - Username: `admin`
   - Password: `admin123`

3. **Test the application:**
   - Visit your frontend URL
   - Login with admin credentials
   - Add a test product
   - Verify all features work

## Environment Variables Reference

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon/public key
- `PORT` - Port number (auto-set by hosting platform)

### Frontend
- `VITE_API_URL` - Backend API URL

## Security Notes

- Never commit `.env` files to Git
- Use environment variables for all sensitive data
- Change default admin password after first login
- Enable HTTPS on production
- Set proper CORS origins in production
