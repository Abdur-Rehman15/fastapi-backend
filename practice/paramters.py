from fastapi import FastAPI, Path, Query
from typing import Any

app = FastAPI()


# path param
@app.get("/items/{item_id}")
def read_item_path(item_id: int):
    return {"using path param with requested id:": item_id}


# query param
@app.get("/item")
def read_item_query(search: str | None = None, limit: int = 10) -> dict[str, Any]:
    return {
        "message": "using query params",
        "search keyword": search,
        "search limit": limit,
    }


# combined
@app.get("/read/{item_id}")
def read_item(
    item_id: int = Path(gt=0), search: str | None = Query("hello", max_length=20)
) -> dict[str, Any]:
    return {"id": item_id, "search": search}
