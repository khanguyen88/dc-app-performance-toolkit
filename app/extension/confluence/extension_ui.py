from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from util.conf import CONFLUENCE_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("gravatar:import_gravatar")
    def manual_import_gravatar():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/users/profile/editmyprofilepicture.action")
        page.wait_until_visible((By.ID, "gravatar-importer-button"))  # Wait for title field visible

        import_button = page.get_element((By.ID, "gravatar-importer-button"))
        import_button.click()

        page.wait_until_visible((By.ID, "gravatar-importer-submit-button"))
        submit_button = page.get_element((By.ID, "gravatar-importer-submit-button"))
        submit_button.click()

        page.wait_until_invisible((By.ID, "gravatar-importer-dialog"))

    manual_import_gravatar()
