from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.crud.books import BookCrud
from src.crud.autors import AutorsCrud
from src.crud.genres import GenresCrud
from src.crud.book_genre import BookGenreCrud
from src.schemas.books import *
from sqlalchemy.ext.asyncio import AsyncSession


books = APIRouter(
    prefix="/api/books",
    tags=[
        "Books",
    ],
)


@books.get("/get_all")
async def get_all_books(
    limit: int = 10, offset: int = 0, session: AsyncSession = Depends(get_session)
):
    try:
        result = await BookCrud.get_all(limit=limit, offset=offset, session=session)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={"Книги не найдены"}
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@books.get("/get_by_name")
async def get_book_by_name(
    name: str,
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await BookCrud.get_obj_by_param(
            limit=limit, offset=offset, session=session, name=name
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={"Книга не найдена"}
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@books.post("/create")
async def create_book(
    book: CreateBookSchema, session: AsyncSession = Depends(get_session)
):
    try:

        get_author = await AutorsCrud.get_obj_by_param(
            session=session, name=book.author
        )
        get_genre = await GenresCrud.get_obj_by_param(session=session, name=book.genre)

        if not get_genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={"Жанр не найден"}
            )

        if not get_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={"Автор не найден"}
            )

        new_book = await BookCrud.create(
            session,
            name=book.name,
            description=book.description,
            avaliable_copies=book.avaliable_copies,
            author_id=get_author.id,
        )
        await BookGenreCrud.create(
            session=session, genres=get_genre.id, books=new_book.id
        )
        get_new_book = await BookCrud.get_by_id(session=session, id=new_book.id)

        return get_new_book

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@books.put("/update")
async def update_book(
    id: UUID, data: UpdateBookSchema, session: AsyncSession = Depends(get_session)
):
    try:
        result = await BookCrud.update(
            session=session, record_id=id, **data.model_dump()
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={"Что-то пошло не так"}
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@books.post("/delete")
async def delete_book(id: UUID, session: AsyncSession = Depends(get_session)):
    try:
        get_book_genre_assotiation = await BookGenreCrud.get_filtered_by_param(
            session=session, books=id
        )

        if get_book_genre_assotiation:
            await BookGenreCrud.delete(session=session, books=id)

        await BookCrud.delete(session=session, record_id=id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"details": "Sucessfully deleted"},
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
