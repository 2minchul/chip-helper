import re
from collections import defaultdict
from http import cookiejar
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import UnableToSetCookieException, ElementClickInterceptedException

from selenium_helper import wait_element_by_name, wait_element_by_id
from .exceptions import BadStatusError


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

        upload_btn = None
        for _ in range(3):
            browser.get('https://studio.youtube.com/')

            upload_btn = wait_element_by_id(browser, 'upload-button', max_count=3)
            if not upload_btn:
                upload_btn = wait_element_by_id(browser, 'upload-icon', max_count=3)
            if upload_btn:
                upload_btn.click()
                break
        if not upload_btn:
            return False

        self.check_status(sleep=1)

        select_input = wait_element_by_name(browser, 'Filedata')
        select_input.send_keys(video_path)

        self.check_status(sleep=0.5)

        th = wait_element_by_id(browser, 'file-loader')
        th.send_keys(thumbnail_path)

        no_kids_btn = wait_element_by_name(browser, 'NOT_MADE_FOR_KIDS')
        no_kids_btn.click()

        next_btn = wait_element_by_id(browser, 'next-button')
        next_btn.click()

        while self.get_step() != 1:  # 두번째 단계
            self.check_status(sleep=1)

        next_btn = wait_element_by_id(browser, 'next-button')
        next_btn.click()

        unlisted_btn = wait_element_by_name(browser, 'UNLISTED')
        unlisted_btn.click()

        while self.get_step() != 2:  # 세번째 단계
            self.check_status(sleep=1)

        while 1:
            done_btn = wait_element_by_id(self.browser, 'done-button', 1)
            if not done_btn.is_enabled():
                break
            try:
                done_btn.click()
            except ElementClickInterceptedException:
                break
            self.check_status(sleep=1)

        is_finish = False
        while not is_finish:
            for element in self.browser.find_elements_by_class_name('ytcp-button'):
                if element.text == '닫기':
                    is_finish = True
                    break
            self.check_status(sleep=1)

        browser.implicitly_wait(2)
        return True

    def check_status(self, sleep=0.0):
        for element in self.browser.find_elements_by_class_name('error-short'):
            if element.text == '처리 중단됨':
                raise BadStatusError('처리 중단됨')

        if sleep:
            self.browser.implicitly_wait(sleep)

    def get_step(self):
        for element in self.browser.find_elements_by_class_name('step'):
            if element.get_attribute('state') == 'numbered':
                return int(element.get_attribute('step-index'))  # 0 or 1 or 2


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
