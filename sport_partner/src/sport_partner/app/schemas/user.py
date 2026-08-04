import re
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic import StringConstraints, field_validator, model_validator
from app.enums.sports import SportType
from app.enums.levels import SkillLevel


def check_if_empty(name: str) -> str:
    name = name.strip()
    if len(name) == 0:
        raise ValueError("title is empty")
    return name


class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=45)]
    surname: Annotated[str, Field(min_length=2, max_length=55)]
    username: Annotated[str | None, Field(min_length=2, max_length=55)] = None
    email: EmailStr | None = None
    age: Annotated[int | None, Field(ge=14, le=120)] = 18
    fav_sports: set[SportType] | None = None
    password: Annotated[str, Field(min_length=8, max_length=20)]
    level: SkillLevel | None = SkillLevel.AMATEUR
    city: Annotated[str | None, Field(min_length=2, max_length=45)] = None
    phone: Annotated[str | None,
                     StringConstraints(pattern=r"^\+?[1-9]\d{7,14}$")] = None

    @model_validator(mode='after')
    def check_if_login_exists(self):
        if (self.username is not None or self.phone is not None
                or self.email is not None):
            return self
        raise ValueError("no login data")

    @field_validator('name')
    def validate_name(self, name: str) -> str:
        return check_if_empty(name)

    @field_validator('surname')
    def validate_surname(self, surname: str) -> str:
        return check_if_empty(surname)

    @field_validator('username')
    def validate_username(self, username: str) -> str:
        return check_if_empty(username)

    @field_validator('password')
    def validate_password(self, password: str) -> str:
        password = check_if_empty(password)
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain an uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain a lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain a digit")
        return password


class UserResponse(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=2, max_length=45)]
    surname: Annotated[str, Field(min_length=2, max_length=55)]
    age: Annotated[int | None, Field(ge=14, le=120)] = 18
    fav_sports: set[SportType] | None
    level: SkillLevel | None = SkillLevel.AMATEUR
    city: Annotated[str | None, Field(min_length=2, max_length=45)] = None

    model_config = ConfigDict(from_attributes=True)
