import requests
from faker import Faker
from src.data import Endpoints, BASE_URL


def register_new_user_and_return_data():
    login_pass = []

    fake = Faker(locale="ru_RU")
    user_data = {"email": fake.email(),
                 "password": fake.password(),
                 "name": fake.first_name()
                 }
    response = requests.post(f'{BASE_URL}{Endpoints.create_user_path}', data=user_data)

    if response.status_code == 200:
        login_pass.append(user_data.get("email"))
        login_pass.append(user_data.get("password"))
        login_pass.append(user_data.get("name"))

    return login_pass, response
