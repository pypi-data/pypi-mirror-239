import pytest
from dcentralab_qa_infra_automation.drivers import BraveDriver, ChromeDriver
from dcentralab_qa_infra_automation.infra.CustomEventListener import CustomEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

"""
open site with extension via CRX. to any browser type.

@Author: Efrat Cohen
@Date: 12.2022
"""


def before_test(request):
    """
    get crx extension file, setup driver - open the site with extension.
    store the driver to use him in different fixtures and pages.
    if brave browser injected - add the option to driver initialization
    :param request: the requesting test context
    """
    pytest.logger.info("Test: " + request.node.nodeid + " is started ")
    # Init driver with extension based on injected driver type
    if pytest.data_driven.get("browser") == "brave":
        pytest.logger.info("brave browser type injected, initialize brave browser")
        driver = BraveDriver.initBraveDriverWithExtension()
    elif pytest.data_driven.get("browser") == "chrome":
        pytest.logger.info("chrome driver type injected, initialize chrome browser")
        driver = ChromeDriver.initChromeDriverWithExtension()

    # If no driver type injected - chrome is the default
    else:
        pytest.logger.info("no browser type injected, initialize default chrome browser")
        driver = ChromeDriver.initChromeDriverWithExtension()

    # Add event listener
    event_listener = CustomEventListener()
    event_firing_driver = EventFiringWebDriver(driver, event_listener)

    pytest.logger.info("driver :" + event_firing_driver.name + " had installed successfully")
    pytest.logger.info(
        f"driver window size: Width--> {driver.get_window_size().get('width')}  ::  Height --> "
        f"{driver.get_window_size().get('height')} ")

    # Set window as desktop
    driver.set_window_size(1728, 1117)
    pytest.logger.info(
        f"Driver window size: Width--> {driver.get_window_size().get('width')}  :: "
        f" Height --> {driver.get_window_size().get('height')} ")

    # Store driver in cls object
    request.cls.driver = driver
    pytest.driver = driver
