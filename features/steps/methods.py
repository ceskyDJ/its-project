import behave.runner
from behave import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from helpers import clear_tinymce


@when('I move to "{tab_name}" section')
def step_impl(context: behave.runner.Context, tab_name: str) -> None:
    browser: WebDriver = context.selenium

    if tab_name == "Method Dimensions":
        tab_id = "autotoc-item-autotoc-1"
    elif tab_name == "Relations":
        tab_id = "autotoc-item-autotoc-2"
    else:
        raise NotImplementedError

    menu_item = browser.find_element(By.ID, tab_id)
    menu_item.click()


@given('I went to tab "{tab_name}"')
def step_impl(context: behave.runner.Context, tab_name: str) -> None:
    context.execute_steps(f'When I move to "{tab_name}" section')


@when('I select "In-the-lab environment" and "Closed evaluation environment" in field "Evaluation Environment Type"')
def step_impl(context: behave.runner.Context) -> None:
    browser: WebDriver = context.selenium

    in_lab_env_option = browser.find_element(By.ID, "form-widgets-evaluation_environment_type-0")
    in_lab_env_option.click()

    closed_eval_env_option = browser.find_element(By.ID, "form-widgets-evaluation_environment_type-1")
    closed_eval_env_option.click()


@when('I select "Model" and "Software" in field "Type of Component Under Evaluation"')
def step_impl(context: behave.runner.Context) -> None:
    browser: WebDriver = context.selenium

    model_option = browser.find_element(By.ID, "form-widgets-type_of_component_under_evaluation-0")
    model_option.click()

    software_option = browser.find_element(By.ID, "form-widgets-type_of_component_under_evaluation-1")
    software_option.click()


@then('I should see "In-the-lab environment" and "Closed evaluation environment" under "Evaluation Environment Type"')
def step_impl(context: behave.runner.Context) -> None:
    browser: WebDriver = context.selenium

    eval_env_type = browser.find_element(By.ID, "form-widgets-evaluation_environment_type")
    selected_options_elements = eval_env_type.find_elements(By.TAG_NAME, "span")

    extracted_options = [option.text for option in selected_options_elements]

    assert "In-the-lab environment" in extracted_options
    assert "Closed evaluation environment" in extracted_options


@then('I should see "Model" and "Software" under "Type of Component Under Evaluation"')
def step_impl(context: behave.runner.Context) -> None:
    browser: WebDriver = context.selenium

    type_comp_under_eval = browser.find_element(By.ID, "form-widgets-type_of_component_under_evaluation")
    selected_options_elements = type_comp_under_eval.find_elements(By.TAG_NAME, "span")

    extracted_options = [option.text for option in selected_options_elements]

    assert "Model" in extracted_options
    assert "Software" in extracted_options


@when('I try to search {field_name} "{searched_item}"')
def step_impl(context: behave.runner.Context, field_name: str, searched_item: str) -> None:
    browser: WebDriver = context.selenium

    if field_name == "Tool":
        input_field_id = "formfield-form-widgets-tools"
        search_field_id = "s2id_autogen12"
    elif field_name == "Standard":
        input_field_id = "formfield-form-widgets-standards"
        search_field_id = "s2id_autogen6"
    elif field_name == "Test Case or Verification and Validation activity":
        input_field_id = "formfield-form-widgets-test_case_or_verification_and_validation_activity"
        search_field_id = "s2id_autogen8"
    else:
        raise NotImplementedError

    # Move to root path (click on button with house icon)
    house_button = browser.find_element(By.XPATH, f"//div[@id='{input_field_id}']//a[@class='crumb']")
    house_button.click()

    # Enter name of the item to search
    search_field = browser.find_element(By.ID, search_field_id)
    search_field.send_keys(searched_item)


@then('I should be able to select {field_name} "{referenced_item}" by clicking on its name')
def step_impl(context: behave.runner.Context, field_name: str, referenced_item: str) -> None:
    browser: WebDriver = context.selenium

    try:
        search_result = browser.find_element(
            By.XPATH, f"//div[@id='select2-drop']//li[1]//a[contains(@class, 'selectable')]"
        )
        WebDriverWait(browser, 15).until(EC.element_to_be_clickable(search_result)).click()
    except (NoSuchElementException, TimeoutException):
        assert False


@given('Method "{method_name}" has referenced {field_name} "{referenced_item}"')
def step_impl(context: behave.runner.Context, method_name: str, field_name: str, referenced_item: str) -> None:
    context.execute_steps(f'''
        When I open "Edit Method" form for Method "{method_name}"
        And I move to "Relations" section
    ''')

    # Search for referenced item
    context.execute_steps(f'When I try to search {field_name} "{referenced_item}"')

    # Select searched item
    context.execute_steps(f'Then I should be able to select {field_name} "{referenced_item}" by clicking on its name')

    context.execute_steps('When I save Edit Method form')


@when('I cancel selection of {field_name} "{referenced_item}"')
def step_impl(context: behave.runner.Context, field_name: str, referenced_item: str) -> None:
    browser: WebDriver = context.selenium

    if field_name == "Tool":
        selected_items_box_id = "s2id_autogen11"
    elif field_name == "Standard":
        selected_items_box_id = "s2id_autogen5"
    else:
        raise NotImplementedError

    selected_items: list[WebElement] = browser.find_elements(
        By.XPATH,
        f"//div[@id='{selected_items_box_id}']//li[@class='select2-search-choice']"
    )

    for item in selected_items:
        item_name = browser.find_element(By.XPATH, "//span[contains(@class, 'pattern-relateditems-item-title')]")

        if item_name.text.strip() == referenced_item:
            # Click to button for removing the item from selection
            close_button = item.find_element(By.CLASS_NAME, "select2-search-choice-close")
            close_button.click()

            # Selection canceling is done
            return
    else:
        ValueError(f"Entered reference item {referenced_item} is not in selection")

    context.execute_steps('When I save Edit Method form')


@when('I don\'t fill in some of the required fields in form "Add Method"')
def step_impl(context: behave.runner.Context) -> None:
    browser: WebDriver = context.selenium

    context.execute_steps('When I fill in all required input fields of form "Add Method"')

    clear_tinymce(browser, "mceu_133")


@then('I should see message "{wanted_message}" under name of unfilled required field')
def step_impl(context: behave.runner.Context, wanted_message: str) -> None:
    browser: WebDriver = context.selenium

    try:
        error_message = browser.find_element(
            By.XPATH,
            "//div[@id='formfield-form-widgets-method_description']//div[@class='error']"
        )

        assert error_message.text == wanted_message
    except NoSuchElementException:
        assert False


@then('I should see Test Case "{test_case_name}" in the displayed list of Test Cases')
def step_impl(context: behave.runner.Context, test_case_name: str) -> None:
    browser: WebDriver = context.selenium

    # It should be at the first page (it is sorted by publish date and this testing process doesn't create
    # so many new Test Cases)
    search_results = browser.find_elements(
        By.XPATH, f"//div[@id='select2-drop']//li[1]//a[contains(@class, 'selectable')]//span[@title='test_case']"
    )

    for result in search_results:
        if result.text.strip() == test_case_name:
            assert True
            return

    # Searched Use Case not found
    assert False
