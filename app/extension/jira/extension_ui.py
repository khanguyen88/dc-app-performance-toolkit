from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from util.conf import JIRA_SETTINGS


def view_notification_page(webdriver, datasets):
    page = BasePage(webdriver)
    project_key = "DEV"

    @print_timing("selenium_view_notification_page:view_root")
    def measure_root_page():
        @print_timing("selenium_view_notification_page:view_root")
        def visit_root():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/ConfigureTeams.jspa?projectKey={project_key}")
            page.wait_until_visible((By.ID, "slack-project-config"))  # Wait for summary field visible
        visit_root()

        @print_timing("selenium_view_notification_page:view_config")
        def measure_config_page():
            configure_button = page.get_elements((By.CSS_SELECTOR, "#slack-project-config button.aui-button-link"))[1]
            configure_button.click()
            page.wait_until_visible((By.ID, "jqlform"))  # Wait for summary field visible
        measure_config_page()
    measure_root_page()

