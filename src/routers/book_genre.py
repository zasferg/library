from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.crud.books import BookCrud
from src.crud.genres import GenresCrud
from src.crud.book_genre import BookGenreCrud
from schemas.books import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.book_and_genre import *
from src.utils.custom_exceptions import AssotiationNotFoundException


books_genres = APIRouter(
    prefix="/api/books_and_genre_assotiation",
    tags=[
        "Books_genres",
    ],
)


@books_genres.post("/add")
async def add_genre_to_book(
    data: CreateBookGenreSchema, session: AsyncSession = Depends(get_session)
):
    try:
        get_genre = await GenresCrud.get_obj_by_param(session=session, name=data.genres)
        get_book = await BookCrud.get_obj_by_param(
            session=session, name=data.books, limit=10, offset=0
        )
        if not get_genre or not get_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Жанр или книга не не найденф",
            )
        genre_book_assotiation = await BookGenreCrud.create(
            session=session, genres=get_genre.id, books=get_book.id
        )

        return genre_book_assotiation

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@books_genres.post("/delete")
async def delete_genre_to_book(
    data: CreateBookGenreSchema, session: AsyncSession = Depends(get_session)
):
    try:
        get_genre = await GenresCrud.get_obj_by_param(session=session, name=data.genres)
        get_book = await BookCrud.get_obj_by_param(
            session=session, name=data.books, limit=10, offset=0
        )

        if not get_genre or not get_book:
            raise ValueError

        get_assotiation = await BookGenreCrud.get_obj_by_param(
            session=session, genres=get_genre.id, books=get_book.id
        )

        if not get_assotiation:
            raise AssotiationNotFoundException

        await BookGenreCrud.delete(session=session, record_id=get_assotiation.id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"details": "Sucessfully deleted"},
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Жанр или книга не не найдены"
        )
    except AssotiationNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данная книга не относится к данному жанру",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
