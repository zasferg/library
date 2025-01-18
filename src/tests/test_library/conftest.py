from src.schemas import authors, books, genres, book_and_genre, users, user_book
import pytest
from datetime import date


@pytest.fixture
def generic_author():
    return authors.CreateAuthorSchema(
        name="generic_author", biography="generic_bio", birth_date="1111-11-11"
    )


@pytest.fixture
def generic_genre():
    return genres.CreateGenreSchema(name="generic_genre")


@pytest.fixture
def generic_book():
    return books.CreateBookSchema(
        name="generic_book_name",
        description="generic_descr",
        avaliable_copies=10,
        author="generic_author",
        genre="generic_genre",
    )


@pytest.fixture
def generic_user():
    return users.CreateUserSchema(email="generic@mail.com", password="generic_pass")


@pytest.fixture
def generic_superuser():
    return users.CreateUserSchema(email="admin@admin.com", password="1111")


@pytest.fixture
def generic_boo_genre_assotiation():
    return book_and_genre.CreateBookGenreSchema(
        books="generic_book_name", genres="generic_genre"
    )


@pytest.fixture
def generic_user_book_assotiation():
    return user_book.CreateBookUsersSchema(
        books="generic_book_name", return_book_date="1111-11-11"
    )
