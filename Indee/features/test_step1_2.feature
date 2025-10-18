Feature: Test Steps 1 and 2 Only

  Scenario: Test Login and Navigate to Project
    Given I am on the FYC platform
    When I login with PIN
    Then I should be logged in
    When I navigate to Test Automation Project
    Then I should see the project page

