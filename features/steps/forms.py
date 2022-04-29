import random

import behave.runner
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from helpers import fill_tinymce


@when('I fill in all required input fields of form "Add {form_name}"')
def step_impl(context: behave.runner.Context, form_name: str) -> None:
    browser: WebDriver = context.selenium

    if form_name == "Tool":
        names = ["Brand new tool", "Bar tool", "Programmer's tool", "Dummy tool", "Low efficient tool",
                 "Teacher's tool", "Pretty good tool"]
        title_input_id = "form-widgets-IDublinCore-title"
    elif form_name == "Method":
        names = ["Lipsum method", "Newly created method", "Foo method", "Cool method for beginners", "Expert method",
                 "Super efficient method", "Student's method", "Best method"]
        title_input_id = "form-widgets-IBasic-title"
    elif form_name == "Standard":
        names = ["ISO 12112", "Special standard", "ČSN 156561/4545", "ETA 424242", "ISO 99126"]
        title_input_id = "form-widgets-IDublinCore-title"
    elif form_name == "Organization":
        names = ["Masaryk University", "Redhat", "Microsoft", "Apple", "Commity", "Super testers", "Google"]
        title_input_id = "form-widgets-IBasic-title"
    elif form_name == "Use Case":
        names = ["Simple Use Case", "Very complex Use Case", "Traditional Use Case", "Extraordinary Use Case"]
        title_input_id = "form-widgets-IBasic-title"
    elif form_name == "Test Case":
        names = ["Basic Test Case", "More complex Test Case", "Limit values Test Case", "IO Test Case"]
        title_input_id = "form-widgets-IBasic-title"
    elif form_name == "Evaluation Scenario":
        names = ["Regular Evaluation Scenario", "Long Evaluation Scenario", "Boring Evaluation Scenario"]
        title_input_id = "form-widgets-IBasic-title"
    else:
        raise NotImplementedError

    # Title could be already filled by different step
    title_input = browser.find_element(By.ID, title_input_id)
    if title_input.get_attribute("value") == "":
        name_index = random.randrange(len(names))
        title_input.send_keys(names[name_index])

        # Save information about selected tool's name
        context.item_name = names[name_index]

    if form_name == "Tool" or form_name == "Method":
        purposes_input = browser.find_element(By.ID, f"form-widgets-{form_name.lower()}_purpose")
        purposes_input.send_keys(f"{form_name}'s purpose and main benefits")

        fill_tinymce(browser, "mceu_133", f"Detailed description of the {form_name.lower()}")

        fill_tinymce(browser, "mceu_94", f"Strengths of the {form_name.lower()}")

        fill_tinymce(browser, "mceu_55", f"{form_name}'s limitations")
    elif form_name == "Organization":
        first_chars = [word[0].upper() for word in context.item_name.split(" ")]
        acronym = ''.join(first_chars)

        acronym_input = browser.find_element(By.ID, "form-widgets-organization_acronym")
        acronym_input.send_keys(acronym)
    elif form_name == "Use Case":
        fill_tinymce(browser, "mceu_16", f"Detailed description of the Use Case")
    elif form_name == "Test Case":
        use_case_number = random.randrange(0, 9)
        test_case_number = random.randrange(0, 9)

        id_input = browser.find_element(By.ID, "form-widgets-test_case_id")
        id_input.send_keys(f"UC{use_case_number}_TC_{test_case_number}")
    elif form_name == "Evaluation Scenario":
        id_textarea = browser.find_element(By.ID, "form-widgets-evaluation_secnario_id")
        id_textarea.send_keys(f"Evaluation Scenario's connections between Test Cases and Requirements")

        description_input = browser.find_element(By.ID, "form-widgets-evaluation_scenario_textual_description")
        description_input.send_keys("Description of the Evaluation Scenario")


@given('I have {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str) -> None:
    browser: WebDriver = context.selenium

    context.execute_steps(f'Given I opened form "Add {item_type}"')

    if item_type in ["Tool", "Standard"]:
        title_input_id = "form-widgets-IDublinCore-title"
    elif item_type in ["Method", "Organization", "Use Case", "Test Case", "Evaluation Scenario"]:
        title_input_id = "form-widgets-IBasic-title"
    else:
        raise NotImplementedError

    title_input = browser.find_element(By.ID, title_input_id)
    title_input.send_keys(item_name)

    # Add item name for future usage
    context.item_name = item_name

    context.execute_steps(f'''
        When I fill in all required input fields of form "Add {item_type}"
        And I save Add {item_type} form
    ''')

    # Backup URL of created item
    context.urls[item_name] = browser.current_url

    # Go back to the main page
    browser.get(context.url)


@when('I save {form_name} form')
def step_impl(context: behave.runner.Context, form_name: str) -> None:
    browser: WebDriver = context.selenium

    if not form_name.startswith("Add") and not form_name.startswith("Edit"):
        raise NotImplementedError

    save_form_button = browser.find_element(By.ID, "form-buttons-save")
    save_form_button.click()


@then('I should see form error message "{message_content}"')
def step_impl(context: behave.runner.Context, message_content: str) -> None:
    browser: WebDriver = context.selenium

    message_element = browser.find_element(By.XPATH, "//div[@id='content-core']//dl[@class='portalMessage error']")
    assert message_element.text == f"Error {message_content}"


@then('I should be in "{form_name}" form')
def step_impl(context: behave.runner.Context, form_name: str) -> None:
    browser: WebDriver = context.selenium

    main_heading = browser.find_element(By.XPATH, "//article[@id='content']/h1")

    assert main_heading.text.strip() == form_name


@then('"{tab_name}" tab should be opened')
def step_impl(context: behave.runner.Context, tab_name: str) -> None:
    browser: WebDriver = context.selenium

    tab_menu_buttons: list[WebElement] = browser.find_elements(By.XPATH, "//nav[@class='autotoc-nav']/a")

    for menu_button in tab_menu_buttons:
        if menu_button.text == tab_name:
            assert "active" in menu_button.get_attribute("class")
            return

    raise ValueError(f"Tab {tab_name} doesn't exists in this form")
