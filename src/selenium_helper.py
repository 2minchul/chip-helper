from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def is_element_exists_by(br, element_name, by):
    try:
        br.find_element(by, element_name)
    except NoSuchElementException:
        return False
    return True


def wait_element_by(br, element_name, by):
    while not is_element_exists_by(br, element_name, by):
        br.implicitly_wait(0.5)
    return br.find_element(by, element_name)


def wait_element_by_id(br, element_id):
    return wait_element_by(br, element_id, By.ID)


def wait_element_by_name(br, name):
    return wait_element_by(br, name, By.NAME)


def wait_element_by_tag(br, tag_name):
    return wait_element_by(br, tag_name, By.TAG_NAME)


def wait_element_by_xpath(br, xpath):
    return wait_element_by(br, xpath, By.XPATH)
