from fastapi import APIRouter, Depends, HTTPException, status
from src.services.product_service import ProductService
from src.api.dependencies import get_product_service, get_user_by_role
from src.schemas.product import ProductUpdate, ProductBase


router = APIRouter(tags=["catalog"])

@router.get("/catalog")
async def get_all_products(product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_all_products()

@router.get("/catalog/{product_id}")
async def get_product_by_id(product_id: int, product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_product_by_id(product_id)

@router.post("/catalog/create")
async def create_product(product_data: ProductBase, product_service: ProductService = Depends(get_product_service)):
    return await product_service.create_product(product_data)

@router.put("/catalog/update/{product_id}")
async def update_product(product_id: int, product_data: ProductUpdate, product_service: ProductService = Depends(get_product_service)):
    return await product_service.update_product(product_id, product_data)

@router.delete("/catalog/delete/{product_id}")
async def delete_product(product_id: int,
                          product_service: ProductService = Depends(get_product_service),
                          user: bool = Depends(get_user_by_role)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для удаления этого продукта."
        )
    return await product_service.delete_product(product_id)