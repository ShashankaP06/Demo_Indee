Feature: Test Steps 1-6 (Play and Pause)

  Scenario: Test Login, Navigate, Open Video, Play, and Pause
    Given I am on the FYC platform
    When I login with PIN
    Then I should be logged in
    When I navigate to Test Automation Project
    Then I should see the project page
    When I click on the video card
    Then the video modal should open
    When I play the video
    And I wait for 10 seconds
    And I pause the video
    When I click Continue Watching

