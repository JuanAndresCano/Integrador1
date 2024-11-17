from selenium.webdriver.common.by import By
from .basePage import BasePage

class LandpagePage(BasePage):
    LOGINBUTTON = (By.ID, "loginButton")
    REGISTERBUTTON = (By.ID, "sign-up-button")
    REGISTERFREELANCER = (By.ID, "register-freelancer")
    REGISTERCLIENT = (By.ID, "register-client")

    def login(self):
        self.click(self.LOGINBUTTON)
    
    def register(self):
        self.click(self.REGISTERBUTTON)

    def registerClient(self):
        self.click(self.REGISTERCLIENT)
    
    def registerFreelancer(self):
        self.click(self.REGISTERFREELANCER)

