Feature: Browse and Apply to Project

  Scenario: Apply to a project
    Given the user is on the login page
    When the freelancer logs in with a valid username and password
    And the user navigates to "Browse Projects" page
    And the user clicks the first project
    And the user clicks the "Apply Project" button
    Then the system should confirm the application was successful