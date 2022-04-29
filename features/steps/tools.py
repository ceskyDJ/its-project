import behave.runner
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


@when('I select Standard "{standard_name}"')
def step_impl(context: behave.runner.Context, standard_name: str) -> None:
    browser: WebDriver = context.selenium

    # Go to "Relations" section
    menu_item = browser.find_element(By.ID, "autotoc-item-autotoc-2")
    menu_item.click()

    # Move to root path (click on button with house icon)
    house_button = browser.find_element(By.XPATH, "//div[@id='formfield-form-widgets-standards']//a[@class='crumb']")
    house_button.click()

    # Enter name of the item to search
    search_field = browser.find_element(By.ID, "s2id_autogen14")
    search_field.send_keys(standard_name)

    # Select standard
    search_result = browser.find_element(
        By.XPATH, f"//div[@id='select2-drop']//li[1]//a[contains(@class, 'selectable')]"
    )
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable(search_result)).click()
