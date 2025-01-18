from src.tests.conftest import run_async
from src.tests.testlib import api_requests
from time import sleep


def test_registration(generic_user):
    response = api_requests.registration_api_request(user=generic_user.model_dump())

    assert response.status_code == 200


def test_login(generic_user):
    api_requests.registration_api_request(user=generic_user.model_dump())
    sleep(1)
    response = api_requests.login_api_request(user=generic_user.model_dump())

    assert response.status_code == 200


def test_get_all_users(generic_superuser, generic_user):
    api_requests.registration_api_request(user=generic_user.model_dump())
    sleep(1)
    login_data = api_requests.login_api_request(user=generic_superuser.model_dump())

    login_data_json = login_data.json()
    access_token = login_data_json["access_token"]

    response = api_requests.get_all_users_api_request(token=access_token)

    assert response.status_code == 200


def test_active_user_info(generic_user):
    registr_data = api_requests.registration_api_request(user=generic_user.model_dump())
    registr_data_json = registr_data.json()
    access_token = registr_data_json["access_token"]
    response = api_requests.get_active_user_api_request(token=access_token)

    assert response.status_code == 200


def test_get_book_to_user(
    create_superuser_loop,
    generic_superuser,
    generic_author,
    generic_genre,
    generic_book,
    generic_boo_genre_assotiation,
    generic_user_book_assotiation,
):

    login_data = api_requests.login_api_request(user=generic_superuser.model_dump())
    login_data_json = login_data.json()
    access_token = login_data_json["access_token"]

    author_response = api_requests.create_author(
        data=generic_author.model_dump(), token=access_token
    )

    assert author_response.status_code == 200

    genre_response = api_requests.create_genre(
        data=generic_genre.model_dump(), token=access_token
    )
    assert genre_response.status_code == 200

    book_response = api_requests.create_book(
        data=generic_book.model_dump(), token=access_token
    )

    assert book_response.status_code == 200

    genre_book_assotiation_response = api_requests.create_genre_book_assotiation(
        data=generic_boo_genre_assotiation.model_dump(), token=access_token
    )

    assert genre_book_assotiation_response.status_code == 200

    get_book_for_user_response = api_requests.get_book_for_user(
        token=access_token, data=generic_user_book_assotiation.model_dump()
    )
    assert get_book_for_user_response.status_code == 200

    user_data_response = api_requests.get_active_user_api_request(token=access_token)
    user_data = user_data_response.json()
    user_books = user_data["books"][0]
    user_books_author = user_books["author"]
    user_books_genre = user_books["genres"][0]
    assert user_data_response.status_code == 200
    assert user_data["email"] == generic_superuser.email
    assert user_books["name"] == generic_book.name
    assert user_books_author["name"] == generic_author.name
    assert user_books_genre["name"] == generic_genre.name
