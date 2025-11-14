from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List
from database import get_db
from models import Product, InventoryHistory, User
from auth import require_admin

router = APIRouter(prefix="/api/reports", tags=["reports"])

class StatsResponse(BaseModel):
    total_products: int
    total_value: float
    low_stock_items: int
    out_of_stock_items: int
    total_categories: int

class CategoryStats(BaseModel):
    category: str
    product_count: int
    total_value: float

class RecentActivity(BaseModel):
    id: int
    product_id: int
    action: str
    performed_by: str
    notes: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    products = db.query(Product).all()
    
    total_products = len(products)
    total_value = sum(p.price * p.quantity for p in products)
    low_stock_items = sum(1 for p in products if p.quantity <= p.min_stock_level and p.quantity > 0)
    out_of_stock_items = sum(1 for p in products if p.quantity == 0)
    total_categories = db.query(Product.category).distinct().count()
    
    return {
        "total_products": total_products,
        "total_value": total_value,
        "low_stock_items": low_stock_items,
        "out_of_stock_items": out_of_stock_items,
        "total_categories": total_categories
    }

@router.get("/category-stats", response_model=List[CategoryStats])
def get_category_stats(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    results = db.query(
        Product.category,
        func.count(Product.id).label('product_count'),
        func.sum(Product.price * Product.quantity).label('total_value')
    ).group_by(Product.category).all()
    
    return [
        {
            "category": r.category or "Uncategorized",
            "product_count": r.product_count,
            "total_value": float(r.total_value or 0)
        }
        for r in results
    ]

@router.get("/recent-activity", response_model=List[RecentActivity])
def get_recent_activity(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    since_date = datetime.utcnow() - timedelta(days=days)
    history = db.query(InventoryHistory).filter(
        InventoryHistory.created_at >= since_date
    ).order_by(InventoryHistory.created_at.desc()).limit(50).all()
    
    return history

@router.get("/low-stock", response_model=List[dict])
def get_low_stock_report(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    products = db.query(Product).filter(
        Product.quantity <= Product.min_stock_level
    ).all()
    
    return [
        {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "category": p.category,
            "quantity": p.quantity,
            "min_stock_level": p.min_stock_level,
            "supplier": p.supplier
        }
        for p in products
    ]
