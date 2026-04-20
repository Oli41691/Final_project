## Автоматизация тестирования интернет-магазина "Chitai-Gorod" 
# Описание проекта
Данный проект предназначен для автоматизированного тестирования сайта интернет-магазина "Chitai-Gorod". В рамках проекта реализованы UI и API тесты, что позволяет обеспечить качество и стабильность сайта за счёт автоматической проверки функционала. Используются такие инструменты, как Selenium WebDriver, pytest и Allure для формирования отчетов.

# Структура проекта
# Final_project:

##  Pages   
Страницы Page Object Model

- BasePage.py
Базовая страница
-  MainPage.py
Главная страница
-  ProductPage.py
Страница товара
- SearchPage.py
Страница поиска
- CartPage.py
Корзина
- CheckoutPage.py
Оформление заказа
- api_client.py
API клиент

## test
- test_ui
UI тесты  
- test_api
 API тесты

## Доп.файлы:
- conftest.py
Конфигурация фикстур pytest
-  pytest.ini
Настройка pytest
- config.py
Конфигурационный файл
- requirements.txt
Зависимости
- .gitignore
Исключения Git
- README.md
Это описание проекта

## Необходимые зависимости
# Установите все необходимые библиотеки командой:
pip install -r requirements.txt

В requirements.txt обычно указаны:
selenium
pytest
pytest-html
pytest-allure-adaptor
requests

## Инструкции по запуску тестов
1. Запуск UI тестов
pytest -m ui

2. Запуск API тестов
pytest -m api

3. Запуск всех тестов
pytest

4. Формирование отчёта Allure
Запускаете тесты с сохранением результатов:
pytest --alluredir=allure-report

Генерируете и просматриваете отчет:
allure serve allure-report

# Проект для ручного тестирования
Ссылка на финальный проект: https://sainthamster.yonote.ru/share/a367a5ce-5530-4252-9d7a-cd0c8735a590

Руководство по ручному тестированию можно найти в отдельном документе в репозитории или внутри проекта в виде файла README в папке с документацией.

# Дополнительная информация
- Перед запуском убедитесь, что драйвер браузера (например, ChromeDriver) установлен и настроен.
- В конфигурационных файлах можно указать параметры запуска, такие как URL сайта, время ожидания и т.п.
- Для формирования Allure-отчета необходимо установить сам allure-commandline:
pip install allure-python-commons
