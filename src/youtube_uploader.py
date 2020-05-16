import re
from collections import defaultdict
from http import cookiejar
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import UnableToSetCookieException, NoSuchElementException, \
    ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.by import By

from selenium_helper import wait_element_by_name, wait_element_by_id, wait_element_by_xpath, is_element_exists_by


class YoutubeUploader:
    browser: Optional[webdriver.Chrome] = None

    def init(self, chrome_diver_path='chromedriver', cookie_file_path='cookies.txt'):
        self.browser = browser = webdriver.Chrome(chrome_diver_path)

        cj = cookiejar.MozillaCookieJar(cookie_file_path)
        cj.load()

        domains = defaultdict(list)

        for cookie in cj:
            domains[cookie.domain].append(cookie)

        merged_domains = defaultdict(list)

        for domain in sorted(domains.keys(), reverse=True):  # type: str
            if domain.startswith('.'):
                is_append = False
                for t in merged_domains.keys():
                    if domain in t:
                        merged_domains[domain].extend(domains[domain])
                        is_append = True
                        break
                if not is_append:
                    merged_domains[domain].extend(domains[domain])
            else:
                merged_domains[domain].extend(domains[domain])

        for domain, cookies in merged_domains.items():
            dummy_url = 'https://' + domain.lstrip('.').rstrip('/') + '/404dummy'
            browser.get(dummy_url)
            for cookie in cookies:
                cookie_dict = {'domain': cookie.domain, 'name': cookie.name, 'value': cookie.value,
                               'secure': cookie.secure}
                try:
                    browser.add_cookie(cookie_dict)
                except UnableToSetCookieException:
                    print('UnableToSetCookieException', cookie)
                    pass

        browser.get('http://youtube.com')
        rex = re.search(r'[{]"key":"creator_channel_id","value":"(.+?)"[}]', browser.page_source)
        if rex:
            return rex.group(1)

    def upload_video(self, video_path, thumbnail_path):
        browser = self.browser
        browser.get('https://studio.youtube.com/')

        upload_btn = wait_element_by_id(browser, 'upload-button')
        upload_btn.click()

        select_input = wait_element_by_name(browser, 'Filedata')
        select_input.send_keys(video_path)

        th = wait_element_by_id(browser, 'file-loader')
        th.send_keys(thumbnail_path)

        no_kids_btn = wait_element_by_name(browser, 'NOT_MADE_FOR_KIDS')
        no_kids_btn.click()

        next_btn = wait_element_by_id(browser, 'next-button')
        next_btn.click()

        wait_element_by_xpath(browser, '//a[@href="https://creatoracademy.youtube.com/page/lesson/cards"]')

        next_btn = wait_element_by_id(browser, 'next-button')
        next_btn.click()

        unlisted_btn = wait_element_by_name(browser, 'UNLISTED')
        unlisted_btn.click()

        while 1:
            try:
                if is_element_exists_by(browser, 'ytcp-video-thumbnail-with-info', By.TAG_NAME):
                    # print('humbnail-with-info exist')
                    break

                if is_element_exists_by(browser, 'done-button', By.ID):
                    # print('exist done-button')
                    done_btn = browser.find_element_by_id('done-button')
                    done_btn.click()
                else:
                    pass
                    # print('not exist done-button')

            except (ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException):
                pass

            browser.implicitly_wait(1)

        # print('break')
        browser.implicitly_wait(2)


if __name__ == '__main__':
    uploader = YoutubeUploader()
    uploader.init()
    uploader.upload_video(
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\1\0001.mp4',
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\1\p0001.jpg'
    )
    uploader.upload_video(
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\2\0002.mp4',
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\2\p0002.jpg'
    )
    uploader.upload_video(
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\3\0003.mp4',
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\3\p0003.jpg'
    )
    uploader.upload_video(
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\4\0004.mp4',
        r'C:\Users\drminchul\Downloads\결과 파일 복사본\결과 파일 복사본\4\p0004.jpg'
    )
    print('완료!')
