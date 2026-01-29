import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product
from app.repositories.product import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ProductRepository(session)

    async def create_product(
        self,
        name: str,
        description: str | None,
        price: Decimal,
        stock: int,
    ) -> Product:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
        )

        await self.repo.create(product)
        await self.session.commit()   # ✅ commit belongs here
        return product

    async def get_product(self, product_id: uuid.UUID) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return product

    async def list_products(self, limit: int, offset: int) -> list[Product]:
        return await self.repo.list(limit=limit, offset=offset)

    async def update_product(
        self,
        product: Product,
        name: str | None,
        description: str | None,
        price: Decimal | None,
        stock: int | None,
    ) -> Product:
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock

        await self.session.commit()   # ✅ REQUIRED
        return product

    async def delete_product(self, product: Product) -> None:
        await self.repo.soft_delete(product)
        await self.session.commit()   # ✅ REQUIRED
