from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
import app.models.user, app.models.product, app.models.order, app.models.storefront
from app.routers import auth, users, products, orders, storefront, seller

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FiberNest API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(storefront.router)
app.include_router(seller.router)

@app.get("/")
def root():
    return {"message": "FiberNest API is running"}