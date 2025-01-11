from typing import List
import uuid
from sqlalchemy import UUID, Boolean, Date, DateTime, Integer,String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime, date

class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,unique=True,default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    password: Mapped[str] = mapped_column(String(255),nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,nullable=False,default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean,nullable=False,default=False)


class Author(Base):

    __tablename__ = "authors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,unique=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30),nullable=False)
    biography: Mapped[str] = mapped_column(String(255),)
    birth_date:Mapped[date] = mapped_column(Date())
    books: Mapped["Book"] = relationship('Book',back_populates='authors')


class Genre(Base):

    __tablename__ = "genres"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,unique=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30),nullable=False)
    books: Mapped[List["Book"]] = relationship('Books',secondary="book_genres",back_populates='genres')

class Book(Base):

    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,unique=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30),nullable=False)
    description: Mapped[str] = mapped_column(String(255),nullable=True)
    publication_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),default='')
    avaliable_copies: Mapped[int] = mapped_column(Integer(),nullable=True)
    author: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("authors.id"),nullable=True)
    genres: Mapped[List["Genre"]] = relationship('Genre',secondary="book_genres",back_populates='books')



class BooksGenres(Base):

    __tablename__ = "books_genres"
    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True,unique=True,autoincrement=True)
    books: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("books.id"),nullable=True) 
    genres: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("genres.id"),nullable=True)




     