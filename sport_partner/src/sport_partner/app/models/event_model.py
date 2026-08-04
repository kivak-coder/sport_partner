from datetime import datetime
from app.db.base import Base
from app.models.user_model import User
from sqlalchemy import DateTime, Enum, String, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.enums.sports import SportType
from app.enums.levels import SkillLevel


class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(primary_key=True)
    creator: Mapped["User"] = relationship(back_populates="events")
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(127))
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True
        )
    max_participants: Mapped[int]
    sport_type: Mapped[SportType] = mapped_column(Enum(SportType), index=True)
    place: Mapped[str | None] = mapped_column(default=None, nullable=True)
    lat: Mapped[float | None] = mapped_column(default=None, nullable=True)
    lon: Mapped[float | None] = mapped_column(default=None, nullable=True)
    level_type: Mapped[SkillLevel] = mapped_column(
        Enum(SkillLevel), default=SkillLevel.AMATEUR, nullable=False
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
        )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    is_active: Mapped[bool] = mapped_column(nullable=False)
