from fastapi import Depends

from apps.item.impls.repositories.daily_repository import DailyRepositoryImpl
from apps.item.impls.repositories.item_repository import ItemRepostioryImpl
from apps.item.repositories import DailyRepository, ItemRepository
from apps.item.services import ItemService
from apps.item.impls.services.item_service import ItemServiceImpl
from settings.dependencies import get_sql_manager
from settings.db_manager import DbManager


def get_item_repository(
    db_manager: DbManager = Depends(get_sql_manager),
) -> ItemRepository:
    return ItemRepostioryImpl(
        session=db_manager.session
    )


def get_daily_repository(
    db_manager: DbManager = Depends(get_sql_manager),
) -> DailyRepository:
    return DailyRepositoryImpl(
        session=db_manager.session
    )


def get_item_service(
    repostiory: ItemRepository = Depends(get_item_repository),
    daily_repository: DailyRepository = Depends(get_daily_repository),
) -> ItemService:
    return ItemServiceImpl(
        repository=repostiory,
        daily_repository=daily_repository,
    )
