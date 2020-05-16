import os
import sys


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
