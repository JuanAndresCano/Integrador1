from selenium.webdriver.common.by import By
from .basePage import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class RegisterClientPage(BasePage):
    FIRSTNAMEFIELD = (By.ID, "id_first_name")
    LASTNAMEFIELD = (By.ID, "id_last_name")
    USERNAMEFIELD = (By.ID, "id_username")
    EMAILFIELD = (By.ID, "id_email")
    PASSWORD1FIELD = (By.ID, "id_password1")
    PASSWORD2FIELD = (By.ID, "id_password2")
    PHONENUMBERFIELD = (By.ID, "id_phoneNumber")
    TAXIDFIELD = (By.ID, "id_taxId")
    COMPANYNAMEFIELD = (By.ID, "id_companyName")
    TYPEOFCOMPANYFIELD = (By.ID, "id_typeOfCompany")
    ADDRESSFIELD = (By.ID, "id_address")
    
    BUSINESSVERTICALFIELD = (By.ID, "id_businessVertical")
    BUSSINESVERTICALELEMENT = (By.XPATH, "/html/body/div/div/div/main/form/div[10]/select/option[4]")
    COUNTRYFIELD = (By.ID, "id_country")
    COUNTRYELEMENT = (By.XPATH, "/html/body/div/div/div/main/form/div[11]/div/select/option[5]")
    CITYFIELD = (By.ID, "id_city")
    CITYELEMENT = (By.XPATH, "/html/body/div/div/div/main/form/div[12]/div/select/option[3]")

    SAMEUSERNAMEERROR = (By.XPATH, "/html/body/div/div/div/main/form/div[2]/div/ul/li")

    # Botón de envío
    SUBMITBUTTON = (By.CSS_SELECTOR, ".btn-submit")

    LANDPAGEBUTTON = (By.ID, "landpage-skillUp")
    

    def register(self, first_name, last_name, username, email, password1, password2, phone_number, tax_id, company_name, type_of_company, address):
        # Ingresar los valores en los campos correspondientes
        self.enter_text(self.FIRSTNAMEFIELD, first_name)
        self.enter_text(self.LASTNAMEFIELD, last_name)
        self.enter_text(self.USERNAMEFIELD, username)
        self.enter_text(self.EMAILFIELD, email)
        self.enter_text(self.PASSWORD1FIELD, password1)
        self.enter_text(self.PASSWORD2FIELD, password2)
        self.enter_text(self.PHONENUMBERFIELD, phone_number)
        self.enter_text(self.TAXIDFIELD, tax_id)
        self.enter_text(self.COMPANYNAMEFIELD, company_name)
        self.enter_text(self.TYPEOFCOMPANYFIELD, type_of_company)
        self.enter_text(self.ADDRESSFIELD, address)
        
        element = self.find_element(self.BUSINESSVERTICALFIELD)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

        self.click(self.BUSSINESVERTICALELEMENT)

        element = self.find_element(self.COUNTRYFIELD)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

        self.click(self.COUNTRYELEMENT)

        element = self.find_element(self.CITYFIELD)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

        self.click(self.CITYELEMENT)

        # Hacer clic en el botón de envío
        element = self.find_element(self.SUBMITBUTTON)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()


    def errorMessageDisplayed(self):
        return self.find_element(self.SAMEUSERNAMEERROR).is_displayed()
    
    def landpageRedirect(self):
        self.click(self.LANDPAGEBUTTON)
    
