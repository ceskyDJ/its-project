Feature: Manipulation with Tools

  Scenario: [8] Creating Tool with more selected Standards
    Given I am logged in as user with privileges to manage Tools
    And I opened form "Add Tool"
    And I have Standard "ISO111213"
    And I have Standard "ECM121-1/00-12-042"
    When I fill in required fields
    And I select Standard "ISO111213"
    And I select Standard "ECM121-1/00-12-042"
    And I save Add Tool form
    Then I should be on page with created Tool's detail
    And I should see information message "Item created"
    And I should see Standard "ISO111213" in "Standards"
    And I should see Standard "ECM121-1/00-12-042" in "Standards"

  Scenario: [9] Submitting Tool for publication
    Given I am logged in as user with privileges to manage Tools
    And I have Tool "Tool for submit"
    And State of Tool "Tool for submit" is "Private"
    When I submit for publication Tool "Tool for submit"
    Then State of Tool "Tool for submit" should be "Pending review"
    And I should see information message "Item state changed"
    And Tool "Tool for submit" should be visible for user with reviewing privileges

  Scenario: [10] Rejecting Tool waiting for review by reviewer without administrator rights
    Given I am logged in as user with privileges for reviewing Tools but not for their administration
    And I have Tool "Bad tool"
    And State of Tool "Bad tool" is "Pending review"
    When I reject submitting of the Tool "Bad tool"
    Then State of Tool "Tool for submit" should be "Private"
    And I should see information message "Item state changed"
    And I should be redirected to page "Insufficient Privileges"

  Scenario: [11] Approving Tool waiting for review
    Given I am logged in as user with privileges for reviewing Tools
    And I have Tool "Correct new tool"
    And State of Tool "Correct new tool" is "Pending review"
    When I approve the Tool "Correct new tool"
    Then State of Tool "Correct new tool" should be "Published"
    And I should see information message "Item state changed"
    And Tool "Correct new tool" should be visible to not logged in user
