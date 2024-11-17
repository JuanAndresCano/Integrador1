from behave import given, when, then
from selenium import webdriver
from pages.loginPage import LoginPage
from pages.dashboardFreelancerPage import DashboardFreelancerPage
from pages.browseProjectPage import BrowseProjectPage
from pages.informationProjectPage import InformationProjectPage

@when('the user navigates to "Browse Projects" page')
def stepUserLogsValidUsernameAndPassword(context):
    context.dashboardFreelancerPage = DashboardFreelancerPage(context.driver)
    context.dashboardFreelancerPage.navToBrowseProjects()

@when('the user clicks the first project')
def stepUserLogsValidUsernameAndPassword(context):
    context.browseProjectPage = BrowseProjectPage(context.driver)
    context.browseProjectPage.navFirstProject()

@then('the project information is show')
def stepUserLogsValidUsernameAndPassword(context):
    context.informationProjectPage = InformationProjectPage(context.driver)
    assert context.informationProjectPage.is_search_displayed()

@when('the first project information is show')
def stepUserLogsValidUsernameAndPassword(context):
    context.informationProjectPage = InformationProjectPage(context.driver)
    assert context.informationProjectPage.is_search_displayed()

@when('the user goes back to "Browse Projects" page')
def stepUserLogsValidUsernameAndPassword(context):
    context.informationProjectPage = InformationProjectPage(context.driver)
    context.informationProjectPage.navToBrowseProjects()
    
@when('the user clicks the second project')
def stepUserLogsValidUsernameAndPassword(context):
    context.browseProjectPage = BrowseProjectPage(context.driver)
    context.browseProjectPage.navSecondProject()

@then('the second project information is show')
def stepUserLogsValidUsernameAndPassword(context):
    context.informationProjectPage = InformationProjectPage(context.driver)
    assert context.informationProjectPage.is_search_displayed()