from selenium.webdriver.common.by import By
import logging
from . import core
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver

ADDITIVE_DELAY = 2  # delay used to slow down the execution in production mode


def login(driver: WebDriver, user: str, passwd: str) -> WebDriver:
    """Log in webdriver using provided credentials.
    """

    logging.info("Logging in...")
    driver.get("https://teams.microsoft.com")
    logging.info("Username step")
    core.wait_for_element(driver, "loginfmt", By.NAME).send_keys(user)
    core.wait_for_element(driver, "idSIButton9", By.ID).click()
    logging.info("Passwd step")
    core.wait_for_element(driver, "passwd", By.NAME).send_keys(passwd)
    core.wait_for_element(driver, "idSIButton9", By.ID).click()
    logging.info("Save credentials step")
    core.wait_for_element(driver, "KmsiCheckboxField", By.ID).click()
    core.wait_for_element(driver, "idSIButton9", By.ID).click()
    logging.info("Waiting for full web app load to complete")
    core.wait_for_element(driver, "div.teams-grid-header", By.CSS_SELECTOR)
    logging.info("Login completed")
    return driver


def scrape_team_recordings_urls(driver: WebDriver, recordings_page_url: str) -> List[str]:
    """Copies all recording sharepoint urls from team recording page

    Returns
    -------
    A list with all the urls
    """

    logging.info("Navigating to team recordings page")
    driver.get(recordings_page_url)

    # Get all three-dots-menu buttons
    try:
        core.wait_for_element(driver, 'button[title=\'Show actions\']', By.CSS_SELECTOR, "presence")
        menu_btns = driver.find_elements_by_css_selector('button[title=\'Show actions\']')
    except:
        menu_btns = []
    logging.info(f'{len(menu_btns)} menu buttons found')

    # Scrape each video url
    video_urls = []
    for i, menu_btn in enumerate(menu_btns):
        # Open modal
        core.click_noninteractable_elm(driver, menu_btn)
        core.wait_for_element_by_text(driver, 'Copy link').click()
        # Get url inside modal
        url_box = core.wait_for_element(driver, "input[aria-label=\'Copy link\']", By.CSS_SELECTOR)
        video_url = url_box.get_attribute('value')
        video_urls.append(video_url)
        logging.info(f'Scraped video URL {video_url}')
        # Close modal
        core.wait_for_element_by_text(driver, 'Copy', element='button').click()
    logging.info("Team urls scraped successfully")
    return video_urls
