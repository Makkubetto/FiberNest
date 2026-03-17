from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.utils.deps import get_db, get_current_user, get_current_seller
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = Order(
        user_id          = current_user.id,
        payment_method   = payload.payment_method,
        delivery_method  = payload.delivery_method,
        delivery_address = payload.delivery_address,
        notes            = payload.notes,
        subtotal         = payload.subtotal,
        shipping_fee     = payload.shipping_fee,
        total            = payload.total,
        status           = "Pending",
    )
    db.add(order)
    db.flush()

    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        product.stock -= item.quantity
        db.add(OrderItem(
            order_id   = order.id,
            product_id = item.product_id,
            quantity   = item.quantity,
            price      = item.price,
        ))

    db.commit()
    db.refresh(order)
    return _serialize(order)

@router.get("/my", response_model=List[OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return [_serialize(o) for o in orders]

@router.get("", response_model=List[OrderOut])
def get_all_orders(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_seller)
):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return [_serialize(o) for o in orders]

@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Access denied")
    return _serialize(order)

@router.patch("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in ("Pending", "Processing"):
        raise HTTPException(status_code=400, detail="Order cannot be cancelled at this stage")
    order.status = "Cancelled"
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
    db.commit()
    db.refresh(order)
    return _serialize(order)

@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_seller)
):
    valid = ("Pending", "Processing", "Shipped", "Delivered", "Cancelled")
    if payload.status not in valid:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid}")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = payload.status
    db.commit()
    db.refresh(order)
    return _serialize(order)

def _serialize(order: Order) -> dict:
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "payment_method": order.payment_method,
        "delivery_method": order.delivery_method,
        "delivery_address": order.delivery_address,
        "notes": order.notes,
        "subtotal": order.subtotal,
        "shipping_fee": order.shipping_fee,
        "total": order.total,
        "created_at": order.created_at,
        "items": [
            {
                "id": i.id,
                "product_id": i.product_id,
                "quantity": i.quantity,
                "price": i.price,
                "name": i.product.name if i.product else None,
            }
            for i in order.items
        ],
    }