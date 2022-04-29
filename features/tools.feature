Feature: Manipulation with Tools

  Scenario: [8] Creating Tool with more selected Standards
    Given I am logged in as user with privileges to manage Tools
    And I have Standard "ISO111213"
    And I have Standard "ECM121-1/00-12-042"
    And I opened form "Add Tool"
    When I fill in all required input fields of form "Add Tool"
    And I select Standard "ISO111213"
    And I select Standard "ECM121-1/00-12-042"
    And I save Add Tool form
    Then I should be on page with created Tool's detail
    And I should see page information message "Item created"
    And Standard "ISO111213" should be in "Standards"
    And Standard "ECM121-1/00-12-042" should be in "Standards"

  Scenario: [9] Submitting Tool for publication
    Given I am logged in as user with privileges to manage Tools
    And I have Tool "Tool for submit"
    And State of Tool "Tool for submit" is "Private"
    When I submit for publication Tool "Tool for submit"
    Then I should see page information message "Item state changed."
    And State of Tool "Tool for submit" should be "Pending review"
    And Tool "Tool for submit" should be visible for user with reviewing privileges

  Scenario: [10] Rejecting Tool waiting for review by reviewer without administrator rights
    Given I am logged in as user with privileges to manage Tools
    And I have Tool "Bad tool"
    And State of Tool "Bad tool" is "Pending review"
    When I log in as user with privileges to review Tools but not for their administration
    And I reject submitting of the Tool "Bad tool"
    Then I should be redirected to page "Insufficient Privileges"

  Scenario: [11] Approving Tool waiting for review
    Given I am logged in as user with privileges to manage Tools
    And I have Tool "Correct new tool"
    And State of Tool "Correct new tool" is "Pending review"
    When I log in as user with privileges to review Tools
    And I approve the Tool "Correct new tool"
    Then I should see page information message "Item state changed."
    And State of Tool "Correct new tool" should be "Published"
    And Tool "Correct new tool" should be visible for not logged in user
