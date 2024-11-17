Feature: Login Feature

  Scenario: Successful login with valid credentials client
    Given the user is on the landpage
    When the user clicks the login button on the landpage
    And the freelancer user logs with a valid username and password
    Then the freelancer user should be redirected to the dashboard page

  Scenario: Successful login with valid credentials freelancer
    Given the user is on the landpage
    When the user clicks the login button on the landpage
    When the client user logs in with a valid username and password
    Then the client user should be redirected to the dashboard page

  Scenario: Unsuccessful login with invalid credentials
    Given the user is on the landpage
    When the user clicks the login button on the landpage
    And the user logs with an invalid username and password
    Then an error message should be displayed

  Scenario: Empty login credentials
    Given the user is on the landpage
    When the user clicks the login button on the landpage
    And the user logs with the username and password fields empty
    Then an error message should be displayed

  