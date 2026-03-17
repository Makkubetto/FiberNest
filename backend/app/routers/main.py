from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from app.database import Base, engine
 
# Import all models so SQLAlchemy can create the tables
import app.models.user
import app.models.product
import app.models.order
import app.models.storefront

# Import all routers
from app.routers import auth, users, products, orders, storefront, seller

# Create all tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FiberNest API",
    description="Backend API for FiberNest coconut coir e-commerce platform",
    version="1.0.0",
)

# Allow frontend HTML files to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# Register all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(storefront.router)
app.include_router(seller.router)
 
@app.get("/", tags=["Root"])
def root():
    return {"message": "FiberNest API is running ✅"}
