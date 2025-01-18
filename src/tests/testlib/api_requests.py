import requests


host = "http://localhost:8000"


def create_author(data, token):
    data["birth_date"] = data["birth_date"].isoformat()
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(
        url=f"{host}/api/authors/create", headers=headers, json=data
    )
    return response


def create_genre(data, token):
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(
        url=f"{host}/api/genres/create", headers=headers, json=data
    )

    return response


def create_book(data, token):
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(url=f"{host}/api/books/create", headers=headers, json=data)
    return response


def create_genre_book_assotiation(data, token):
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(
        url=f"{host}/api/books_and_genre_assotiation/add", headers=headers, json=data
    )

    return response


def registration_api_request(user):
    response = requests.post(url=f"{host}/api/auth/registration", json=user)
    return response


def login_api_request(user):
    response = requests.post(url=f"{host}/api/auth/login", json=user)
    return response


def get_all_users_api_request(token):
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(
        url=f"{host}/api/users/all",
        headers=headers,
    )

    return response


def get_active_user_api_request(token):
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(
        url=f"{host}/api/users/me",
        headers=headers,
    )

    return response


def get_access_api_request(token):
    response = requests.post(url=f"{host}/api/auth/get_access", data=f'"{token}"')
    return response


def get_book_for_user(data, token):
    data["return_book_date"] = data["return_book_date"].isoformat()
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(
        url=f"{host}/api/users/get_book", headers=headers, json=data
    )

    return response


def wiev_all_books_avaliable_to_user(data, token):

    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(
        url=f"{host}/api/users/books_by_param", headers=headers, json=data
    )

    return response
