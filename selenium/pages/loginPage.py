from selenium.webdriver.common.by import By
from .basePage import BasePage

class LoginPage(BasePage):
    USERNAMEFIELD = (By.ID, "username")
    PASSWORDFIELD = (By.ID, "password")
    LOGINBUTTON = (By.ID, "buttonLogin")
    MESSAGEERROR = (By.ID, "messagesk")
    LOGINTITLE = (By.XPATH, "/html/body/main/div/h2")
    

    def login(self, username, password):
        self.enter_text(self.USERNAMEFIELD, username)
        self.enter_text(self.PASSWORDFIELD, password)
        self.click(self.LOGINBUTTON)

    def is_search_displayed(self):
        return self.find_element(self.MESSAGEERROR).is_displayed()
    
    def isLoginDisplayed(self):
        return self.find_element(self.LOGINTITLE).is_displayed()
