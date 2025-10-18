Feature: Test Steps 1-9 (Volume and Resolution)

  Scenario: Test complete playback with volume and resolution changes
    Given I am on the FYC platform
    When I login with PIN
    Then I should be logged in
    When I navigate to Test Automation Project
    Then I should see the project page
    
    When I click Details tab if it exists
    And I wait for 10 seconds
    When I click Videos tab if it exists
    
    When I click on the video card
    Then the video modal should open
    When I play the video
    And I wait for 15 seconds
    When I rewind the video by 10 seconds
    And I pause the video
    When I toggle fullscreen
    When I click Continue Watching
    When I set volume to 50 percent
    When I change resolution to "480p"
    When I change resolution to "720p"

    When I pause the video
    And I click Back button
    When I logout
    Then I should be logged out


