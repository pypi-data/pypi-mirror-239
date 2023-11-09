import time

from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

SETTINGS_TITLE = (By.XPATH, "//*[contains(text(), 'Settings')]")
NETWORK_OPTION = (By.XPATH, "//*[contains(text(), 'Network')]")
NETWORK_TITLE = (By.XPATH, "//*[contains(@class, 'chakra-text css-1xs2h3i')]")
NETWORK_SELECT = (By.XPATH, "//select[contains(@class, 'chakra-select')]")


class NamiSettingsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_on_settings_window(self):
        """
        check if settings window loaded
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("SETTINGS", SETTINGS_TITLE)

    def click_on_network(self):
        """
        click on network
        """
        self.click("NETWORK_OPTION", NETWORK_OPTION)

    def is_on_network_window(self):
        """
        check if network page loaded
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("NETWORK_OPTION", NETWORK_OPTION)

    def click_on_network_select(self):
        """
        click on network select
        """
        self.click("NETWORK_SELECT", NETWORK_SELECT)

    def choose_network(self, network="Preprod"):
        """
        choose network
        """
        time.sleep(2)
        CHOOSE_NETWORK = (By.XPATH, f"//*[contains(text(), '{network}')]")

        self.click("CHOOSE_NETWORK", CHOOSE_NETWORK)

        # Click on somewhere in the page to close the window if did not close
        action_chains = ActionChains(self.driver)
        action_chains.move_by_offset(200, 300).click().perform()
