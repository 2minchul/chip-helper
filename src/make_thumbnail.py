import os

from cmd_tool import get_execution_path, exit_enter
from img_tool import composite_thumbnail


def contains_name(text, files: list):
    return any(text in filename for filename in files)


def find_filename(text, files: list):
    for filename in files:
        if text in filename:
            return filename


if __name__ == '__main__':
    input_path = os.path.join(get_execution_path(), 'input')

    for cur_dir, _, files in os.walk(input_path):
        jpg_filename = find_filename('.jpg', files)
        mp4_filename = find_filename('.mp4', files)

        if jpg_filename and mp4_filename:
            suffix, _ = os.path.splitext(mp4_filename)

            print('composite:', jpg_filename, '...')
            composite_thumbnail(os.path.join(cur_dir, jpg_filename), os.path.join(cur_dir, f'p{suffix}.jpg'))

    print('완료되었습니다!')
    exit_enter()
