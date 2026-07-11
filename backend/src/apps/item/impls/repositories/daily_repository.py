from datetime import date

from sqlalchemy import select

from apps.item.models import Daily
from apps.item.repositories import DailyRepository
from settings.impls.sql_alchemy_repositories import SQLAlchemyRepository


class DailyRepositoryImpl(DailyRepository, SQLAlchemyRepository[Daily]):
    cls_model = Daily

    async def select_item_rows(
        self,
        sku: str,
        date_from: date,
        date_to: date,
    ) -> list[Daily]:
        stmt = (
            select(Daily)
            .where(
                Daily.item_id == sku,
                Daily.date >= date_from,
                Daily.date <= date_to,
            )
            .order_by(Daily.date)
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
