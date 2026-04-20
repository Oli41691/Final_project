from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from Pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Tuple, List

class CartPage(BasePage):
    CART_ITEMS: Tuple[str, str] = (By.CSS_SELECTOR, ".cart-item")

    def open(self) -> None:
        """
        Открывает первый элемент в корзине, если он есть
        """
        elements: List[WebElement] = self.driver.find_elements(*self.CART_ITEMS)
        if elements:
            elements[0].click()

    def get_items_count(self) -> int:
        """
        Возвращает количество товаров в корзине
        """
        items: List[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
        return len(items)

    def is_item_in_cart(self, title: str) -> bool:
        """
        Проверяет, есть ли товар с указанным заголовком в корзине
        :param title: название товара для поиска
        :return: True, если товар найден, False — иначе
        """
        items: List[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
        for item in items:
            item_title: str = item.find_element(By.CLASS_NAME, 'cart-item__title').text
            if title.lower() in item_title.lower():
                return True
        return False
