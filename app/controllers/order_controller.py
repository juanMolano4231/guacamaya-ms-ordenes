from fastapi import Request, HTTPException
from app.models.order_model import *

def create_order_controller(request: Request, body):
    user = request.state.user
    order = create_order(user["id"], body["items"])
    return order

def get_orders_controller(request: Request):
    user = request.state.user
    return get_orders_by_user(user["id"])

def get_order_detail_controller(request: Request, order_id: int):
    user = request.state.user
    order = get_order_detail(order_id, user["id"], user["role"] == "ADMIN")

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

def update_status_controller(request: Request, order_id: int, body):
    if request.state.user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden")

    order = update_order_status(order_id, body["status"])

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if "error" in order:
        raise HTTPException(status_code=400, detail=order["error"])

    return order