import uvicorn
from fastapi import FastAPI
from src.routers.library import library


app = FastAPI()

app.include_router(library)
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)