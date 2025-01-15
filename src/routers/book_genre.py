from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.crud.books import BookCrud
from src.crud.genres import GenresCrud
from src.crud.book_genre import BookGenreCrud
from schemas.books import *
from sqlalchemy.ext.asyncio import AsyncSession


books_genres = APIRouter(prefix="/api/books_and_genre_assotiation")


    
@books_genres.post("/add_genre_book_assotiation")
async def add_genre_to_book(genre_name: str, book_name: str, session: AsyncSession = Depends(get_session)):
    try:
        get_genre = await GenresCrud.get_obj_by_param(session=session, name=genre_name)
        get_book = await BookCrud.get_obj_by_param(session=session,name=book_name)
        if not get_genre or not get_book:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Жанр или книга не не найденф"}
        )
        genre_book_assotiation = await BookGenreCrud.create(session=session, genres = get_genre.id, books=get_book.id)

        return genre_book_assotiation

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@books_genres.post("/delete_genre_book_assotiation")
async def delete_genre_to_book(genre_name: str, book_name: str, session: AsyncSession = Depends(get_session)):
    try:
        get_genre = GenresCrud.get_obj_by_param(session=session,name=genre_name)
        get_book = BookCrud.get_obj_by_param(session=session,name=book_name)
        if not get_genre or not get_book:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Жанр или книга не не найдены"}
        )
        get_assotiation = BookGenreCrud.get_filtered_by_param(session=session, genres=get_genre.id, books=get_book.id)
        if not get_genre or not get_book:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Данная книга не относится к данному жанру"}
        )
        await BookGenreCrud.delete(session=session,record_id=get_assotiation.id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"details": "Sucessfully deleted"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
