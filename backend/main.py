from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from routes import products, auth, reports
from models import User
from auth import get_password_hash

app = FastAPI(title="Wholesale Shop Inventory Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Create default admin user if not exists
def create_default_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@wholesale.com",
                password=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("Default admin user created: username=admin, password=admin123")
    finally:
        db.close()

create_default_admin()

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Wholesale Shop Inventory Management API"}
