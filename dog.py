import aiofiles

from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter


class Dog(BaseModel):
    id: int
    name: str
    breed: str


app = FastAPI()
app.include_router(CRUDRouter(schema=Dog))
image_id = 1


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
