from fastapi import Depends

from apps.item.impls.repositories.item_repository import ItemRepostioryImpl
from apps.item.repositories import ItemRepository
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


def get_item_service(
    repostiory: ItemRepository = Depends(get_item_repository)
) -> ItemService:
    return ItemServiceImpl(
        repository=repostiory,
    )
