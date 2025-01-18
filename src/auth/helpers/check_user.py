from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.helpers.utils import get_token_data, credentials_exception
from src.crud.users import UserCrud
from src.database import get_session
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


security = HTTPBearer()


async def get_active_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: AsyncSession = Depends(get_session),
):
    payload = get_token_data(token.credentials)
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    user = await UserCrud.get_by_id(session=session, id=user_id)
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not authenticated"
        )
    return {"user": user, "payload": payload, "token": token}


async def get_superuser_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: AsyncSession = Depends(get_session),
):
    print(token)
    payload = get_token_data(token.credentials)
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    user = await UserCrud.get_by_id(session=session, id=user_id)
    if not user:
        raise credentials_exception
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return {"user": user, "payload": payload, "token": token}
