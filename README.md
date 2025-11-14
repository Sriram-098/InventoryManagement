# Inventory Management System

A complete inventory management system with React frontend and FastAPI backend connected to Supabase PostgreSQL.

## Features

- Product management (CRUD operations)
- Real-time inventory tracking
- Low stock alerts
- Dashboard with statistics
- Responsive UI

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## API Endpoints

- GET /api/products - Get all products
- GET /api/products/{id} - Get product by ID
- POST /api/products - Create new product
- PUT /api/products/{id} - Update product
- DELETE /api/products/{id} - Delete product

## Database Schema

The system uses a `products` table with the following fields:
- id (Primary Key)
- name
- sku (Unique)
- description
- category
- price
- quantity
- min_stock_level
- created_at
- updated_at
