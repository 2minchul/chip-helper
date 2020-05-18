# chip-helper

- [Install](#Install)
- [How to use](#how-to-use)



## Install

1. python 설치  
    - https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe 설치파일을 다운받아 실행합니다.  
    - `Install Now` 를 선택하여 python 을 설치합니다.
2. 프로젝트 다운로드
    - 해당 프로젝트를 [다운로드](https://github.com/2minchul/chip-helper/archive/master.zip) 하여 적당한 위치에 압축을 풀어줍니다.
3. 실행환경 구성
    - `setup.cmd` 를 실행합니다.
    - 실행 후 `venv` 폴더가 생성되고 `finish!` 문구가 보이면 정상입니다.
4. 추가적인 파일
    - `DXGulimB-KSCpc-EUC-H.ttf` 를 `resource` 폴더 안에 넣어주세요
    - `chromedriver.exe` 를 아래 설명대로 다운받아 `resource` 폴더 안에 넣어주세요
        1. 사용중인 크롬에서 *설정* - *Chrome 정보* 에서 크롬 버전을 확인합니다.
        2. https://chromedriver.chromium.org/downloads 에서 사용중인 크롬 정보와 가장 비슷한 버전을 선택합니다.
        3. `chromedriver_win32.zip` 를 다운받은 후 압축을 풀어주세요.

## How to use

### 1-영상분류

영상 파일의 이름을 기준으로 숫자로 이루어진 하위 폴더를 생성 한 후 영상 파일을 이동시킵니다.

1. [input](https://github.com/2minchul/chip-helper/tree/master/input) 폴더 안에 숫자로 이루어진 이름의 1920 x 1080 영상파일들을 넣어주세요.
2. `1-영상분류.cmd` 실행

### 2-썸네일 생성기

영상 파일에서 자동으로 이미지를 캡처 한 후에 이미지를 합성하여 후면 전사 사진을 만듭니다.

1. `2-썸네일생성기.cmd` 실행
2. 각 폴더 안에 p`nnnn`.jpg 가 생성됩니다.

### 3-유튜브업로드

**썸네일 생성기** 에서 만들어진 썸네일과 영상파일들을 일괄적으로 유튜브에 업로드 합니다.

1. 크롬을 켜서 [cookiestxt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg) 플러그인을 설치하세요.
2. 유튜브에 접속 후 로그인 합니다.
3. 유튜브 창에서 cookiestxt 플러그인을 클릭하여 보이는 모든 text 를 복사 합니다.
4. 프로젝트 최상위 폴더 안에 `cookies.txt` 파일 생성 후 복사한 text 를 붙여넣습니다. (해당 text는 로그인 정보를 포함하고 있으므로 다른이에게 공유하면 안됩니다)
5. `3-유튜브업로드.cmd` 실행
6. 영상 파일은 *nnnn*.mp4 형식으로 이름이 변경되며 순차적으로 유튜브에 업로드됩니다.

### 4-유튜브url추출

유튜브에 업로드 된 영상의 url 을 가져와서 `youtube_url.txt` 를 생성합니다.

1. **3-유튜브업로드** 에서 업로드한 영상이 모두 정상적으로 게시될때까지 기다립니다.
2. `4-유튜브url추출.cmd` 실행
3. 각 폴더 하위에 해당 영상의 url 이 저장된 `youtube_url.txt` 가 생성됩니다.

### 5-qr코드생성기

유튜브 url을 네이버 QR코드 서비스에 등록 한 후 QR코드 이미지를 합성합니다.

1. 각 폴더에 **4-유튜브url추출** 에서 만들어진 `youtube_url.txt` 가 정상적으로 존재하는지 확인하세요.
2. `5-qr코드생성기.cmd` 실행
3. 네이버 로그인 페이지가 뜨면 로그인을 수동으로 진행합니다.
4. 각 `youtube_url.txt` 에 대해 네이버QR코드를 생성 후 자동으로 QR코드 이미지가 합성되어 *nnnn*.png 로 저장됩니다.
5. 생성된 `qrcode.html` 을 크롬으로 실행하면 해당 qr코드를 수정할 수 있는 페이지로 바로 이동 할 수 있습니다.