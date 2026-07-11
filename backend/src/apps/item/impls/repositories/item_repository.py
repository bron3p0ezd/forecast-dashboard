from sqlalchemy import select

from apps.item.models import Item
from apps.item.repositories import ItemRepository
from settings.impls.sql_alchemy_repositories import SQLAlchemyRepository


class ItemRepostioryImpl(ItemRepository, SQLAlchemyRepository[Item]):
    cls_model = Item

    async def select_item_by_sku(
        self,
        sku: str,
    ) -> Item | None:
        stmt = select(Item).where(Item.item_id == sku)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def select_items_by_subcategory(
        self,
        subcategory: str | None
    ) -> list[Item]:
        stmt = (
            select(Item)
            .order_by(Item.item_id)
        )

        if subcategory is not None:
            stmt = stmt.where(
                Item.subcategory.ilike(f"%{subcategory}%")
            )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
