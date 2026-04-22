from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple
from selenium.webdriver.remote.webelement import WebElement
import time

class MainPage(BasePage):
    URL: str = "https://www.chitai-gorod.ru/"
    SEARCH_INPUT: Tuple[str, str] = (By.ID, 'app-search')
    SEARCH_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, 'button.chg-app-button--primary[type="submit"]')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def go(self) -> None:
        """
        Открывает главную страницу сайта
        """
        self.driver.get(self.URL)

    def is_loaded(self) -> None:
        """
        Проверяет, что страница полностью загружена
        """
        self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))

    def perform_search(self, query: str) -> None:
        search_input: WebElement = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(query)
        time.sleep(0.5)  # Можно попробовать побольше или меньше
        search_button: WebElement = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        search_button.click()

    def handle_age_confirmation(self, timeout: int = 3) -> None:
        """
        Обрабатывает подтверждение возраста, если требуется
        :param timeout: время ожидания в секундах
        """
        try:
            modal = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ui-modal-content__content'))
            )
            button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'chg-app-button--primary'))
            )
            button.click()
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass
        except Exception as e:
            print(f"Ошибка при обработке подтверждения возраста: {e}")
