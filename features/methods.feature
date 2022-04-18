Feature: Manipulating with Methods

  Background:
    Given I am logged in as user with privileges to manage Use Cases

  Scenario: [12] Creating Method with entered Method Dimensions
    Given I opened form "Add Method"
    When I fill in all required input fields
    And I select "In-the-lab environment" and "Closed evaluation environment" in field "Evaluation Environment Type"
    And I select "Model" and "Software" in field "Type of Component Under Evaluation"
    And I save Add Method form
    Then I should be on page with created Method's detail
    And I should see information message "Item created"
    And I should see "In-the-lab environment" and "Closed evaluation environment" under "Evaluation Environment Type"
    And I should see "Model" and "Software" under "Type of Component Under Evaluation"

  Scenario: [13] Deleting Method relation with Tool and Standard
    Given I have Method "Relation-rich method"
    And Method "Relation-rich method" has referenced tool "Ref tool"
    And Method "Relation-rich method" has referenced Standard "Ref standard"
    When I open "Edit Method" form for Method "Relation-rich method"
    And I remove Tool "Ref tool"
    And I remove Standard "Ref standard"
    And I save Edit Method form
    Then I should be on detail page of Method "Relation-rich method"
    And I should see information message "Changes saved"
    And Tool "Ref tool" should not be contained in "Tools"
    And Standard "Ref standard" should not be contained in "Standards"

  Scenario: [14] Creating Method without required fields
    Given I opened "Add Method" form
    When I don't fill in some of the required fields
    And I save Add Method form
    Then I should see error message "There were some errors."
    And I should see message "Required input is missing." under name of unfilled required field

  Scenario: [15] Searching for Test Case in Add Method form
    Given I have Test Case "My Test Case"
    And I opened "Add Method" form
    And I went to tab "Relations"
    When I click into field "Test Case or Verification and Validation activity"
    And I click on home icon
    And I type "My"
    Then I should see Test Case "My Test Case" in the displayed list of Test Cases
    And I should be able to select Test Case "My Test Case" by clicking on its name
