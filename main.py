from database import Base, engine, SessionLocal
from fastapi import FastAPI, File, UploadFile, status, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from models import Dog, Image
from schemas import DogRequest, ImageRequest


# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
async def root():
    return {"message": "Welcome to doggo-api!"}


@app.get("/dogs")
def read_dogs_list(session: Session = Depends(get_session)):
    # get all dogs items
    dogs_list = session.query(Dog).all()

    # close the session
    session.close()

    return dogs_list


@app.get("/dogs/{id}")
def read_dog(id: int, session: Session = Depends(get_session)):
    # get the dog item with the given id
    dog = session.query(Dog).get(id)

    # close the session
    session.close()

    # check if dog item with given id exists
    # If not, raise exception and return 404 not found response
    if not dog:
        raise HTTPException(
            status_code=404, detail=f"dog item with id {id} not found")

    return dog


@app.post("/dogs", status_code=status.HTTP_201_CREATED)
def create_dog(dog: DogRequest, session: Session = Depends(get_session)):
    # create an instance of the Dog database model
    dogdb = Dog(name=dog.name, breed=dog.breed, age=dog.age)

    # add it to the session and commit it
    session.add(dogdb)
    session.commit()

    # close the session
    session.close()

    # return the dog
    return dogdb


@app.put("/dogs/{id}")
def update_dog(id: int, dog_req: DogRequest, session: Session = Depends(get_session)):
    # get the dog item with the given id
    dog = session.query(Dog).get(id)

    # update dog item with the given task
    # (if an item with the given id was found)
    if dog:
        dog.name = dog_req.name
        dog.breed = dog_req.breed
        dog.age = dog_req.age
        session.commit()

    # close the session
    session.close()

    # check if dog item with given id exists
    # If not, raise exception and return 404 not found response
    if not dog:
        raise HTTPException(
            status_code=404, detail=f"dog item with id {id} not found")

    return dog


@app.delete("/dogs/{id}")
def delete_dog(id: int, session: Session = Depends(get_session)):
    # get the dog item with the given id
    dog = session.query(Dog).get(id)

    # if dog item with given id exists, delete it from the database. Otherwise raise 404 error
    if dog:
        session.delete(dog)
        session.commit()
        session.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"dog item with id {id} not found")

    return None


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
