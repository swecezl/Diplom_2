import allure
import requests
from src.data import Endpoints, BASE_URL, ResponseTexts


class TestGetOrdersUser:

    @allure.title("Получение заказов конкретного пользователя: авторизованный пользователь")
    def test_get_orders_user_with_authorization(self, create_new_user_return_response):
        data = create_new_user_return_response
        access_token = data.json()["accessToken"]
        response = requests.get(f'{BASE_URL}{Endpoints.order_path}', headers={'Authorization': f'{access_token}'})
        orders = response.json()["orders"]
        total = response.json()["total"]
        total_today = response.json()["totalToday"]
        assert response.status_code == 200
        assert response.text == f'{{"success":true,"orders":{orders},"total":{total},"totalToday":{total_today}}}'

    @allure.title("Получение заказов конкретного пользователя: неавторизованный пользователь")
    def test_get_orders_user_without_authorization(self):
        response = requests.get(f'{BASE_URL}{Endpoints.order_path}')
        assert response.status_code == 401
        assert response.text == ResponseTexts.error_unauthorised_user