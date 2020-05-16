import argparse
import os

from cmd_tool import get_execution_path, exit_enter
from imagetools import get_image_size, composite_thumbnail


def make_dirs():
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


def make_thumbnail():
    input_path = os.path.join(get_execution_path(), 'input')

    for cur_dir, _, files in os.walk(input_path):
        dir_name = os.path.basename(cur_dir)
        jpg_filename = None

        # set filenames
        for file_name in files:
            _, ext = os.path.splitext(file_name)
            if ext == '.jpg':
                jpg_path = os.path.join(cur_dir, file_name)
                if get_image_size(jpg_path) == (1920, 1080):
                    jpg_filename = file_name
                    break

        if jpg_filename:
            if not dir_name.isnumeric():
                print(f'skip: "{dir_name}" 는 숫자로 구성된 폴더이름이 아닙니다')
                continue

            n = int(dir_name)
            print('composite:', jpg_filename, '...')
            composite_thumbnail(os.path.join(cur_dir, jpg_filename), os.path.join(cur_dir, f'p{n:04}.jpg'))

    print('완료되었습니다!')
    exit_enter()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chip Helper')
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    make_dirs_parser = subparsers.add_parser('makedirs', help='Create folders like "nnnn" format in a specific path')
    thumbnail_parser = subparsers.add_parser('thumbnail', help='Create thumbnails')

    args = parser.parse_args()
    dict(makedirs=make_dirs, thumbnail=make_thumbnail).get(args.command)()
