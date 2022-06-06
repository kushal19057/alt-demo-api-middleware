from fastapi import FastAPI

my_awesome_api = FastAPI()

@my_awesome_api.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"message": item_id}
