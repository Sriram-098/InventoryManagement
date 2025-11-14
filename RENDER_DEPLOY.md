# Quick Render Deployment Fix

## The Issue
The error occurs because `cryptography` package requires Rust compiler, and Render's Python 3.13 has compatibility issues.

## Solution: Use Python 3.11

### Method 1: Manual Deployment (Recommended)

1. **Create Backend Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `inventory-backend`
     - **Root Directory**: `backend`
     - **Runtime**: `Python 3`
     - **Build Command**: 
       ```bash
       pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt && python migrate_db.py
       ```
     - **Start Command**: 
       ```bash
       uvicorn main:app --host 0.0.0.0 --port $PORT
       ```
     - **Python Version**: Select `3.11.9` in Environment settings

2. **Add Environment Variables:**
   ```
   DATABASE_URL=postgresql://postgres.guutfvgljkjwiojqdpij:Sriram938137@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres
   SUPABASE_URL=https://guutfvgljkjwiojqdpij.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   PYTHON_VERSION=3.11.9
   ```

3. **Deploy Backend** - Click "Create Web Service"

4. **Create Frontend Static Site:**
   - Click "New" → "Static Site"
   - Connect same repository
   - Configure:
     - **Name**: `inventory-frontend`
     - **Root Directory**: `frontend`
     - **Build Command**: 
       ```bash
       npm install && npm run build
       ```
     - **Publish Directory**: `dist`

5. **Add Frontend Environment Variable:**
   ```
   VITE_API_URL=https://inventory-backend.onrender.com/api
   ```
   (Replace with your actual backend URL)

6. **Deploy Frontend** - Click "Create Static Site"

### Method 2: Using Blueprint (render.yaml)

If you want to use the `render.yaml` file:

1. Push your code to GitHub
2. On Render Dashboard, click "New" → "Blueprint"
3. Connect your repository
4. Render will detect `render.yaml` and create both services
5. Add environment variables in each service's settings

## Troubleshooting

### If build still fails:

**Option A: Specify Python version in Render Dashboard**
- Go to your service settings
- Under "Environment", add:
  ```
  PYTHON_VERSION=3.11.9
  ```

**Option B: Use alternative requirements**
Create `backend/requirements-render.txt`:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
python-multipart==0.0.6
python-jose==3.3.0
ecdsa==0.18.0
bcrypt==4.1.2
email-validator==2.1.0
```

Then use this build command:
```bash
pip install --upgrade pip && pip install -r requirements-render.txt
```

### If database connection fails:

Check that your Supabase database allows connections from Render's IPs. You may need to:
1. Go to Supabase Dashboard
2. Settings → Database
3. Add Render's IP ranges to allowed connections

### After Successful Deployment:

1. Visit your backend URL: `https://your-backend.onrender.com`
2. You should see: `{"message":"Wholesale Shop Inventory Management API"}`
3. Visit your frontend URL: `https://your-frontend.onrender.com`
4. Login with: username=`admin`, password=`admin123`

## Alternative: Deploy to Railway (Easier)

If Render continues to have issues, try Railway:

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

Railway handles Python dependencies better and doesn't have the same Rust/cryptography issues.
