from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.templating import Jinja2Templates
from typing import Annotated

from src.services.product_service import ProductService
from src.api.dependencies import get_cart_service
from src.dependencies.auth_deps import get_current_user
from src.schemas.product import ProductCreate, ProductRead, ProductUpdate, ProductCategory
from src.models.user import User
from src.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])
CartServiceDep = Annotated[CartService, Depends(get_cart_service)]
templates = Jinja2Templates(directory="src/frontend/templates")

@router.get("/items")
async def get_products_from_cart(
    cart_service: CartServiceDep,
    _: User = Depends(get_current_user)                         
):
    return await cart_service.get_products_from_cart()