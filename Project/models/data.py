from pydantic import BaseModel

class Data(BaseModel):
    id: int
    title: str

class UserData(BaseModel):
    title: str