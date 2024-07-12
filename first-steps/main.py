from enum import Enum

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated

class Exercise(BaseModel):
    name: Annotated[str, Query(max_length=10)]
    reps: int
    notes: str | None = None
    series: int


app = FastAPI()

class GameCategory(str, Enum):
    shooter = "shooter"



@app.post("/add")
async def add_training(exercise:Exercise):
    return exercise

@app.get("/")
async def root():
    return ("data",212)


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results