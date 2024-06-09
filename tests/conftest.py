import requests
import pytest
import allure
from helpers import register_new_user_and_return_data
from src.data import Endpoints, BASE_URL


@pytest.fixture
def create_user_and_return_data():
    login, data = register_new_user_and_return_data()
    yield login, data
    with allure.step('Получение данных о зарегистрированном пользователе'):
        access_token = data.json()['accessToken']
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f'{BASE_URL}{Endpoints.user_path}', headers={'Authorization': f'{access_token}'})


