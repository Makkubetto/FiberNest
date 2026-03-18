from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Import all models so SQLAlchemy creates the tables
import app.models.user
import app.models.product
import app.models.order
import app.models.storefront
import app.models.verification       # ← new

# Import all routers
from app.routers import auth, users, products, orders, storefront, seller

# Auto-create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FiberNest API",
    description="Backend API for FiberNest coconut coir e-commerce platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                   "http://localhost:5500",
                   "http://127.0.0.1:5500",
                   "http://localhost:8000",
                   "http://127.0.0.1:8000",
                   "null",
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(storefront.router)
app.include_router(seller.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "FiberNest API is running ✅"}