import allure
import pytest
import json
from Pages.api_client import ApiClient
from config import BASE_URL, URL_2, ACCESS_TOKEN

client = ApiClient(base_url=BASE_URL)

@allure.story("Добавление товара с неверным ID")
@allure.title("Проверка ошибки при добавлении товара с неправильным ID")
@pytest.mark.api
def test_add_nonexistent_product():
    invalid_product_id = 999999999 
    response_code, response_json = client.product_to_cart(product_id=invalid_product_id, use_url_2=True)
    assert response_code == 404

@allure.story("Получение информации о товарах в корзине")
@allure.title("Проверка успешного получения корзины")
@pytest.mark.api
def test_get_cart_info():
    client = ApiClient(base_url=BASE_URL, token=ACCESS_TOKEN)
    code, response = client.get_cart_info()
    assert code == 200

@allure.story("Поиск по названию")
@allure.title("Поиск товара по фразе с корректными параметрами")
@pytest.mark.api
def test_search_product(api_client):
    """
    Тест проверяет успешный поиск по фразе и правильность структуры ответа.
    """
    response_code, response = api_client.search_product(
        city_id=213,
        phrase="в плену синих роз",
        ab_test_group="1",
        page=1,
        per_page=60
    )
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
    """
    Тест проверяет успешное добавление товара по валидному ID.
    """
    product_id = 3111363
    code, response = api_client.product_to_cart(product_id=product_id, use_url_2=True)
    assert code == 200, f"Код ответа: {code}"
    if response:
        assert isinstance(response, dict)
        assert response.get("success") or "id" in response, "Ответ должен содержать 'success' или 'id'"
    else:
        pass

@allure.story("Поиск книги с невалидным запросом")
@allure.title("Поиск без фразы возвращает ошибку")
@pytest.mark.api
def test_search_without_phrase():
    """
    Тест проверяет, что поиск без фразы возвращает ошибку.
    """
    code, response = client.search_product(
        city_id=213,
        phrase="",
        ab_test_group=""
    )
    assert code >= 400, f"Ожидали ошибку, код: {code}"
    assert isinstance(response, dict)
    if "error" in response:
        assert response["error"] is not None


@allure.story("Оформление заказа с невалидным ID города")
@allure.title("Проверка ошибки при неправильном cityID")
@pytest.mark.api
def test_checkout_with_invalid_city_id():
    """
    Тест проверяет, что неправильный city_id возвращает ошибку (код >= 400).
    """
    invalid_city_id = "1ола61"
    code, response = client.checkout(
        city_id=invalid_city_id,
        shipment_type="pickup",
        user_type="individual",
        order_type="order"
    )
    assert code >= 400, f"Ожидали ошибку, код: {code}"
    assert isinstance(response, dict)
    if "error" in response:
        assert response["error"] is not None

@allure.story("Добавление товара с невалидным количеством")
@allure.title("Проверка ошибки при запросе с большим количеством")
@pytest.mark.api
def test_add_product_with_invalid_quantity():
    """
    Тест проверяет, что при запросе с очень большим количеством товара приходит ошибка.
    """
    product_id = "3111363"
    large_quantity = 1000000
    code, response = client.product_to_cart(
        product_id=product_id,
        quantity=large_quantity
    )
    assert code >= 400, f"Ожидали ошибку, получили код: {code}"
    assert isinstance(response, dict)
    if "error" in response:
        assert response["error"] is not None

@allure.story("Проверка работы API без авторизации")
@allure.title("Запрос корзины без токена авторизации")
@pytest.mark.api
def test_api_without_authentication():
    """
    Тест проверяет работу получения корзины без токена.
    """
    unauth_client = ApiClient(base_url=BASE_URL, token=None)
    code, response = unauth_client.get_cart_info()
    assert code == 401 or code == 403, f"Ожидали ошибку авторизации, получили код: {code}"
    assert isinstance(response, dict)
    if "error" in response:
        assert response["error"] is not None
