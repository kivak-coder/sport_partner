from datetime import datetime

from sqlalchemy import ARRAY, CheckConstraint, DateTime, Enum, String, func

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from app.enums.levels import SkillLevel
from app.enums.sports import SportType


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint(
            "age >= 14 AND age <= 120",
            name='check_age'
        )
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(45))
    surname: Mapped[str] = mapped_column(String(55))
    username: Mapped[str | None] = mapped_column(
        String(55), unique=True, nullable=True
        )
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255), unique=True)
    age: Mapped[int | None] = mapped_column(default=18)
    fav_sports: Mapped[list[SportType]] = mapped_column(ARRAY(Enum(SportType)), nullable=True)  #сомнительная фигня, но пока пусть будет
    level: Mapped[SkillLevel] = mapped_column(
        Enum(SkillLevel), default=SkillLevel.AMATEUR, index=True
        )
    city: Mapped[str | None] = mapped_column(
        String(20), nullable=True, index=True
        )
    phone: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
        )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    is_active: Mapped[bool] = mapped_column(nullable=False)
