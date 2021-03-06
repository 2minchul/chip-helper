import os
import sys
from contextlib import contextmanager


def exit_enter(code=0):
    input('press enter to exit...')
    sys.exit(code)


def get_execution_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def get_input_path_or_exit():
    path = os.path.join(get_execution_path(), 'input')
    if os.path.isdir(path):
        return path

    print('input 폴더를 찾을 수 없습니다')
    print(f'"{get_execution_path()}" 에 input 폴더를 생성해주세요')
    exit_enter(1)


def get_resource_path():
    return os.path.join(get_execution_path(), 'resource')


def get_chrome_driver_path_or_exit():
    chrome_driver_path = os.path.join(get_resource_path(), 'chromedriver.exe')
    if not os.path.isfile(chrome_driver_path):
        print('resource 폴더에 chromedriver 를 다운받아야 합니다')
        exit_enter(1)
    return chrome_driver_path


@contextmanager
def cd(path):
    origin = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)
