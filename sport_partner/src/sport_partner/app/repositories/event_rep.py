from typing import Any, Sequence
from sqlalchemy import delete, func, select, update
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

    async def get_by_creator(
            self, session: AsyncSession, creator_id: int
            ) -> Event | None:
        stmt = select(Event).where(Event.creator_id == creator_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def check_if_active(
            self, session: AsyncSession, event_id: int
            ) -> bool:
        stmt = select(Event.is_active).where(Event.id == event_id)
        result = await session.execute(stmt)
        if (result is None):
            raise Exception("No such event")
        return bool(result.scalar_one_or_none())

    async def get_by_sport_type(
            self, session: AsyncSession, sport_type: SportType,
            skip: int = 0, limit: int = 100,
            ) -> Sequence[Event]:
        stmt = (select(Event)
                .where(Event.sport_type == sport_type)
                .offset(skip).limit(limit))
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_by_level(
            self, session: AsyncSession, level: SkillLevel
            ) -> Sequence[Event]:
        stmt = select(Event).where(Event.level_type == level)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_events(self, session: AsyncSession,
                         sport_type: SportType | None = None,
                         level: SkillLevel | None = None,
                         city: str | None = None, skip: int = 0,
                         limit: int = 100
                         ) -> Sequence[Event]:
        stmt = select(Event)
        if sport_type:
            stmt = stmt.where(Event.sport_type == sport_type)
        if level:
            stmt = stmt.where(Event.level_type == level)
        if city:
            stmt = stmt.where(Event.place == city)
        stmt = stmt.offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def insert(
            self, session: AsyncSession, event_in: EventCreate
            ) -> Event:
        event_data = event_in.model_dump()
        db_event = Event(**event_data)
        session.add(db_event)
        await session.flush()
        return db_event

    async def update(
            self, session: AsyncSession, event_id: int,
            update_data: dict[str, Any]
            ) -> Event | None:
        if not update_data:
            return await self.get(session, event_id)
        stmt = (
            update(Event).where(Event.id == event_id)
            .values(**update_data)
            .returning(Event)
        )
        result = await session.execute(stmt)
        await session.flush()
        return result.scalar_one_or_none()

    async def delete(self, session: AsyncSession, event_id: int) -> bool:
        stmt = delete(Event).where(Event.id == event_id).returning(Event.id)
        result = await session.execute(stmt)
        await session.flush()
        return result.scalar_one_or_none() is None

    async def count_events(self, session: AsyncSession,
                           sport_type: SportType | None = None,
                           level: SkillLevel | None = None,
                           city: str | None = None) -> int:
        stmt = select(func.count(Event.id))
        if sport_type:
            stmt = stmt.where(Event.sport_type == sport_type)
        if level:
            stmt = stmt.where(Event.level_type == level)
        if city:
            stmt = stmt.where(Event.place == city)
        result = await session.execute(stmt)
        return result.scalar_one()
