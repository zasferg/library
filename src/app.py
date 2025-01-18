import uvicorn
from fastapi import Depends, FastAPI
from src.routers.books import books
from src.routers.autors import autors
from src.routers.genres import genres
from src.routers.book_genre import books_genres
from src.routers.users import users
from src.routers.authentication import auth
from src.auth.helpers.check_user import get_superuser_user

app = FastAPI()

app.include_router(
    books,
    dependencies=[
        Depends(get_superuser_user),
    ],
)
app.include_router(
    autors,
    dependencies=[
        Depends(get_superuser_user),
    ],
)
app.include_router(
    genres,
    dependencies=[
        Depends(get_superuser_user),
    ],
)
app.include_router(
    books_genres,
    dependencies=[
        Depends(get_superuser_user),
    ],
)
app.include_router(auth)
app.include_router(users)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
