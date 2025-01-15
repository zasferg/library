from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.crud.autors import AutorsCrud
from src.schemas.authors import *
from sqlalchemy.ext.asyncio import AsyncSession


autors = APIRouter(prefix="/api/autors")


@autors.get("/get_all")
async def get_all_autors(session: AsyncSession=Depends(get_session)):
    try:
        result = await AutorsCrud.get_all(session=session)
        if not result:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Книги не найдены"}
        )
        return result 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    

@autors.get("/get_by_name")
async def get_author_by_name(name: str, session: AsyncSession=Depends(get_session)):
    try:
        result = await AutorsCrud.get_obj_by_param(session=session,name=name)
        if not result:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Книги не найдены"}
        )
        return result 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})


@autors.post("/create")
async def create_author(data: CreateAuthorSchema, session: AsyncSession=Depends(get_session)):
    try:
        check_author = await AutorsCrud.get_obj_by_param(session=session,name=data.name)
        if check_author:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"Данный автор уже есть в базе данных"}
            )
        new_author = AutorsCrud.create(session=session, 
                                    name=data.name,
                                    biography=data.biography,)
        
        return new_author
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    

@autors.put("/update")
async def update_author(id: UUID, 
                        data: UpdateAuthorSchema, 
                        session: AsyncSession=Depends(get_session)):

    try:
        result = await AutorsCrud.update(session=session,record_id=id,**data.model_dump())
        if not result:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Что-то пошло не так"}
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    

@autors.post("/delete")
async def delete_author(id: UUID, session:AsyncSession=Depends(get_session)):
    try:

        await AutorsCrud.delete(session=session,record_id=id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"details": "Sucessfully deleted"},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    