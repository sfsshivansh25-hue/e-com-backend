import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services.product import ProductService
from app.api.deps import require_admin

router = APIRouter(prefix="/products", tags=["products"])

#Auth dependency placeholder

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    product = await service.create_product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
    )
    return product

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    try:
        return await service.get_product(product_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@router.put("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_admin)])
async def update_product(
    product_id: uuid.UUID,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    try:
        product = await service.get_product(product_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return await service.update_product(
        product=product,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
    )
    
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    try:
        product = await service.get_product(product_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    await service.delete_product(product)
    return None

