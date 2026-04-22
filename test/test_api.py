import allure
import pytest
from Pages.api_client import ApiClient
from config import BASE_URL, URL_2, ACCESS_TOKEN

@allure.story("Добавление товара с неверным ID")
@allure.title("Проверка ошибки при добавлении товара с неправильным ID")
@pytest.mark.api
def test_add_nonexistent_product(api_client):
    with allure.step("Устанавливаем неправильный ID товара"):
        invalid_product_id = 999999999
    with allure.step("Отправляем запрос на добавление товара в корзину"):
        response_code, response_json = api_client.product_to_cart(product_id=invalid_product_id)
    with allure.step("Проверяем, что сервер возвращает код 404, 401, 400, 422"):
        assert response_code in [404, 401, 400, 422], f"Получен неожиданный статус: {response_code}"

@allure.story("Получение информации о товарах в корзине")
@allure.title("Проверка успешного получения корзины")
@pytest.mark.api
def test_get_cart_info(api_client):
    with allure.step("Отправляем запрос на получение информации о корзине"):
        code, response = api_client.get_cart_info()
    with allure.step("Проверяем, что ответ успешный (код 200)"):
        assert code == 200

@allure.story("Поиск по названию")
@allure.title("Поиск товара по фразе с корректными параметрами")
@pytest.mark.api
def test_search_product(api_client_url_2):
    with allure.step("Выполняем поиск по фразе 'в плену синих роз'"):
        response_code, response = api_client_url_2.search_product(
            city_id=213,
            phrase="в плену синих роз",
        )
    with allure.step(f"Проверяем, что код ответа — {response_code} и структура ответа корректна"):
        assert response_code == 200, f"Код ответа: {response_code}"
        assert isinstance(response, dict), f"Ожидал dict, получил {type(response)}"
        assert "data" in response, "Ответ должен содержать 'data'"
        data = response["data"]
        assert isinstance(data, list), "'data' должно быть списком"
        for item in data:
            assert isinstance(item, dict), "Каждый элемент 'data' должен быть словарем"

@allure.story("Добавление товара в корзину")
@allure.title("Добавление товара по валидному ID")
@pytest.mark.api
def test_add_product_valid(api_client):
    product_id = 3111363
    with allure.step(f"Добавляем товар с ID {product_id} в корзину"):
        response_code, response_json = api_client.product_to_cart(product_id=product_id)
    with allure.step("Проверяем, что сервер возвращает код 200"):
        assert response_code in [200], f"Получен неожиданный статус: {response_code}"

@allure.story("Поиск книги с невалидным запросом")
@allure.title("Поиск без фразы возвращает ошибку")
@pytest.mark.api
def test_search_without_phrase(api_client):
    with allure.step("Выполняем поиск без фразы"):
        code, response = api_client.search_product(
            city_id=213,
            phrase="",
            ab_test_group=""
        )
    with allure.step(f"Проверяем, что получили ошибку (код {code})"):
        assert code >= 400, f"Ожидали ошибку, код: {code}"
        assert isinstance(response, dict)
        if "error" in response:
            with allure.step("Проверяем наличие сообщения об ошибке"):
                assert response["error"] is not None

@allure.story("Оформление заказа с невалидным ID города")
@allure.title("Проверка ошибки при неправильном cityID")
@pytest.mark.api
def test_checkout_with_invalid_city_id(api_client):
    invalid_city_id = "1ола61"
    with allure.step("Отправляем заказ с некорректным city_id"):
        code, response = api_client.checkout(
            city_id=invalid_city_id,
            shipment_type="pickup",
            user_type="individual",
            order_type="order"
        )
    with allure.step(f"Проверяем, что получена ошибка (код {code})"):
        assert code >= 400, f"Ожидали ошибку, код: {code}"
        assert isinstance(response, dict)
        if "error" in response:
            with allure.step("Проверяем сообщение об ошибке"):
                assert response["error"] is not None

@allure.story("Добавление товара с невалидным количеством")
@allure.title("Проверка ошибки при запросе с большим количеством")
@pytest.mark.api
def test_add_product_with_invalid_quantity(api_client):
    product_id = 3111363  # число в виде int
    large_quantity = 1000000
    with allure.step(f"Добавляем товар с количеством {large_quantity}"):
        code, response = api_client.product_to_cart(
            product_id=product_id,
            quantity=large_quantity
        )
    with allure.step(f"Проверяем, что сервер возвращает ошибку (код {code})"):
        assert code >= 400, f"Ожидали ошибку, получили код: {code}"
        assert isinstance(response, dict)
        if "error" in response:
            with allure.step("Проверяем сообщение об ошибке"):
                assert response["error"] is not None

@allure.story("Проверка работы API без авторизации")
@allure.title("Запрос корзины без токена авторизации")
@pytest.mark.api
def test_api_without_authentication():
    with allure.step("Создаём клиента без токена авторизации"):
        unauth_client = ApiClient(base_url=BASE_URL, token=None)
    with allure.step("Отправляем запрос на получение корзины без авторизации"):
        code, response = unauth_client.get_cart_info()
    with allure.step(f"Проверяем, что получен код ошибки авторизации (код {code})"):
        assert code in (401, 403), f"Ожидали ошибку авторизации, получили код: {code}"
        assert isinstance(response, dict)
        if "error" in response:
            with allure.step("Проверяем сообщение об ошибке авторизации"):
                assert response["error"] is not None
