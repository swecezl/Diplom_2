import requests
import pytest
import allure
from src.data import Endpoints, BASE_URL, ResponseTexts
from faker import Faker

fake = Faker(locale="ru_RU")


class TestUpdateUserData:

    @pytest.mark.parametrize('new_user_data',
                             [f'{{"name": "{fake.first_name()}"}}', f'{{"email": "{fake.free_email()}"}}'])
    @allure.title("Изменение данных пользователя с хедером авторизации")
    def test_update_authorized_user_data(self, create_user_and_return_data, new_user_data):
        login, data = create_user_and_return_data
        access_token = data.json()["accessToken"]
        payload = new_user_data
        response = requests.patch(f'{BASE_URL}{Endpoints.user_path}', data=payload,
                                  headers={'Authorization': f'{access_token}'})
        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        assert response.status_code == 200 and response.text == f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}}}}'

    @pytest.mark.parametrize('new_user_data',
                             [f'{{"name": "{fake.first_name()}"}}', f'{{"email": "{fake.email()}"}}'])
    @allure.title("Изменение данных пользователя без хедера авторизации")
    def test_update_unauthorized_user_data(self, new_user_data):
        payload = new_user_data
        response = requests.patch(f'{BASE_URL}{Endpoints.user_path}', data=payload)
        assert response.status_code == 401 and response.text == ResponseTexts.error_unauthorised_user
