from fastapi import APIRouter

library = APIRouter(prefix="/api/ping")

@library.get("/")
async def ping():
    return {"details": "OK"}
