from typing import List, Tuple
from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class SearchPage(BasePage):
    SEARCH_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, 'button.chg-app-button--primary[type="submit"]')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_results(self) -> List[WebElement]:
        """
        Возвращает список элементов результатов поиска
        :return: список WebElement
        """
        return self.wait.until(EC.visibility_of_all_elements_located(self.SEARCH_BUTTON))
    
    def is_book_in_results(self, title: str) -> bool:
        """
        Проверяет, есть ли товар с указанным названием в результатах
        :param title: название книги/товара
        :return: True, если товар найден, иначе False
        """
        results = self.get_results()
        classes_to_check: List[str] = ['product-item__title', 'search-title__head', 'search-title__sub', 'search-results-container']
        for item in results:
            for class_name in classes_to_check:
                try:
                    element: WebElement = item.find_element(By.CLASS_NAME, class_name)
                    item_title: str = element.text
                    if title.lower() in item_title.lower():
                        return True
                except NoSuchElementException:
                    continue
        return False

    def open_first_result(self) -> None:
        """
        Открывает первый результат поиска
        """
        results = self.get_results()
        if results:
            results[0].click()

    def is_loaded(self) -> None:
        """
        Проверяет, что страница поиска загружена
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-results-container')))
