Feature: Test Steps 1, 2, and 3

  Scenario: Test Login, Navigate, and Open Video
    Given I am on the FYC platform
    When I login with PIN
    Then I should be logged in
    When I navigate to Test Automation Project
    Then I should see the project page
    When I click on the video card
    Then the video modal should open

