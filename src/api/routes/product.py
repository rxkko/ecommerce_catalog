from fastapi import APIRouter, Depends, Query, HTTPException, status, Request
from fastapi_cache.decorator import cache
from typing import Annotated, Optional, List
from src.services.product_service import ProductService
from src.api.dependencies import get_product_service
from src.schemas.product import ProductUpdate, ProductBase
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["catalog"])
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
templates = Jinja2Templates(directory="src/static")

@router.get("/catalog")
# @cache(expire=600)
async def get_all_products(
    request: Request,
    product_service: ProductServiceDep,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)):
    products = await product_service.get_all_products(limit=limit, offset=offset)
    print(products.items)
    return templates.TemplateResponse(
        "catalog.html",
        {"request": request, "products": products}
    )

@router.get("/catalog/{product_id}")
async def get_product_by_id(product_id: int, product_service: ProductServiceDep):
    return await product_service.get_product_by_id(product_id)

@router.post("/catalog/create")
async def create_product(product_data: ProductBase, product_service: ProductServiceDep):
    return await product_service.create_product(product_data)

@router.put("/catalog/update/{product_id}")
async def update_product(product_id: int, product_data: ProductUpdate, product_service: ProductServiceDep):
    return await product_service.update_product(product_id, product_data)

@router.delete("/catalog/delete/{product_id}")
async def delete_product(product_id: int, product_service: ProductServiceDep):
    return await product_service.delete_product(product_id)

