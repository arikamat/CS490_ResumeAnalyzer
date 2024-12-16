from pydantic import BaseModel


class CategoricalKeyword(BaseModel):
    skills: list[str]
    experience: list[str]
    education: list[str]
