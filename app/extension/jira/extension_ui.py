import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def navigate_to_import_screen(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("app_specific_user_login")
    def app_specific_user_login():
        login_page = Login(webdriver)
        login_page.delete_all_cookies()
        login_page.go_to()
        login_page.set_credentials(username='admin', password='admin')
        if login_page.is_first_login():
            login_page.first_login_setup()
        if login_page.is_first_login_second_page():
            login_page.first_login_second_page_setup()
        login_page.wait_for_page_loaded()
    app_specific_user_login()

    @print_timing("app_specific:import_screen_navigation")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ImportMpp!default.jspa")
        page.wait_until_visible((By.ID, "project-input"))  # Wait for summary field visible
        project_list = page.get_element((By.ID, "project-input"))
        project_list.click()

    measure()

