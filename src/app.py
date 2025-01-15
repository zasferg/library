import uvicorn
from fastapi import FastAPI
from src.routers.library import library
from src.routers.books import books 
from src.routers.autors import autors
from src.routers.genres import genres
from src.routers.book_genre import books_genres


app = FastAPI()

app.include_router(library)
app.include_router(books)
app.include_router(autors)
app.include_router(genres)
app.include_router(books_genres)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)