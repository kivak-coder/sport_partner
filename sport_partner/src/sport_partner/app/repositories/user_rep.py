from app.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


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

