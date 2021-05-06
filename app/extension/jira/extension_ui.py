import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS
import os


def import_mpp(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("import_mpp:user_login")
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

    @print_timing("import_mpp:do_import_wedding_file")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ImportMpp!default.jspa")

        page.wait_until_visible((By.ID, "mppFile"))
        page.get_element((By.ID, "mppFile")).send_keys(os.getcwd() + "/example.mpp")

        page.get_element((By.ID, "project")).send_keys("WEDDING")
        page.get_element((By.ID, "aui-uid-0-0")).click()

        page.get_element((By.ID, "issueType")).send_keys("Task")
        page.get_element((By.ID, "aui-uid-1-0")).click()

        page.get_element((By.ID, "issue-label")).send_keys("wedding")

        page.get_element((By.CSS_SELECTOR, "#mpp2jira-form input[type='submit']")).click()

        page.wait_until_visible((By.ID, "submitBtn"))
        page.get_element((By.ID, "submitBtn")).click()

    measure()

