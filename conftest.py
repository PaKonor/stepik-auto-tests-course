# import pytest
# from selenium import webdriver

#
# @pytest.fixture()
# def fixt():
#     print("Start browser")
#     browser = webdriver.Chrome()
#     yield browser
#     print("Close browser")
#     browser.quit()

"""Встроенная фикстура request может получать данные о текущем запущенном тесте,
что позволяет, например, сохранять дополнительные данные в отчёт,
а также делать многие другие интересные вещи"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',  # можно в параметре default указать браузер, который будет ывзываться по умолчанию и не нужно бужет прописывать параметр в запросе в терминале
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language', action='store', default='en',
                     help="Choose language: ru, en")



@pytest.fixture(scope="function")
def fixt(request):
    browser_name = request.config.getoption("browser_name") #логика обработки командной строки в conftest.py.
    user_language = request.config.getoption("language")
    # browser = None
    if browser_name == "chrome":
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        print("\nstart chrome browser for test..")
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", user_language)
        print("\nstart firefox browser for test..")
        browser = webdriver.Firefox(firefox_profile=fp)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()


"""запуск хрома pytest -s -v --browser_name=chrome test_parser.py
запуск firefox pytest -s -v --browser_name=firefox test_parser.py

pytest_addoption(parser) - это метод, который позволяет запускать тест, который зависит от опции командной строки.
А parser - это (в данном случае) атрибут, который считывает значения из строки """
