from selenium.webdriver.common.by import By
from .basePage import BasePage
from selenium.webdriver.common.action_chains import ActionChains

class BrowseProjectPage(BasePage):
    FIRSTPROJECT = (By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/a")
    SECONDPROJECT = (By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/a")

    def navFirstProject(self):
        self.click(self.FIRSTPROJECT)

    def navSecondProject(self):
        self.driver.execute_script("window.scrollBy(0, 500);")  # Ajusta 500 según la altura que necesites
        element = self.find_element(self.SECONDPROJECT)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()
