from fastapi import APIRouter, Depends
from src.services.product_service import ProductService
from src.api.dependencies import get_product_service


router = APIRouter(tags=["catalog"])

@router.get("/catalog")
async def get_all_products(product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_all_products()