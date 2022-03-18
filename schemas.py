from pydantic import BaseModel


class DogRequest(BaseModel):
    name: str
    breed: str
    age: int


class ImageRequest(BaseModel):
    dog_name: str
    path: str
