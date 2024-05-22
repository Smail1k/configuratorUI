from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    username: str
    fullName: str
    password: str | None
    autoIn: bool
    role: bool

    model_config = ConfigDict(from_attributes=True)
