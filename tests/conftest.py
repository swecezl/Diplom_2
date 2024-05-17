import requests
import pytest
from helpers import register_new_user_and_return_data
from src.data import Endpoints, BASE_URL


@pytest.fixture
def create_user_and_return_email_and_password():
    data = register_new_user_and_return_data()
    yield data[0]
    access_token = data[1].json()["accessToken"]
    requests.delete(f'{BASE_URL}{Endpoints.user_path}', headers={'Authorization': f'{access_token}'})


@pytest.fixture
def create_new_user_return_response():
    data = register_new_user_and_return_data()
    yield data[1]
    access_token = data[1].json()["accessToken"]
    requests.delete(f'{BASE_URL}{Endpoints.user_path}', headers={'Authorization': f'{access_token}'})