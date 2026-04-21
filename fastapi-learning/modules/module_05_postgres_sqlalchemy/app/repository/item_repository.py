from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item


class ItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, *, limit: int, offset: int) -> tuple[list[Item], int]:
        items_q = select(Item).order_by(Item.id).limit(limit).offset(offset)
        total_q = select(func.count()).select_from(Item)
        items = (await self.session.execute(items_q)).scalars().all()
        total = (await self.session.execute(total_q)).scalar_one()
        return list(items), int(total)

    async def get(self, item_id: int) -> Optional[Item]:
        return await self.session.get(Item, item_id)

    async def add(self, *, name: str, description: Optional[str], price_cents: int) -> Item:
        item = Item(name=name, description=description, price_cents=price_cents)
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def delete(self, item_id: int) -> bool:
        item = await self.session.get(Item, item_id)
        if item is None:
            return False
        await self.session.delete(item)
        await self.session.flush()
        return True
