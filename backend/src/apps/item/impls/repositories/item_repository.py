from sqlalchemy import select

from apps.item.models import Item
from apps.item.repositories import ItemRepository
from settings.impls.sql_alchemy_repositories import SQLAlchemyRepository


class ItemRepostioryImpl(ItemRepository, SQLAlchemyRepository[Item]):
    cls_model = Item

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
                Item.subcategory == subcategory,
            )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
