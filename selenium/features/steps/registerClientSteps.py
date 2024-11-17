from behave import given, when, then
from selenium import webdriver
from pages.registerClientPage import RegisterClientPage
from pages import *
from pages.loginPage import LoginPage

@when('the user clicks the register button on the landpage')
def stepUserClicksRegisterButton(context):
    context.landpagePage.register()

@when('the user clicks the register client button on the landpage')
def stepUserClicksRegisterClientButton(context):
    context.landpagePage.registerClient()

@when('the user register a client with valid credentials')
def stepUserRegistersClientWithValidCredentials(context):
    context.registerClientPage = RegisterClientPage(context.driver)
    context.registerClientPage.register(
        first_name='Juan', 
        last_name='Perez', 
        username='juanperez123', 
        email='juanperez@example.com', 
        password1='TestPassword123', 
        password2='TestPassword123', 
        phone_number='987654321', 
        tax_id='9876543210', 
        company_name='Empresa Test', 
        type_of_company='Retail', 
        address='Calle Falsa 123, Ciudad, País'
    )
    
@when('the user register a second client with valid credentials')
def stepUserClicksRegisterClientButton(context):
    context.registerClientPage = RegisterClientPage(context.driver)
    context.registerClientPage.register(
        first_name='Maria', 
        last_name='Lopez', 
        username='mariaLopez1', 
        email='mariaLopez@example.com', 
        password1='TestPassword123', 
        password2='TestPassword123', 
        phone_number='123456789', 
        tax_id='12345678901', 
        company_name='Empresa Test', 
        type_of_company='Retail', 
        address='Calle Falsa 123, Ciudad, País'
    )

@when('error is show of already created user')
def stepUserClicksRegisterClientButton(context):
    context.registerClientPage.errorMessageDisplayed()
    
@when('the user client go backs to the landpage')
def stepUserClicksRegisterClientButton(context):
    context.registerClientPage.landpageRedirect()

@then('the user must be redirected to the login page')
def stepUserIsRedirectedToLoginPage(context):
    context.loginPage = LoginPage(context.driver)
    assert context.loginPage.isLoginDisplayed()

