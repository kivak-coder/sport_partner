from typing import Any

from sqlalchemy import delete, select, update
from app.models.event_model import Event
from sqlalchemy.ext.asyncio import AsyncSession
from app.enums.sports import SportType
from app.enums.levels import SkillLevel
from app.schemas.event import EventCreate


class EventRepository:
    async def get(self, session: AsyncSession, id: int) -> Event | None:
        stmt = select(Event).where(Event.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_creator(self, session: AsyncSession, creator_id: int) -> Event | None:
        stmt = select(Event).where(Event.creator_id == creator_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # async def check_if_active(self, session: AsyncSession, event_id: int) -> bool:
    #     return self.get(session, event_id)

    async def get_by_sport_type(
            self, session: AsyncSession, sport_type: SportType
            ):
        stmt = select(Event).where(Event.sport_type == sport_type)
        result = await session.execute(stmt)
        return result.scalars()

    async def get_by_level(self, session: AsyncSession, level: SkillLevel):
        stmt = select(Event).where(Event.level_type == level)
        result = await session.execute(stmt)
        return result.scalars()

    async def insert(self, session: AsyncSession, event_in: EventCreate):
        event_data = event_in.model_dump()
        db_event = Event(**event_data)
        session.add(db_event)
        await session.flush()
        return db_event

    async def update(self, session: AsyncSession, event_id: int, update_data: dict[str, Any]):
        if not update_data:
            return await self.get(session, event_id)
        stmt = (
            update(Event).where(Event.id == id)
            .values(**update_data)
            .returning(Event)
        )
        result = await session.execute(stmt)
        await session.flush()
        return result.scalar_one_or_none()

    async def delete(self, session: AsyncSession, event_id: int) - > bool:
        stmt = delete(Event).where(Event.id == event_id)
        result = await session.execute(stmt)
        await session.flush()
        return result.rowcount > 0


