# Render Deployment - Rust/Pydantic Error Fix

## The Problem
Render is using Python 3.13 which doesn't have pre-built wheels for `pydantic-core` and `bcrypt`, requiring Rust compilation which fails.

## Solution: Force Python 3.11

### Step 1: Update Render Settings

In your Render dashboard for the backend service:

1. Go to **Environment** tab
2. Add this environment variable:
   ```
   PYTHON_VERSION=3.11.9
   ```

3. **OR** in the service settings, look for "Python Version" dropdown and select **3.11.9**

### Step 2: Use Alternative Requirements (If Step 1 doesn't work)

Update your build command to use the minimal requirements file:

**Build Command:**
```bash
cd backend && pip install --upgrade pip && pip install -r requirements-minimal.txt && python migrate_db.py
```

This uses Pydantic v1 which has pre-built wheels and doesn't require Rust.

### Step 3: Redeploy

Click "Manual Deploy" → "Clear build cache & deploy"

## Alternative: Deploy Backend Only (Simplest)

If you just want to get the backend working:

1. **Create a new Web Service on Render**
2. **Settings:**
   - **Root Directory**: Leave empty or set to `backend`
   - **Build Command**: 
     ```bash
     cd backend && pip install --upgrade pip && pip install -r requirements-minimal.txt
     ```
   - **Start Command**: 
     ```bash
     cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

3. **Environment Variables:**
   ```
   PYTHON_VERSION=3.11.9
   DATABASE_URL=your_supabase_url
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

4. **Deploy!**

## If Still Failing: Use Docker

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Then in Render:
- Select "Docker" as runtime
- Dockerfile path: `backend/Dockerfile`

## Recommended: Deploy to Railway Instead

Railway handles Python dependencies better:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway up
```

Railway will automatically:
- Detect Python version
- Install dependencies
- Deploy your app

No Rust compilation issues!

## Quick Test Locally

To verify the minimal requirements work:

```bash
cd backend
pip install -r requirements-minimal.txt
python main.py
```

If it works locally, it will work on Render with Python 3.11.9.
