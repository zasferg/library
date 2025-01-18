from sqlite3 import IntegrityError
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.crud.users import UserCrud
from src.crud.tokens import TokenCrud
from src.schemas.users import CreateUserSchema
from src.schemas.authors import *
from sqlalchemy.ext.asyncio import AsyncSession
from auth.helpers.utils import (
    create_access_token,
    create_refresh_token,
    get_checked_token_data,
    verify_password,
    hash_password
)


auth = APIRouter(
    prefix="/api/auth",
    tags=[
        "Auth",
    ],
)


@auth.post("/registration")
async def registration_handler(
    user_data: CreateUserSchema, 
    session: AsyncSession = Depends(get_session)
):
    try:

        user = await UserCrud.create(
            session=session,
            email=user_data.email,
            password=hash_password(user_data.password),
        )

        access_token = create_access_token(data={"user_id": str(user.id)})
        refresh_token = create_refresh_token(data={"user_id": str(user.id)})
        await TokenCrud.create(
            session=session, refresh_token=refresh_token, user_id=user.id
        )

        return {"access_token": access_token, "refresh_token": refresh_token}
    except IntegrityError as ie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь уже зарегистрирован.",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth.post("/login")
async def registration_handler(
    user_data: CreateUserSchema, 
    session: AsyncSession = Depends(get_session)
):
    try:
        get_user = await UserCrud.get_filtered_by_param(session=session,email= user_data.email)

        if not get_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не зарегистрирован"
                )

        if not verify_password(user_data.password, get_user[0].password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль"
                )
        
        access_token = create_access_token(data={"user_id": str(get_user[0].id)})
        refresh_token = create_refresh_token(data={"user_id": str(get_user[0].id)})

        await TokenCrud.create(
            session=session, refresh_token=refresh_token, user_id=get_user[0].id
        )

        return {"access_token": access_token, "refresh_token": refresh_token}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth.post("/get_access")
async def get_access_handler(
    refresh_token: str = Body(..., embed=True),
    session: AsyncSession = Depends(get_session),
):
    try:
        payload = await get_checked_token_data(
            token=refresh_token, session=session, refresh=True
        )
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный токен"
            )

        access_token = create_access_token(data={"user_id": str(payload["user_id"])})
        refresh_token = create_refresh_token(data={"user_id": str(payload["user_id"])})
        await TokenCrud.create(
            session=session, refresh_token=refresh_token, user_id=payload["user_id"]
        )

        return {"access_token": access_token, "refresh_token": refresh_token}
    except HTTPException as _he:
        raise HTTPException(status_code=_he.status_code, detail=f"Токен истек, {_he}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
