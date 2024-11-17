from behave import given, when, then
from selenium import webdriver
from pages.loginPage import LoginPage
from pages.landpagePage import LandpagePage
from pages.dashboardClientPage import DashboardClientPage
from pages.clientProjectPage import ClientProjectPage
from pages.createProjectPage import CreateProjectPage

#Scenario: Successful login with valid credentials

@given('the user is on the login page')
def stepUserIsInLandpagePage(context):
    context.driver = webdriver.Chrome()
    context.driver.get('http://127.0.0.1:8000/login/')
    context.landpagePage = LoginPage(context.driver)

@when('the user logs in with a valid username and password')
def stepUserLogsValidUsernameAndPassword(context):
    context.loginPage = LoginPage(context.driver)
    context.loginPage.login("maria_lopez","Skillup123")

@when('the user navigates to "My Projects" page')
def stepUserLogsValidUsernameAndPassword(context):
    context.dashboardFreelancerPage = DashboardClientPage(context.driver)
    context.dashboardFreelancerPage.navToMyProjects()

@when('the user clicks the "Create Project" button')
def stepUserLogsValidUsernameAndPassword(context):
    context.clientProjectPage = ClientProjectPage(context.driver)
    context.clientProjectPage.createProject()

@when('the user fills in the project creation form with valid data')
def stepUserLogsValidUsernameAndPassword(context):
    context.createProjectPage = CreateProjectPage(context.driver)
    context.createProjectPage.createProject("title", "position", "descriptioooooooooooooooooooooooooooooooooon", 5400, 100)
    
@then('the new project should be displayed in the "My Projects" page')
def stepUserLogsValidUsernameAndPassword(context):
    context.clientProjectPage = ClientProjectPage(context.driver)
    assert context.clientProjectPage.projectDisplayed("title")
