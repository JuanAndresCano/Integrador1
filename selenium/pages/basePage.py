from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 50000

    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.find_element(locator).click()
        time.sleep(1)

    def enter_text(self, locator, text):
        self.find_element(locator).send_keys(text)
        time.sleep(0.3)
