from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .basePage import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class CreateProjectPage(BasePage):
    TITLEFIELD = (By.ID, "id_title")
    REQUIREDPOSITIONFIELD = (By.ID, "id_requiredPosition")
    DESCRIPTIONFIELD = (By.ID, "id_description")
    DAYSDURATIONFIELD = (By.ID, "id_daysDuration")
    BUDGETFIELD = (By.ID, "id_budget")
    CREATEPROJECTBUTTON = (By.ID, "create-project-button")

    EXPERIENCELEVELFIELD = (By.ID, "id_complexity")
    FIELD = (By.XPATH, "/html/body/main/div/div[1]/form/div[4]/div[2]/div/select/option[2]")

    SKILL = (By.XPATH, "/html/body/main/div/div[1]/form/div[5]/div/div[1]/input")



    def createProject(self, title, requiredPosition, description, budget, days):
        self.enter_text(self.TITLEFIELD, title)
        self.enter_text(self.REQUIREDPOSITIONFIELD, requiredPosition)
        self.enter_text(self.DESCRIPTIONFIELD, description)
        self.enter_text(self.BUDGETFIELD, budget)
        self.enter_text(self.DAYSDURATIONFIELD, days)

        element = self.find_element(self.EXPERIENCELEVELFIELD)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

        #selectElement = self.find_elements(by=By.TAG_NAME, value="Option")
        self.click(self.FIELD)
        
        element = self.find_element(self.SKILL)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

        element = self.find_element(self.CREATEPROJECTBUTTON)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    