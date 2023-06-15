from fastapi import FastAPI, UploadFile, File, Response
from rembg import remove
from PIL import Image
import numpy as np
import io
import logging

logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Server is running."}


@app.post("/{path:path}")
async def remove_background(file: UploadFile = File(...)):
    if path != "removebg":
        return JSONResponse(content={"message": "Not Found"}, status_code=404)

    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        img = np.array(img)
        result = remove(img)
        img = Image.fromarray(result)
        byte_arr = io.BytesIO()
        img.save(byte_arr, format="PNG")
        byte_arr = byte_arr.getvalue()
        return Response(content=byte_arr, media_type="image/png")
    except Exception as e:
        logger.error(e)
        raise
