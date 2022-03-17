from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Create a sqlite engine instance
engine = create_engine("sqlite:///dogs.db")

# Create a DeclarativeMeta instance
Base = declarative_base()


class Dog(Base):
    # Define To Do class inheriting from Base
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30), nullable=False)
    breed = Column(String(50))
    image = Column(String(100))


# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to doggo-api!"}


@app.get("/dogs")
def read_dogs_list():
    return "read dogs list"


@app.get("/dogs/{id}")
def read_dog(id: int):
    return "read dogs item with id {id}"


@app.post("/dogs", status_code=status.HTTP_201_CREATED)
def create_dog():
    return "create dogs item"


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
