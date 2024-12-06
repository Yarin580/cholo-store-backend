from pydantic import BaseModel


class BuyerSchema(BaseModel):
    id: int = None
    name : str
    email : str
    phone : str
