from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.templating import Jinja2Templates
from typing import Annotated, List, Optional

from src.services.product_service import ProductService
from src.api.dependencies import get_product_service
from src.dependencies.auth_deps import get_current_user, admin_required
from src.schemas.product import ProductCreate, ProductRead, ProductUpdate, ProductCategory
from src.models.user import User

router = APIRouter(prefix="/catalog", tags=["Catalog"])
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
templates = Jinja2Templates(directory="src/frontend/templates")


@router.get("/api", summary="Получить список товаров")
async def api_get_products(
    product_service: ProductServiceDep,
    limit: int = Query(10, ge=1, description="Лимит товаров"),
    offset: int = Query(0, ge=0, description="Смещение")
):
    return await product_service.get_all_products(limit=limit, offset=offset)


@router.get("/{product_id}", response_model=ProductRead, summary="Получить товар по ID")
async def get_product_by_id(
    product_id: int,
    product_service: ProductServiceDep
):
    return await product_service.get_product_by_id(product_id)


@router.post("/product/create", response_model=ProductRead, status_code=status.HTTP_201_CREATED, summary="Создать новый товар")
async def create_product(
    product_data: ProductCreate,
    product_service: ProductServiceDep
):
    return await product_service.create_product(product_data)

@router.post("/{product_id}/add", summary="Добавить товар в корзину")
async def add_product_to_cart(
    product_id: int,
    product_service: ProductServiceDep,  
    user: User = Depends(get_current_user)
):
    return await product_service.add_product_to_cart(product_id, user.id)

@router.put("/{product_id}", response_model=ProductRead, summary="Обновить товар")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: ProductServiceDep
):
    return await product_service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить товар")
async def delete_product(
    product_id: int,
    product_service: ProductServiceDep
):
    await product_service.delete_product(product_id)
    return None

@router.get("/api/filter/", response_model=List[ProductRead], summary="Фильтр товаров")
async def get_products_by_categories_api(
    product_service: ProductServiceDep,
    categories: List[ProductCategory] = Query(...),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    print(categories, min_price, max_price)
    products = await product_service.get_products_by_categories(
        categories,
        min_price=min_price,
        max_price=max_price
    )
    return products


@router.get("/", include_in_schema=False)
async def html_get_products(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})