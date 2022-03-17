from database import Base, engine, Dog
from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session


class DogRequest(BaseModel):
    # Create DogRequest Base Model
    name: str
    breed: str
    age: int
    image: str


# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to doggo-api!"}


@app.get("/dogs")
def read_dogs_list():
     # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all dogs items
    dogs_list = session.query(Dog).all()

    # close the session
    session.close()

    return dogs_list


@app.get("/dogs/{id}")
def read_dog(id: int):
    return "read dogs item with id {id}"


@app.post("/dogs", status_code=status.HTTP_201_CREATED)
def create_dog(dog: DogRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the Dog database model
    dogdb = Dog(name=dog.name, breed=dog.breed, age=dog.age)

    # add it to the session and commit it
    session.add(dogdb)
    session.commit()

    # grab the id given to the object from the database
    id = dogdb.id

    # close the session
    session.close()

    # return the id
    return f"created dog item with id {id}"


@app.put("/dogs/{id}")
def update_dog(id: int):
    return "update dogs item with id {id}"


@app.delete("/dogs/{id}")
def delete_dog(id: int):
    return "delete dogs item with id {id}"


@app.get("/images/{id}")
async def get_image(id: int):
    return FileResponse(f"./static/images/{id}.png")


@app.post("/images")
async def upload_file(file: UploadFile = File(...)):
    global image_id
    file_path = f"./static/images/{image_id}.png"
    with open(file_path, 'wb') as image:
        content = await file.read()
        image.write(content)
        image.close()
    image_id += 1
    return JSONResponse(content={"filename": f"{image_id}.png"},
                        status_code=201)
