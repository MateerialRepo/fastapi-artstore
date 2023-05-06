import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from mangum import Mangum


class Art(BaseModel):
    id: int
    title: str
    main_reference_number: str
    department_title: str
    artist_title: str


ARTS_FILE = "arts.json"
ARTS = []

if os.path.exists(ARTS_FILE):
    with open(ARTS_FILE, "r") as f:
        ARTS = json.load(f)

app = FastAPI()
handler = Mangum(app)


@app.get("/")
async def root():
    return {"message": "Welcome to my ARTStore app!"}


@app.get("/random-art")
async def random_art():
    return random.choice(ARTS)


@app.get("/list-ARTS")
async def list_ARTS():
    return {"ARTS": ARTS}


@app.get("/art_by_index/{index}")
async def art_by_index(index: int):
    if index < len(ARTS):
        return ARTS[index]
    else:
        raise HTTPException(404, f"Art index {index} out of range ({len(ARTS)}).")


@app.post("/add-art")
async def add_art(art: Art):
    art.id = uuid4().hex
    json_art = jsonable_encoder(art)
    ARTS.append(json_art)

    with open(ARTS_FILE, "w") as f:
        json.dump(ARTS, f)

    return {"art_id": art.art_id}


@app.get("/get-art")
async def get_art(art_id: str):
    for art in ARTS:
        if art.id == art_id:
            return art

    raise HTTPException(404, f"Art ID {art_id} not found in database.")
