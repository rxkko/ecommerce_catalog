from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from typing import Annotated

from src.api.dependencies import get_cart_service
from src.dependencies.auth_deps import get_current_user
from src.models.user import User
from src.models.cart_item import CartItem
from src.services.cart_service import CartService
from src.schemas.cart import CartCount


router = APIRouter(prefix="/cart", tags=["Cart"])
CartServiceDep = Annotated[CartService, Depends(get_cart_service)]
templates = Jinja2Templates(directory="src/frontend/templates")

@router.get("/items", summary="Получить все товары из корзины")
async def get_products_from_cart(
    cart_service: CartServiceDep,
    user: User = Depends(get_current_user)                         
):
    return await cart_service.get_products_from_cart(user.id)

@router.get("/count", response_model=CartCount, summary="Количество товаров в корзине")
async def get_cart_count(
    cart_service: CartServiceDep,
    user: User = Depends(get_current_user)
):
    count = await cart_service.get_cart_count(user.id)
    return CartCount(count=count)

@router.delete("/delete", summary="Удалить товар из корзины")
async def delete_from_cart(
    product_id: int,
    cart_service: CartServiceDep,
    user: User = Depends(get_current_user)
):
    return await cart_service.delete_product_from_cart(product_id, user.id)

@router.post("/product/increment", summary="Добавление количества товара в корзине")
async def increment_cart_item(
    product_id: int,
    cart_service: CartServiceDep,
    user: User = Depends(get_current_user)
):
    await cart_service.increment_cart_item(product_id, user.id)
    return {"message": "Количество товара увеличено"}

@router.post("/product/decrement", summary="Уменьшение количества товара в корзине")
async def decrement_cart_item(
    product_id: int,
    cart_service: CartServiceDep,
    user: User = Depends(get_current_user)
):
    await cart_service.decrement_cart_item(product_id, user.id)
    return {"message": "Количество товара уменьшено"}

@router.get("/", include_in_schema=False)
async def html_get_products(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})