from selenium.webdriver.common.by import By
from .basePage import BasePage

class DashboardClientPage(BasePage):
    TITLEFIELD = (By.ID, "title-SkillUp")
    MYPROJECTS = (By.ID, "projects-link")

    def is_search_displayed(self):
        return self.find_element(self.TITLEFIELD).is_displayed()
    
    def navToMyProjects(self):
        self.click(self.MYPROJECTS)

    