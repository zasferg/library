import uvicorn
from fastapi import FastAPI
from src.routers.books import books
from src.routers.autors import autors
from src.routers.genres import genres
from src.routers.book_genre import books_genres
from src.routers.users import users
from src.routers.authentication import auth


app = FastAPI()

app.include_router(books)
app.include_router(autors)
app.include_router(genres)
app.include_router(books_genres)
app.include_router(auth)
app.include_router(users)



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
