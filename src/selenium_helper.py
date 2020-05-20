from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def is_element_exists_by(br, element_name, by):
    try:
        br.find_element(by, element_name)
    except NoSuchElementException:
        return False
    return True


def wait_element_by(br, element_name, by, interval=0.5, max_count=None):
    n = 0
    while not is_element_exists_by(br, element_name, by):
        n += 1
        br.implicitly_wait(interval)
        if max_count and max_count <= n:
            return None
    return br.find_element(by, element_name)


def wait_element_by_id(br, element_id, interval=0.5, max_count=None):
    return wait_element_by(br, element_id, By.ID, interval, max_count)


def wait_element_by_name(br, name, interval=0.5, max_count=None):
    return wait_element_by(br, name, By.NAME, interval, max_count)


def wait_element_by_tag(br, tag_name, interval=0.5, max_count=None):
    return wait_element_by(br, tag_name, By.TAG_NAME, interval, max_count)


def wait_element_by_xpath(br, xpath, interval=0.5, max_count=None):
    return wait_element_by(br, xpath, By.XPATH, interval, max_count)
