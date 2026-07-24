from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    AMATEUR = "amateur"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"
