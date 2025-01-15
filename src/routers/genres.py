from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_session
from src.crud.genres import GenresCrud
from src.schemas.genres import *
from sqlalchemy.ext.asyncio import AsyncSession


genres = APIRouter(prefix="/api/genres")


@genres.get("/get_all")
async def get_all_genres(session: AsyncSession=Depends(get_session)):
    try:
        result = await GenresCrud.get_all(session=session)
        if not result:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Жанры не найдены"}
        )
        return result 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    

@genres.get("/get_by_name")
async def get_genre_by_name(name: str, session: AsyncSession=Depends(get_session)):
    try:
        result = await GenresCrud.get_obj_by_param(session=session,name=name)
        if not result:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Жанры не найдены"}
        )
        return result 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    

@genres.post("/create")
async def create_author(data: CreateGenreSchema, session: AsyncSession=Depends(get_session)):
    try:
        check_genre = await GenresCrud.get_obj_by_param(session=session,name=data.name)
        if check_genre:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={"Данный жанр уже есть в базе данных"}
            )
        new_genre = GenresCrud.create(session=session, 
                                    name=data.name,)     
        return new_genre
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    

@genres.put("/update")
async def update_author(id: UUID, 
                        data: UpdateGenrSchema, 
                        session: AsyncSession=Depends(get_session)):

    try:
        result = await GenresCrud.update(session=session,record_id=id,**data.model_dump())
        if not result:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"Что-то пошло не так"}
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    

@genres.post("/delete")
async def delete_author(id: UUID, session:AsyncSession=Depends(get_session)):
    try:

        await GenresCrud.delete(session=session,record_id=id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"details": "Sucessfully deleted"},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={e})
    