from typing import Any

from app.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from app.schemas.user import UserCreate


class UserRepository:
    async def get_user_by_email(
            self, session: AsyncSession, email: str
            ) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_user_by_phone(
            self, session: AsyncSession, phone: str
            ) -> User | None:
        stmt = select(User).where(User.phone == phone)
        result = await session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(
            self, session: AsyncSession, username: str
            ) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get(self, session: AsyncSession, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        result = await session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, user_in: UserCreate):
        user_data = user_in.model_dump()
        db_user = User(**user_data)
        session.add(db_user)
        await session.flush()
        return db_user

    async def update(
            self, session: AsyncSession, user_id: int, update_data: dict[str, Any]
            ) -> User | None:
        if not update_data:
            return await self.get(session, user_id)
        stmt = (
            update(User).where(User.id == id)
            .values(**update_data)
            .returning(User)
        )
        result = await session.execute(stmt)
        await session.flush()
        return result.scalar_one_or_none()

    async def delete(
            self, session: AsyncSession, user_id: int
    ) -> bool:
        stmt = delete(User).where(User.id == user_id)
        result = await session.execute(stmt)
        await session.flush()
        return result.rowcount > 0


       
