from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from database import get_db
from models import Product, InventoryHistory, User
from auth import get_current_user, require_admin

router = APIRouter(prefix="/api/products", tags=["products"])

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: str = ""
    category: str = ""
    price: float
    quantity: int = 0
    min_stock_level: int = 10
    supplier: str = ""

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    category: str = None
    price: float = None
    quantity: int = None
    min_stock_level: int = None
    supplier: str = None

class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    description: Optional[str] = ""
    category: Optional[str] = ""
    price: float
    quantity: int
    min_stock_level: int
    supplier: Optional[str] = ""
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    id: int
    product_id: int
    action: str
    quantity_change: int
    performed_by: Optional[str] = ""
    notes: Optional[str] = ""
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
def get_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    return query.all()

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    categories = db.query(Product.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Log history
    history = InventoryHistory(
        product_id=db_product.id,
        action="added",
        quantity_change=product.quantity,
        performed_by=current_user.username,
        notes=f"Product added: {product.name}"
    )
    db.add(history)
    db.commit()
    
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    old_quantity = db_product.quantity
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    
    # Log history
    quantity_change = db_product.quantity - old_quantity
    history = InventoryHistory(
        product_id=db_product.id,
        action="updated",
        quantity_change=quantity_change,
        performed_by=current_user.username,
        notes=f"Product updated: {db_product.name}"
    )
    db.add(history)
    db.commit()
    
    return db_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Log history before deletion
    history = InventoryHistory(
        product_id=db_product.id,
        action="deleted",
        quantity_change=0,
        performed_by=current_user.username,
        notes=f"Product deleted: {db_product.name}"
    )
    db.add(history)
    
    db.delete(db_product)
    db.commit()
    
    return {"message": "Product deleted successfully"}

@router.get("/{product_id}/history", response_model=List[HistoryResponse])
def get_product_history(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    history = db.query(InventoryHistory).filter(
        InventoryHistory.product_id == product_id
    ).order_by(InventoryHistory.created_at.desc()).all()
    return history
