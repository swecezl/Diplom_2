import requests
from faker import Faker
from src.data import Endpoints, BASE_URL, ResponseTexts
import pytest
import allure

fake = Faker(locale="ru_RU")


class TestCreateUser:

    @allure.title('Проверка создания нового пользователя')
    @allure.description(
        'Проверка успешного возможности создания нового пользователя')
    def test_create_new_user_success(self, create_new_user_return_response):
        response = create_new_user_return_response
        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]
        assert response.status_code == 200
        assert response.text == f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}},"accessToken":"{access_token}","refreshToken":"{refresh_token}"}}'

    @allure.title('Проверка обязательности заполнения полей')
    @allure.description(
        'Проверяем что поля логина, пароля, имени обязательны для заоплнения, а также проверка кода и текста ошибки')
    @pytest.mark.parametrize('wrong_user_data',
                             [f'{{"email": "", "password": "qwerty123", "name": {fake.first_name()}',
                              f'{{"email": {fake.email()}, "password": "", "name": {fake.first_name()}}}',
                              f'{{"email": {fake.email()}, "password": "qwerty123", "name": ""}}'])
    def test_mandatory_fields_are_missing(self, wrong_user_data):
        response = requests.post(f'{BASE_URL}{Endpoints.create_user_path}', data=wrong_user_data)
        assert response.status_code == 403
        assert response.text == ResponseTexts.error_missing_mandatory_field

    @allure.title('Проверка невозможности создания одинаковых пользователей')
    @allure.description(
        'Проверка невозможности создания пользователя с уже существующими данными, проверка кода и текста ошибки')
    def test_creating_same_user_is_prohibited(self, create_user_and_return_email_and_password):
        new_user = create_user_and_return_email_and_password
        email = new_user[0]
        password = new_user[1]
        name = new_user[2]
        user_data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{BASE_URL}{Endpoints.create_user_path}', data=user_data)
        assert response.status_code == 403
        assert response.text == ResponseTexts.error_user_already_exists