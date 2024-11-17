Feature: Register Client Feature

  Scenario: Successful Register with valid credentials 
    Given the user is on the landpage
    When the user clicks the register button on the landpage
    And the user clicks the register client button on the landpage
    And the user register a client with valid credentials
    Then the user must be redirected to the login page

  Scenario: Successful Register with valid credentials but already created user and login 
    Given the user is on the landpage
    When the user clicks the register button on the landpage
    And the user clicks the register client button on the landpage
    And the user register a client with valid credentials
    And error is show of already created user
    And the user client go backs to the landpage
    And the user clicks the login button on the landpage
    And the client user logs in with a valid username and password
    Then the client user should be redirected to the dashboard page

  Scenario: Successful Register with valid credentials and login
    Given the user is on the landpage
    When the user clicks the register button on the landpage
    And the user clicks the register client button on the landpage
    And the user register a second client with valid credentials
    Then the user must be redirected to the login page  
  
  Scenario: Register with invalid phone number format
    Given the user is on the landpage
    When the user clicks the register button on the landpage
    And the user clicks the register client button on the landpage
    And the user attempts to register a client with an invalid phone number format
    Then the user should see an error message indicating the phone number is invalid

  Scenario: Register with invalid tax ID format
    Given the user is on the landpage
    When the user clicks the register button on the landpage
    And the user clicks the register client button on the landpage
    And the user attempts to register a client with an invalid tax ID format
    Then the user should see an error message indicating the tax ID is invalid

  Scenario: Register with non-matching passwords
    Given the user is on the landpage
    When the user clicks the register button on the landpage
    And the user clicks the register client button on the landpage
    And the user attempts to register a client with passwords that do not match
    Then the user should see an error message indicating the passwords do not match

  Scenario: Register with empty fields
    Given the user is on the landpage
    When the user clicks the register button on the landpage
    And the user clicks the register client button on the landpage
    And the user attempts to register a client with some fields empty
    Then the user should see an error message indicating that all required fields must be filled
