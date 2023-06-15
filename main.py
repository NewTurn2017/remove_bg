from fastapi import FastAPI, UploadFile, File, Response
from rembg import remove
from PIL import Image
import numpy as np
import io

app = FastAPI()


@app.post("/removebg")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img = np.array(img)
    result = remove(img)
    img = Image.fromarray(result)
    byte_arr = io.BytesIO()
    img.save(byte_arr, format="PNG")
    byte_arr = byte_arr.getvalue()
    return Response(content=byte_arr, media_type="image/png")
