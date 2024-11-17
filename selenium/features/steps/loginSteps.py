from behave import given, when, then
from selenium import webdriver
from pages.loginPage import LoginPage
from pages.landpagePage import LandpagePage
from pages.dashboardFreelancerPage import DashboardFreelancerPage
from pages.dashboardClientPage import DashboardClientPage

#Scenario: Successful login with valid credentials

@given('the user is on the landpage')
def stepUserIsInLandpagePage(context):
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.get('http://127.0.0.1:8000/')
    context.landpagePage = LandpagePage(context.driver)

@when('the user clicks the login button on the landpage')
def stepUserPressButtonToLogin(context):
    context.landpagePage.login() 

@when('the freelancer user logs with a valid username and password')
def stepUserLogsValidUsernameAndPassword(context):
    context.loginPage = LoginPage(context.driver)
    context.loginPage.login("andPrz2005","Skillup123")

@then('the freelancer user should be redirected to the dashboard page')
def stepUserRedirectToDashboard(context):
    dashboardFreelancerPage = DashboardFreelancerPage(context.driver)
    assert dashboardFreelancerPage.is_search_displayed()

#Scenario: Unsuccessful login with invalid credentials

@when('the user logs with an invalid username and password')
def stepUserLogsValidUsernameAndPassword(context):
    context.loginPage = LoginPage(context.driver)
    context.loginPage.login("f","free0105")

@then('an error message should be displayed')
def stepUserRedirectToDashboard(context):
    assert context.loginPage.is_search_displayed()

#Scenario: Empty login credentials

@when('the user logs with the username and password fields empty')
def stepUserLogsValidUsernameAndPassword(context):
    context.loginPage = LoginPage(context.driver)
    context.loginPage.login(" "," ")

@when('the client user logs in with a valid username and password')
def stepUserLogsValidUsernameAndPassword(context):
    context.loginPage = LoginPage(context.driver)
    context.loginPage.login("juanperez123","TestPassword123")

@then('the client user should be redirected to the dashboard page')
def stepUserRedirectToDashboard(context):
    dashboardClientPage = DashboardClientPage(context.driver)
    assert dashboardClientPage.is_search_displayed()