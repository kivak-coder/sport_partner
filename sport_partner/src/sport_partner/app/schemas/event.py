from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator, model_validator
from app.enums.sports import SportType
from app.enums.levels import SkillLevel


class EventCreate(BaseModel):
    title: Annotated[str, Field(max_length=127)]
    event_date: datetime
    max_participants: Annotated[int, Field(ge=2, le=30)]
    sport_type: SportType
    place: str | None = None
    lat: float | None = None
    lon: float | None = None
    level_type: SkillLevel = SkillLevel.AMATEUR

    @field_validator('title')
    def title_name_validate(cls, title: str) -> str:
        title = title.strip()
        if len(title) == 0:
            raise ValueError("title is empty")
        return title

    @field_validator('event_date')  # мб добавить часовые пояса
    def event_date_validate(cls, date: datetime) -> datetime:
        now = datetime.now()
        if now < date:
            return date
        raise ValueError(f"{date} already passed!")

    @model_validator(mode='after')
    def validate_location(self):
        if self.place is not None or (self.lat is not None
                                      and self.lon is not None):
            return self
        raise ValueError("You must specify the place!")


class EventResponse(BaseModel):
    id: int
    creator_id: int
    sport_type: SportType
    title: Annotated[str, Field(max_length=127)]
    event_date: datetime
    place: str | None = None
    lat: float | None = None
    lon: float | None = None
    max_participants: Annotated[int, Field(ge=2, le=30)]
    status: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator('title')
    def title_name_validate(cls, title: str) -> str:
        title = title.strip()
        if len(title) == 0:
            raise ValueError("title is empty")
        return title

    @field_validator('event_date')  # мб добавить часовые пояса
    def event_date_validate(cls, date: datetime) -> datetime:
        now = datetime.now()
        if now < date:
            return date
        raise ValueError(f"{date} already passed!")

    @model_validator(mode='after')
    def validate_location(self):
        if self.place is not None or (self.lat is not None
                                      and self.lon is not None):
            return self
        raise ValueError("You must specify the place!")
  