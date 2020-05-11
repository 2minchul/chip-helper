# chip-helper

*비개발자를 위한 상세한 설명입니다*

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

## How to use

### 폴더 생성기
특정 경로에 x번 부터 y번 까지 nnnn 형식의 폴더를 생성합니다.  
상대경로와 절대경로 모두 지원합니다.

1. `폴더생성기.cmd` 실행

Example Input.
```text
생성할 경로: input
시작할 숫자: 1
끝나는 숫자: 1000
```

### 썸네일 생성기
1. [input](https://github.com/2minchul/chip-helper/tree/master/input) 폴더 안에 썸네일로 쓰일 사진을 설명대로 위치시키세요.
2. `썸네일생성기.cmd` 실행