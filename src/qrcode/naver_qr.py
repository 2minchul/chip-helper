from typing import Optional

import requests
from selenium import webdriver

from selenium_helper import wait_element_by_id


class NaverQrCode:
    default_headers = {
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'charset': 'utf-8'
    }
    browser: Optional[webdriver.Chrome]
    my_naver_id: Optional[str]

    def init(self, chrome_diver_path='chromedriver'):
        self.browser = webdriver.Chrome(chrome_diver_path)
        self.browser.get("http://naver.com")

    def login(self):
        browser = self.browser
        browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        frame = wait_element_by_id(browser, 'minime')
        self.my_naver_id = self._get_naver_id(frame)

    def _get_naver_id(self, minime_frame):
        br = self.browser
        br.switch_to.frame(minime_frame)
        email_div = br.find_element_by_class_name('MY_EMAIL')
        email = email_div.text
        naver_id, *_ = email.split('@')
        br.switch_to.default_content()
        return naver_id

    def create_qr(self, qr_name, qr_link):
        br = self.browser
        br.get('https://qr.naver.com/code/createForm.nhn')
        input_tag = wait_element_by_id(br, 'qrCodePub')
        qr_code_pub = input_tag.get_attribute('value')  # qr 코드를 만들기 위한 1회용 token
        return self.send_create_qr_api(qr_code_pub, qr_name, qr_link)

    def send_create_qr_api(self, qr_pub, qr_name, qr_link):
        headers = self.default_headers.copy()
        headers.update({'Referer': 'https://qr.naver.com/code/createForm.nhn', 'Origin': 'https://qr.naver.com'})

        cookies = {cookie['name']: cookie['value'] for cookie in self.browser.get_cookies()}

        data = {
            "qrcdNo": "", "qrCodeUrl": "",
            "qrSaveStatusCd": "79", "qrColorBorderCd": "21", "qrDirectLinkTypeCd": "29",
            "qrSearchWord": "", "qrAttachOrder": "L|D|I|V|M|C", "qrSubjectFontTypeCd": "157", "qrLogoImgUrl": "",
            "qrLandingSkinTypeCd": "177", "qrAttachImgViewTypeCd": "164", "qrBorderSkinTypeCd": "237",
            "qrUserBorderSkinUrl": "", "qrCenterImgUrl": "", "qrLocation": "241",
            "qrUserBorderSkinThumbnailUrl": "", "qrCenterImgThumbnailUrl": "",
            "qrVersion": "30", "qrCodeExp": "10001", "qrName": qr_name,
            "qrLogoTypeCd": "24", "qrSubject": "", "qrLocationTypeCd": "241",
            "qrAttachLinkList[0].linkSubject": "", "qrAttachLinkList[0].linkUrl": "",
            "qrAttachLinkList[1].linkSubject": "", "qrAttachLinkList[1].linkUrl": "",
            "qrAttachLinkList[2].linkSubject": "", "qrAttachLinkList[2].linkUrl": "",
            "qrAttachLinkList[3].linkSubject": "", "qrAttachLinkList[3].linkUrl": "",
            "qrAttachLinkList[4].linkSubject": "", "qrAttachLinkList[4].linkUrl": "",
            "qrDesc": "", 'qrNaverId': self.my_naver_id, 'qrDirectLink': qr_link, 'qrCodePub': qr_pub
        }
        response = requests.post(
            'https://qr.naver.com/code/createCode.nhn',
            headers=headers, cookies=cookies, data=data
        )
        return response.json()

    def visit_admin_page(self):
        self.browser.get('https://qr.naver.com/code/codeAdmin.nhn')

    def close(self):
        self.browser.close()
        del self.browser
