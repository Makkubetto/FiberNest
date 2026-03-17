from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.utils.deps import get_db, get_current_seller
from app.models.order import Order, OrderItem
from app.models.product import Product

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _=Depends(get_current_seller)):
    today = date.today()
    today_orders = db.query(Order).filter(func.date(Order.created_at) == today).all()
    month_orders = db.query(Order).filter(
        func.extract("month", Order.created_at) == today.month,
        func.extract("year",  Order.created_at) == today.year
    ).all()
    return {
        "today_sales":   sum(o.total for o in today_orders),
        "today_orders":  len(today_orders),
        "month_sales":   sum(o.total for o in month_orders),
        "month_orders":  len(month_orders),
        "total_products": db.query(Product).count(),
        "low_stock":     db.query(Product).filter(Product.stock <= 10).count(),
    }

@router.get("/orders/recent")
def recent_orders(db: Session = Depends(get_db), _=Depends(get_current_seller)):
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(10).all()
    return [{"id": f"ORD-{o.id:04d}", "buyer": o.user.full_name, "total": o.total, "status": o.status, "date": o.created_at.strftime("%b %d")} for o in orders]

@router.get("/reports")
def get_reports(db: Session = Depends(get_db), _=Depends(get_current_seller)):
    today = date.today()
    today_orders = db.query(Order).filter(func.date(Order.created_at) == today).all()
    month_orders = db.query(Order).filter(func.extract("month", Order.created_at) == today.month, func.extract("year", Order.created_at) == today.year).all()
    return {
        "today":  {"total": sum(o.total for o in today_orders),  "orders": len(today_orders),  "avg": sum(o.total for o in today_orders)  / max(len(today_orders), 1)},
        "month":  {"total": sum(o.total for o in month_orders),  "orders": len(month_orders),  "avg": sum(o.total for o in month_orders)  / max(len(month_orders), 1)},
    }