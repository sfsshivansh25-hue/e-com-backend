from fastapi import APIRouter
from app.api.v1.products import router as products_router
from app.api.v1.cart import router as cart_router
from app.api.v1.auth import router as auth_router
from app.api.v1.orders import router as orders_router
from app.api.v1.checkout import router as checkout_router
from app.api.v1 import payments

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(products_router)
api_router.include_router(auth_router)
api_router.include_router(cart_router)
api_router.include_router(orders_router)
api_router.include_router(checkout_router)
api_router.include_router(payments.router)



