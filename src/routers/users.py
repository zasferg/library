from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.schemas.users import UpdateUserSchema
from src.crud.users import UserCrud
from src.crud.books import BookCrud
from src.crud.user_book import UserBookCrud
from src.schemas.user_book import CreateBookUsersSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.helpers.check_user import get_active_user


users = APIRouter(
    prefix="/users",
    tags=[
        "Users",
    ],
)


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
        get_book = await BookCrud.get_obj_by_param(session=session, name=book_data.books,offset=0,limit=10)

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
        
        check_user_have_book = await UserBookCrud.get_filtered_by_param(session=session,books=get_book.id,users=user_id)

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

        get_book = await BookCrud.get_obj_by_param(session=session, name=book_data,offset=0,limit=10)

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

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"details": "Sucessfully deleted"},
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))