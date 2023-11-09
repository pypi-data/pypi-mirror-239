import time

import pytest
from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.namiPages.NamiConnectWalletPage import NamiConnectWalletPage
from dcentralab_qa_infra_automation.pages.namiPages.NamiCreateAccountPage import NamiCreateAccountPage
from dcentralab_qa_infra_automation.pages.namiPages.NamiImportSeedPhrasePage import NamiImportSeedPhrasePage
from dcentralab_qa_infra_automation.pages.namiPages.NamiBasePage import NamiBasePage
from dcentralab_qa_infra_automation.pages.namiPages.NamiSignPage import NamiSignPage
from dcentralab_qa_infra_automation.pages.namiPages.NamiSuccessfullyCreatedWalletPage import NamiSuccessfullyCreatedWalletPage
from dcentralab_qa_infra_automation.pages.namiPages.NamiWelcomePage import NamiWelcomePage
from dcentralab_qa_infra_automation.pages.namiPages.NamiSettingsPage import NamiSettingsPage

"""
Nami wallet actions
@Author: Efrat Cohen
@Date: 06.2023
"""
from dcentralab_qa_infra_automation.utils.WalletsActionsInterface import WalletsActionsInterface


class NamiActions(WalletsActionsInterface):
    """
    coinbase actions class
    this class implements wallet actions interface.
    """

    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)
        self.nami_wallet_base_page = NamiBasePage(self.driver)
        self.nami_welcome_page = NamiWelcomePage(self.driver)
        self.nami_import_seed_phrase_page = NamiImportSeedPhrasePage(self.driver)
        self.nami_sign_in_page = NamiSignPage(self.driver)
        self.nami_wallet_created_page= NamiSuccessfullyCreatedWalletPage(self.driver)
        self.nami_create_account_page = NamiCreateAccountPage(self.driver)
        self.nami_connect_wallet_page = NamiConnectWalletPage(self.driver)
        self.nami_settings_page = NamiSettingsPage(self.driver)


    def import_wallet(self):
        """
        import wallet process
        """
        # Open new tab
        self.driver.execute_script("window.open('');")

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Open chrome extension
        self.driver.get(pytest.properties.get("nami.connect.url"))


        # Check if Nami wallet welcome page loaded
        assert self.nami_welcome_page.is_page_loaded(), "Nami welcome page loaded"

        # Click on import button
        self.nami_welcome_page.click_on_import_wallet()

        # Check is import a wallet popup loaded
        assert self.nami_welcome_page.is_import_a_wallet_popup_loaded(), "import a wallet popup loaded"

        # Click on choose seed phrase length
        self.nami_welcome_page.click_on_choose_seed_phrase_length()

        # Choose word phrase (24)
        self.nami_welcome_page.choose_word_seed_phrase()

        # Click on accept terms button
        self.nami_welcome_page.click_on_accept_terms_button()

        # Click on continue button
        self.nami_welcome_page.click_on_continue_button()

        time.sleep(3)

        # Switch to the new window
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[2])


        # Check if import seed phrase page loaded
        assert self.nami_import_seed_phrase_page.is_page_loaded(), "import seed phrase page loaded"

        # Insert word seed phrase
        self.nami_import_seed_phrase_page.insert_word_seed_phrase()

        # Click on next button
        self.nami_import_seed_phrase_page.click_on_next_button()


        # Check if create account page loaded
        assert self.nami_create_account_page.is_page_loaded(), "create account page loaded"

        # Insert account name
        self.nami_create_account_page.insert_account_name()

        # Insert account password
        self.nami_create_account_page.insert_password()

        # Confirm password
        self.nami_create_account_page.insert_confirm_password()

        # Click on create account button
        self.nami_create_account_page.click_on_create_button()

        # Check if successfully created wallet page loaded
        assert self.nami_wallet_created_page.is_page_loaded(), "successfully create wallet page loaded"

        # Click on close button
        self.nami_wallet_created_page.click_on_close_button()

        # Focus on the second tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Close the tad
        self.driver.close()

        # Focus on the first tab window
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_network(self):
        """
        switch network process
        """
        # Open new tab
        self.driver.execute_script("window.open('');")

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Open chrome extension
        self.driver.get(pytest.properties.get("nami.connect.url"))

        namiBasePage = NamiBasePage(self.driver)

        # Check if Nami wallet welcome page loaded
        assert namiBasePage.is_page_loaded(), "Nami base page loaded"

        # Click on menu button
        namiBasePage.click_on_menu()

        # Choose settings menu option
        namiBasePage.click_on_setting()
        assert namiBasePage.is_on_settings_window(), "settings window loaded"

        # Click on network
        namiBasePage.click_on_network()
        assert namiBasePage.is_on_network_window(), "network window loaded"

        # Click on network select
        namiBasePage.click_on_network_select()

        # Choose network
        namiBasePage.choose_network()

        time.sleep(1)

        # Close the tad
        self.driver.close()

        # Focus on the first tab window
        self.driver.switch_to.window(self.driver.window_handles[0])

    def connect_wallet(self):
        """
        connect wallet implementation
        """
        time.sleep(3)

        # Nami popup instance
        w_handle = self.driver.window_handles[1]

        # Switch to pop up window
        self.driver.switch_to.window(w_handle)

        connectWalletPage = ConnectWalletPage(self.driver)
        # Check is connect to website popup loaded
        assert connectWalletPage.is_page_loaded(), "connect wallet window loaded"

        # Click on accept button
        connectWalletPage.click_on_accept_button()

        time.sleep(2)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def confirm(self):
        """
        confirm wallet process
        """
        time.sleep(8)

        # Nami popup instance
        w_handle = self.driver.window_handles[1]

        # Switch to pop up window
        self.driver.switch_to.window(w_handle)

        signPage = SignPage(self.driver)
        # Check is sign popup loaded
        assert signPage.is_page_loaded(), "Sign window loaded"

        # Click on sign button
        signPage.click_on_sign_button()

        # Check is confirm with password popup loaded
        signPage.is_confirm_with_password_popup_loaded()

        # Insert password
        signPage.insert_password()

        # Click on confirm button
        signPage.click_on_confirm_button()

        time.sleep(2)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])
