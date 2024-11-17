from selenium.webdriver.common.by import By
from .basePage import BasePage

class DashboardFreelancerPage(BasePage):
    TITLEFIELD = (By.ID, "title-SkillUp")
    BROWSEPROJECTS = (By.ID, "find-work-link")

    def is_search_displayed(self):
        return self.find_element(self.TITLEFIELD).is_displayed()
    
    def navToBrowseProjects(self):
        self.click(self.BROWSEPROJECTS)

    