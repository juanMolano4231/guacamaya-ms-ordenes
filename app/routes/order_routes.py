from fastapi import APIRouter, Request, Depends
from app.middleware.auth import authenticate
from app.controllers.order_controller import *

router = APIRouter()

def auth_dep(request: Request):
    authenticate(request)

@router.post("/orders")
def create_order_route(request: Request, body: dict, _: None = Depends(auth_dep)):
    return create_order_controller(request, body)

@router.get("/orders")
def get_orders_route(request: Request, _: None = Depends(auth_dep)):
    return get_orders_controller(request)

@router.get("/orders/{order_id}")
def get_order_detail_route(order_id: int, request: Request, _: None = Depends(auth_dep)):
    return get_order_detail_controller(request, order_id)

@router.put("/orders/{order_id}/status")
def update_status_route(order_id: int, request: Request, body: dict, _: None = Depends(auth_dep)):
    return update_status_controller(request, order_id, body)