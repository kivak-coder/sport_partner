from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class eventParticipant(Base):
    __tablename__ = 'event_participants'
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete="CASCADE"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    user = relationship("User")
    event = relationship("Event")
