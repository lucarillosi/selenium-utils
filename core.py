from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium import webdriver
import logging
from selenium.webdriver.remote.webdriver import WebDriver

MAX_WAIT = 10


def get_connected_driver(hostname: str = 'localhost:4444', chrome_options=webdriver.ChromeOptions()) -> WebDriver:
    """Create a driver and wait for chrome connection

    Returns
    -------
    driver
        The connected driver
    """

    while True:
        try:
            logging.info("Connecting to chrome")
            driver = webdriver.Remote(
                command_executor=f'http://{hostname}/wd/hub',
                options=chrome_options
            )
            logging.info("Chrome connected")
            return driver
        except:
            logging.info("Cannot connect to chrome. Retrying...")
            time.sleep(1)


def wait_for_element(
        driver,
        selector: str,
        selector_strategy=By.CSS_SELECTOR,
        search_strategy="visibility",
        max_wait=MAX_WAIT
):
    """Waits for the specified element to be available on the page and returns it.
    Raises TimeoutException if element is not present after {max_wait} seconds.

    Parameters
    ----------
    selector
        Selector string such as .example-class
    selector_strategy
        Selector type such as selenium.webdriver.common.by.By.CSS_SELECTOR
    search_strategy
        When to consider the element as ready. Allowed values are "visibility"|"presence"

    Returns
    -------
    Selected element

    Raises
    ------
    TimeoutException if element is not present after {max_wait} seconds.
    """

    try:
        if search_strategy == "visibility":
            logging.info(f'Waiting for element {selector} visibility')
            return WebDriverWait(driver, max_wait)\
                .until(EC.visibility_of_element_located((selector_strategy, selector)))
        elif search_strategy == "presence":
            logging.info(f'Waiting for element {selector} presence')
            return WebDriverWait(driver, max_wait)\
                .until(EC.presence_of_element_located((selector_strategy, selector)))
        else:
            raise NotImplementedError(f'Search strategy must be visibility|presence, got {search_strategy}')
    except TimeoutException as e:
        logging.info("Loading took too much time!")
        raise e


def wait_for_element_by_text(driver, text: str, element='*', classes=None, search_strategy="visibility", max_wait=MAX_WAIT):
    """Waits for the element with specified text to be available on the page and returns it.
    Raises TimeoutException if element is not present after {max_wait} seconds.
    For details and additional params see core.wait_for_element

    Parameters
    ----------
    text
        Exact element text e.g. "Click here"
    element (optional)
        Element type e.g. "div" or "button"
    classes (optional)
        Element classes e.g. btn-primary (MUST PROVIDE ALL ELEMENT CLASSES, not only one)

    Returns
    -------
    Selected element

    Raises
    ------
    TimeoutException if element is not present after {max_wait} seconds.
    """

    # Text selector
    selectors = [f'normalize-space()=\'{text}\'']

    if classes is not None:
        # Add class selector
        selectors.append(f'@class=\'{classes}\'')
    selector_string = " and ".join(selectors)

    xpath_selector = f'//{element}[{selector_string}]'
    return wait_for_element(driver,
                            selector=xpath_selector,
                            selector_strategy=By.XPATH,
                            search_strategy=search_strategy,
                            max_wait=max_wait
                            )


def click_noninteractable_elm(driver, element):
    """Click on provided element by raising JS "click" event instead
    of mouse-clicking it. Useful if element is not visible and therefore
    not mouse-clickable.

    Parameters
    ----------
    element
        Selenium web element
    """
    driver.execute_script("$(arguments[0]).click();", element)
