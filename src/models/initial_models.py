from typing import List
import uuid
from sqlalchemy import UUID, Boolean, Date, DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime, date


class Base(DeclarativeBase):
    pass


class BooksUsers(Base):

    __tablename__ = "books_users"

    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, unique=True, autoincrement=True
    )
    books: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.id"), nullable=True
    )
    users: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    given_to_user_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    return_book_date: Mapped[datetime] = mapped_column(
        Date, nullable=True, default=None
    )


class BooksGenres(Base):

    __tablename__ = "books_genres"

    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, unique=True, autoincrement=True
    )
    books: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.id"), nullable=True
    )
    genres: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("genres.id"), nullable=True
    )


class User(Base):

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tokens: Mapped[List["Token"]] = relationship(
        "Token", back_populates="user", lazy="selectin"
    )
    books: Mapped[List["Book"]] = relationship(
        "Book", secondary="books_users", back_populates="user", lazy="selectin"
    )


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    refresh_token: Mapped[str] = mapped_column(
        Text, nullable=False, unique=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id], back_populates="tokens", lazy="selectin"
    )


class Author(Base):

    __tablename__ = "authors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    biography: Mapped[str] = mapped_column(
        Text,
    )
    birth_date: Mapped[date] = mapped_column(Date())
    books: Mapped[List["Book"]] = relationship(back_populates="author")


class Genre(Base):

    __tablename__ = "genres"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    books: Mapped[List["Book"]] = relationship(
        "Book", secondary="books_genres", back_populates="genres"
    )


class Book(Base):

    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    avaliable_copies: Mapped[int] = mapped_column(Integer(), nullable=True)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("authors.id"), nullable=True
    )
    author: Mapped["Author"] = relationship(
        "Author", foreign_keys=[author_id], lazy="selectin", back_populates="books"
    )
    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="books_genres", back_populates="books", lazy="selectin"
    )
    user: Mapped["User"] = relationship(
        "User", secondary="books_users", back_populates="books", lazy="selectin"
    )
