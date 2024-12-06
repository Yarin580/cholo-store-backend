from pydantic import BaseModel


class CategoryResponseDto(BaseModel):
    id: int
    name: str

class CategoryCreateDto(BaseModel):
    name: str
