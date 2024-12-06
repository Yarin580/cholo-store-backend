from pydantic import BaseModel


class BuyerCreateDto(BaseModel):
    name: str
    email: str
    phone: str

class BuyerResponseDto(BaseModel):
    id: int
    name: str
    email: str
    phone: str