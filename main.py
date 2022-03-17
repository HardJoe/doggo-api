import aiofiles

from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter


app = FastAPI()
# dogs = {
#     "id": 1,
#     "name": "Lady",
#     "age": 3,
#     "breed": "American Cocker Spaniel"
# }
# , {
#     "name": "Tramp",
#     "age": 3,
#     "gender": 1,
#     "breed": "mixed",
#     "weight": 8
# }


class Dog(BaseModel):
    id: int
    name: str
    breed: str


# lady = Dog(id=1, name="Lady", age=3, breed="spaniel")
# tramp = Dog(id=2, name="Tramp", age=5, breed="mixed")
# dogs = [lady, tramp]
dogs = []


@app.get("/")
async def root():
    return {"message": "Welcome to doggo-api!"}


@app.get("/dogs")
async def get_dogs():
    return {data: dogs


@ app.get("/dogs/{id}")
async def get_dog(id: int):
    if any(dog for dog in dogs if dog.id == id):
        raise HTTPException(status_code=404, detail="Dog not found")
    return {"dog": dogs[id]}


# @app.post("/dogs")
# def calculate(m: str = Form(...), f: str = Form(...)):
#     return {
#         "male": m,
#         "female": f,
#         "lovePercentage": randint(0, 100)
#     }


# @app.post("/loveanalysis")
# def analyze(person: Person):
#     return {
#         "name": person.name,
#         "age": person.age,
#         "loveChance": randint(0, 100)
#     }
