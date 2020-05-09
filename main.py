import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver

import qr_generator

default_headers = {
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'charset': 'utf-8'
}


def is_element_exists(br, element_id):
    try:
        br.find_element_by_id(element_id)
    except NoSuchElementException:
        return False
    return True


def wait_element(br, element_id):
    while not is_element_exists(br, element_id):
        br.implicitly_wait(0.5)
    return br.find_element_by_id(element_id)


def get_qr_code_pub(br: WebDriver) -> str:
    input_tag = wait_element(br, 'qrCodePub')
    return input_tag.get_attribute('value')


def send_qr(naver_id, qr_pub, cookies, qr_name, qr_link='http://%EC%9D%B4%EB%AF%BC%EC%B2%A0.com'):
    data = {"qrcdNo": "", "qrCodeUrl": "", "qrSaveStatusCd": "79", "qrColorBorderCd": "21", "qrDirectLinkTypeCd": "29",
            "qrSearchWord": "", "qrAttachOrder": "L|D|I|V|M|C", "qrSubjectFontTypeCd": "157", "qrLogoImgUrl": "",
            "qrLandingSkinTypeCd": "177", "qrAttachImgViewTypeCd": "164", "qrBorderSkinTypeCd": "237",
            "qrUserBorderSkinUrl": "", "qrCenterImgUrl": "", "qrLocation": "241", "qrUserBorderSkinThumbnailUrl": "",
            "qrCenterImgThumbnailUrl": "", "qrVersion": "30", "qrCodeExp": "10001", "qrName": qr_name,
            "qrLogoTypeCd": "24", "qrSubject": "", "qrLocationTypeCd": "241", "qrAttachLinkList[0].linkSubject": "",
            "qrAttachLinkList[0].linkUrl": "", "qrAttachLinkList[1].linkSubject": "", "qrAttachLinkList[1].linkUrl": "",
            "qrAttachLinkList[2].linkSubject": "", "qrAttachLinkList[2].linkUrl": "",
            "qrAttachLinkList[3].linkSubject": "", "qrAttachLinkList[3].linkUrl": "",
            "qrAttachLinkList[4].linkSubject": "", "qrAttachLinkList[4].linkUrl": "", "qrDesc": "",
            'qrNaverId': naver_id, 'qrDirectLink': qr_link, 'qrCodePub': qr_pub}

    headers = default_headers.copy()
    headers.update({'Referer': 'https://qr.naver.com/code/createForm.nhn', 'Origin': 'https://qr.naver.com'})

    response = requests.post('https://qr.naver.com/code/createCode.nhn', headers=headers, cookies=cookies, data=data)
    return response.json()


def get_naver_id(br, minime_frame):
    br.switch_to.frame(minime_frame)
    email_div = br.find_element_by_class_name('MY_EMAIL')
    email = email_div.text
    naver_id, *_ = email.split('@')
    br.switch_to.default_content()
    return naver_id


def create_qr(br, naver_id, qr_name, qr_link='http://%EC%9D%B4%EB%AF%BC%EC%B2%A0.com'):
    br.get('https://qr.naver.com/code/createForm.nhn')
    qr_code_pub = get_qr_code_pub(br)
    cookies = {cookie['name']: cookie['value'] for cookie in br.get_cookies()}
    return send_qr(naver_id, qr_code_pub, cookies, qr_name, qr_link)


def read_urls():
    with open('urls.txt') as f:
        for line in f:
            if line:
                yield line


if __name__ == '__main__':
    browser = webdriver.Chrome()

    browser.get("http://naver.com")
    browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
    print('waiting login ...')
    frame = wait_element(browser, 'minime')
    naver_id = get_naver_id(browser, frame)
    print('login success')

    for i, url in enumerate(read_urls()):
        name = f'{i + 1:04}'
        qr_url = create_qr(browser, naver_id, name).get('QRCodeData', {}).get('qrCodeUrl')
        if qr_url:
            qr_generator.generate(qr_url, f'qr/{name}.png')
            print(f'success {name}: {url}')
        else:
            print(f'failure {name}: {url}')

    browser.get('https://qr.naver.com/code/codeAdmin.nhn')
    print('모든 작업이 끝났습니다.')
    input()
    browser.close()
