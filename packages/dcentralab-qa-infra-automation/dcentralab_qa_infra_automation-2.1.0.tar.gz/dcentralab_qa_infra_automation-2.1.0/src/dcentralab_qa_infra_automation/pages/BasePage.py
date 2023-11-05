from traceback import print_stack

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """
    The BasePage class holds all common functionality across the website.
    So, we can use those function in every page.

    @Author: Efrat Cohen
    @Date: 12.2022
    """

    def __init__(self, driver):
        """ BasePage constructor - This function is called every time a new object of the base class is created"""
        self.driver = driver
        self.timeout = pytest.properties.get("timeout")

    def get_element(self, element_name, by_locator):
        """
        Get element
        :param element_name: current element name
        :param by_locator: current locator
        :return: element when found, otherwise None
        """
        try:
            element = self.driver.find_element(by=by_locator[0], value=by_locator[1])
            pytest.logger.info(f"Element :: {element_name} :: found")
            return element
        except:
            pytest.logger.error(f"Could not found element :: {element_name} not found \n {print_stack()}")
            return False

    def get_elements(self, element_name, by_locator):
        """
        Get list of elements
        :param element_name: current element name
        :param by_locator: current locator
        :return: element when found, otherwise None
        """
        try:
            element = self.driver.find_elements(by=by_locator[0], value=by_locator[1])
            pytest.logger.info(f"List of elements :: {element_name} :: found")
            return element
        except:
            pytest.logger.error(f"Could not found list of elements :: {element_name} not found \n {print_stack()}")
            return False

    def is_element_exist(self, element_name, by_locator):
        """
        check if element exist
        @param: element_name - current element name
        @param: by_locator - current locator
        @return: true if on page, otherwise return false
        """
        try:
            pytest.logger.info("check if element: " + element_name + " is exist on the page")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator))
            pytest.logger.info("element: " + element_name + " exists")
            return True
        except:
            # If element not found
            pytest.logger.info("element " + element_name + " not found")
            return False

    def is_element_exist_with_custom_timeout(self, element_name, by_locator, timeout):
        """
        check if element exists
        @param: element_name - current element name
        @param: by_locator - current locator
        @return: true if on page, otherwise return false
        """
        try:
            pytest.logger.info("check if element: " + element_name + " is exists on the page")
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(by_locator))
            pytest.logger.info("element: " + element_name + " exists")
            return True
        except:
            # If element not found
            pytest.logger.info("element " + element_name + " not found")
            return False

    def is_specific_element_exist(self, element_name, by_locator, index):
        """
        check if specific element of a list exists
        @param: element_name - current element name
        @param: by_locator - current locator
        @param: index - list index to check
        @return: true if on page, otherwise return false
        """
        try:
            pytest.logger.info("check if element: " + element_name + "in index " + index + " is exists on the page")
            element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[
                index]
            pytest.logger.info("element: " + element_name + "in index " + index + " exists")
            if element:
                return True
        except:
            # If element not found
            pytest.logger.info("element " + element_name + "in index " + index + " not found")
            return False

    def click(self, element_name, by_locator):
        """
         Performs click on web element whose locator is passed to it
         :param element_name - current element name
         :param by_locator - current locator to click on
        """

        pytest.logger.info("clicking on " + element_name + " element")
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).click()

    def click_on_specific_item_in_list(self, element_name, by_locator, index):
        """
        Performs click on specific item in web element list whose locator is passed to it
        :param element_name - current element name
        :param by_locator - current locator
        :param index - index to click on
        """

        pytest.logger.info("clicking on " + element_name + " element")
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[index].click()

    def enter_text(self, element_name, by_locator, text):
        """
         Performs text entry of the passed in text, in a web element whose locator is passed to it
         :param element_name - current element name
         :param by_locator - current locator
         :param text - test to insert
        """

        pytest.logger.info("insert value: " + text + " into " + element_name + " element")
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).send_keys(
            text)

    def enter_text_on_specific_list_item(self, element_name, by_locator, index, text):
        """
         Performs text entry of the passed in text, in a web element whose locator is passed to it
         :param element_name - current element name
         :param by_locator - current locator
         :param index - current index
         :param text - test to insert
        """

        pytest.logger.info("insert value: " + text + " into " + element_name + " in index " + str(index) + " element")
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[
            index].send_keys(text)

    def upload_file(self, element_name, by_locator, file_path):
        """
        Performs choose file in input with type file, in a web element whose locator and file path are passed to it
        :param element_name - current element name
        :param by_locator - current locator to click on
        :param file_path:
        """
        pytest.logger.info("upload file: " + file_path + " into " + element_name + " element")
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).send_keys(
            file_path)

    def get_text_from_specific_index(self, element_name, by_locator, index):
        """
        Performs get text of web element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        :param index - current index
        :return current element text
        """
        pytest.logger.info("get the value from " + element_name + " element")
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[
            index].text

    def get_value_from_specific_index(self, element_name, by_locator, index):
        """
        Performs get value of web element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        :param index - current index
        :return current element value
        """
        pytest.logger.info("get the value from " + element_name + " element")

        element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[
            index]
        # Get the value attribute of the input element
        value = element.get_attribute("value")
        return value

    def get_text(self, element_name, by_locator):
        """
        Performs get text of web element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        :return current element text
        """
        pytest.logger.info("get the value from " + element_name + " element")
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).text

    def clear_text(self, element_name, by_locator):
        """
        Performs clear value of web element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        """
        pytest.logger.info("clear test from " + element_name + " element")
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).clear()

    def scroll_to_element(self, element_name, by_locator):
        """
        scroll the page to specific element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        """
        pytest.logger.info("scroll to : " + element_name + " element")
        element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def is_button_enable(self, element_name, by_locator):

        """
        Verify is button is enabled in order to click
        :param element_name:
        :param by_locator:
        :return: boolean
        """
        is_enable = False
        try:
            element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator))
            if element:
                if element.is_enabled():
                    is_enable = True
                else:
                    is_enable = False
            return is_enable

        except:
            pytest.logger.info(f"Element :: {element_name} with locator :: {by_locator} is not enable")
            return False

    def get_element_attribute_list(self, element_name, by_locator, attribute):
        """

        :param element_name: current element
        :param by_locator: current locator
        :param attribute: HTML attribute (class,id,...)
        :return:
        """
        try:
            element = self.get_element(element_name, by_locator)
            attribute_list = element.get_attribute(attribute)
            pytest.logger.info(
                f"Found List of attributes :: {attribute}: {attribute_list}, for element :: {element_name}")
            return attribute_list
        except:
            pytest.logger.error(f"Attribute :: {attribute} :: doesn't exist for element {element_name} ")
            return False
