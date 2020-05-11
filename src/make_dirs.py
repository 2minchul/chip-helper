import os

from cmd_tool import exit_enter,get_execution_path

if __name__ == '__main__':
    os.chdir(get_execution_path())
    print(os.path.abspath(os.curdir))
    print('폴더 생성기')
    print('존재하는 폴더는 건너뜀')
    path = input('생성할 경로: ')
    if not os.path.isdir(path):
        print('없는 경로입니다')
        exit_enter(1)

    s, e = map(int, (input('시작할 숫자: '), input('끝나는 숫자: ')))

    for i in range(s, e + 1):
        os.makedirs(os.path.join(path, f'{i:04}'), exist_ok=True)
    print('완료')
    exit_enter(0)
