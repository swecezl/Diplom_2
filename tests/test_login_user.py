import allure
import requests
import random
from faker import Faker
from src.data import Endpoints, BASE_URL, ResponseTexts

fake = Faker(locale="ru_RU")


class TestLoginUser:

    @allure.title('Проверка успешного логина пользователя')
    @allure.description(
        'Проверка получения корректного кода и текста в случае передачи корректных данных для логина')
    def test_login_user_success(self, create_user_and_return_data):
        login, data = create_user_and_return_data
        payload = {
            "email": login[0],
            "password": login[1]
        }
        response = requests.post(f'{BASE_URL}{Endpoints.login_path}', data=payload)
        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]
        assert response.status_code == 200 and response.text == f'{{"success":true,"accessToken":"{access_token}","refreshToken":"{refresh_token}","user":{{"email":"{email}","name":"{name}"}}}}'

    @allure.title('Проверка логина с некорректным email')
    @allure.description(
        'Проверка получения ошибки если в форму логина передаем незарегистрированный email')
    def test_login_with_incorrect_email(self, create_user_and_return_data):
        login, data = create_user_and_return_data
        email = fake.free_email()
        password = login[1]
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f'{BASE_URL}{Endpoints.login_path}', payload)
        assert response.status_code == 401 and response.text == ResponseTexts.error_incorrect_password_or_email

    @allure.title('Проверка логина с некорректным паролем')
    @allure.description(
        'Проверка получения ошибки если в форму логина передаем неверный пароль пользвователя')
    def test_login_with_incorrect_password(self, create_user_and_return_data):
        login, data = create_user_and_return_data
        email = login[0]
        password = random.randint(100000, 999999)
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f'{BASE_URL}{Endpoints.login_path}', payload)
        assert response.status_code == 401 and response.text == ResponseTexts.error_incorrect_password_or_email
