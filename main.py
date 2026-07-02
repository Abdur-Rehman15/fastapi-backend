from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
def read_item_path(item_id: int):
    return {"using path param with requested id:": item_id}

@app.get("/item")
def read_item_query(search: str | None = None, limit: int = 10):
    return {
        "message": "using query params",
        "search keyword": search,
        "search limit": limit,
    }


@app.get("/read/{item_id}")
def read_item(
    item_id: int = Path(..., gt=0), search: str | None = Query(None, max_length=20)
):
    return {"id": item_id, "search": search}
