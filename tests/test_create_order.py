import allure
import requests
from jsonschema import validate
from src.api_client import *
from src.data import Endpoints, BASE_URL, ResponseTexts


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_authorization(self, create_new_user_return_response):
        data = create_new_user_return_response
        access_token = data.json()["accessToken"]
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa71"]
        }
        response = requests.post(f'{BASE_URL}{Endpoints.order_path}', data=payload,
                                 headers={'Authorization': f'{access_token}'})
        assert response.status_code == 200

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self):
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa71"]
        }
        response = requests.post(f'{BASE_URL}{Endpoints.order_path}', data=payload)
        name = response.json()["name"]
        order_number = response.json()["order"]["number"]
        assert response.status_code == 200
        assert response.text == f'{{"success":true,"name":"{name}","order":{{"number":{order_number}}}}}'

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_new_user_return_response):
        new_user = create_new_user_return_response
        access_token = new_user.json()["accessToken"]
        payload = {
            "ingredients": [""]
        }
        response = requests.post(f'{BASE_URL}{Endpoints.order_path}', data=payload,
                                 headers={'Authorization': f'{access_token}'})
        assert response.status_code == 400
        assert response.text == ResponseTexts.error_empty_ingredients

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self, create_new_user_return_response):
        new_user = create_new_user_return_response
        access_token = new_user.json()["accessToken"]
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa66"]
        }
        response = requests.post(f'{BASE_URL}{Endpoints.order_path}', data=payload,
                                 headers={'Authorization': f'{access_token}'})
        assert response.status_code == 400
        assert response.text == ResponseTexts.error_incorrect_ids