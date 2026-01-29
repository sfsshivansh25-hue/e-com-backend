import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()
        return product


    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
       result = await self.session.execute(
            select(Product).where(
                Product.id == product_id,
                Product.is_active.is_(True)
            )
        )
       return result.scalar_one_or_none()

    async def list(self, limit: int, offset: int) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .where(Product.is_active.is_(True))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def update(self, product: Product) -> Product:
        await self.session.flush()
        return product


    async def soft_delete(self, product: Product) -> None:
        product.is_active = False
        await self.session.flush()