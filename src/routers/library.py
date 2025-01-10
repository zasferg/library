from fastapi import APIRouter

library = APIRouter(prefix="")

@library.get("/library/")
async def ping():
    return {"details": "OK"}
