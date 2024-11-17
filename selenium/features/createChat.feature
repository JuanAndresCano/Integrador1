Feature: Create Chat Feature

  Scenario: Client Create Chat Freelancer List
    Given the user is on the login page
    When the client user logs in with a valid username and password
    And the user navigates to "My Projects" page
    And the user clicks the first project
    Then the project information is show

  Scenario: Client Create Chat Freelancer Request
    Given the user is on the login page
    When the client user logs in with a valid username and password
    And the user navigates to "My Projects" page
    And the user clicks the first project
    Then the project information is show