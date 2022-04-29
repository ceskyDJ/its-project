from typing import Callable, TypeVar

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


T = TypeVar('T')


def use_tinymce_input(browser: WebDriver, frame_id: str, function: Callable[[WebElement], T]) -> T:
    """
    Calls given function on TinyMCE input field

    :param browser: Instance of open browser (webdriver)
    :param frame_id: Identifier of TinyMCE input field box (mceu_[0-9]+)
    :param function: Function to call on TinyMCE input
    :return: Result of called function
    """
    # Switch to TinyMCE iframe (it has own DOM)
    frame = browser.find_element(By.XPATH, f"//div[@id='{frame_id}']//iframe")
    browser.switch_to.frame(frame)

    # Clear TinyMCE input field
    input_field = browser.find_element(By.ID, "tinymce")
    function_result = function(input_field)

    # Restore frame selection
    browser.switch_to.parent_frame()

    return function_result


def fill_tinymce(browser: WebDriver, frame_id: str, content: str) -> None:
    """
    Fills TinyMCE input field with specified content

    :param browser: Instance of open browser (webdriver)
    :param frame_id: Identifier of TinyMCE input field box (mceu_[0-9]+)
    :param content: Content to fill in
    """
    use_tinymce_input(browser, frame_id, lambda input_field: input_field.send_keys(content))


def clear_tinymce(browser: WebDriver, frame_id: str) -> None:
    """
    Clears content of TinyMCE input field

    :param browser: Instance of open browser (webdriver)
    :param frame_id: Identifier of TinyMCE input field box (mceu_[0-9]+)
    """
    use_tinymce_input(browser, frame_id, lambda input_field: input_field.clear())


def javascript_click(browser: WebDriver, button: WebElement) -> None:
    """
    Click on the button with Javascript (guaranteed)

    It is good for situations, when HTML link (tag `a`) has classic href attribute (not `javascript:void(0);`).
    It these situations Selenium sometimes use the button like basic HTML link (tag `a`) instead of using Javascript
    on click handler.

    :param browser: Instance of open browser (webdriver)
    :param button: Button to click on
    """
    browser.execute_script("arguments[0].href = 'javascript:void(0);';", button)
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable(button)).click()
