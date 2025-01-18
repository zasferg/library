from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.schemas.users import UpdateUserSchema
from src.crud.users import UserCrud
from src.crud.books import BookCrud
from src.crud.user_book import UserBookCrud
from src.schemas.user_book import CreateBookUsersSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.helpers.check_user import get_active_user, get_superuser_user
import logging


users = APIRouter(
    prefix="/api/users",
    tags=[
        "Users",
    ],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@users.get("/all")
async def get_all_users(
    auth_data: dict = Depends(get_superuser_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await UserCrud.get_all(session=session)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Пользователи не найдены"},
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users.get("/me")
async def get_user_info(
    auth_data: dict = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
):

    try:
        user_id = auth_data["user"].id
        user_in_db = await UserCrud.get_by_id(session=session, id=user_id)
        if not user_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не существует",
            )
        return user_in_db
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users.patch("/me")
async def get_user_info(
    update_data: UpdateUserSchema,
    auth_data: dict = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
):

    try:
        user_id = auth_data["user"].id
        updated_user = await UserCrud.update(
            session=session, record_id=user_id, **update_data.model_dump()
        )
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не существует",
            )
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users.post("/get_book")
async def get_book(
    book_data: CreateBookUsersSchema,
    auth_data: dict = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        user_id = auth_data["user"].id

        logger.info(f"Пользователь c ID {user_id} пытается удалить книгу {book_data.books}")

        get_book = await BookCrud.get_obj_by_param(
            session=session, name=book_data.books, offset=0, limit=10
        )

        if not get_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Данной книги не существует",
            )

        if get_book.avaliable_copies == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Нет доступных книг",
            )

        check_books_count = await UserBookCrud.get_filtered_by_param(
            session=session, books=get_book.id
        )

        if len(check_books_count) >= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"У данного пользователя больше 5 книг",
            )

        check_user_have_book = await UserBookCrud.get_filtered_by_param(
            session=session, books=get_book.id, users=user_id
        )

        if len(check_user_have_book) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"У данного пользователя уже есть эта книга",
            )

        book_user_assotiation = await UserBookCrud.create(
            session=session,
            books=get_book.id,
            users=user_id,
            return_book_date=book_data.return_book_date,
        )

        logger.info(f"Книга{book_data.books} успешно присвоена {user_id}")

        await BookCrud.update(
            session=session,
            record_id=get_book.id,
            avaliable_copies=get_book.avaliable_copies - 1,
        )
        return book_user_assotiation
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users.post("/delete_book")
async def delete_book(
    book_data: str,
    auth_data: dict = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:

        user_id = auth_data["user"].id

        logger.info(f"Пользователь с ID {user_id} пытается вернуть книгу {book_data}")

        get_book = await BookCrud.get_obj_by_param(
            session=session, name=book_data, offset=0, limit=10
        )

        get_book_user_assoiation = await UserBookCrud.get_obj_by_param(
            session=session, books=get_book.id, users=user_id
        )

        await UserBookCrud.delete(
            session=session, record_id=get_book_user_assoiation.id
        )
        await BookCrud.update(
            session=session,
            record_id=get_book.id,
            avaliable_copies=get_book.avaliable_copies + 1,
        )
        logger.info(f"Книга {book_data} вернута пользователем {user_id}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"details": "Sucessfully deleted"},
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users.get("/books_by_param")
async def get_available_books(
    auth_data: dict = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await BookCrud.get_all_available_books(
            session=session,
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={"Книги не найдены"}
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
