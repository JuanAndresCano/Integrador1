from selenium.webdriver.common.by import By
from .basePage import BasePage

class ClientProjectPage(BasePage):
    CREATEPROJECTBUTTON = (By.ID, "create-project")

    PROJECTS_LIST = (By.CLASS_NAME, "project-list")
    
    PROJECT_TITLES = (By.CSS_SELECTOR, ".project-card h4")

    def createProject(self):
        self.click(self.CREATEPROJECTBUTTON)

    def projectDisplayed(self, title):

        project_titles = self.find_elements(self.PROJECT_TITLES)
        
        # Verificar si el título específico está en la lista de proyectos
        for project in project_titles:
            if title in project.text:
                return True  # Si el título se encuentra, se ha creado el proyecto

        return False