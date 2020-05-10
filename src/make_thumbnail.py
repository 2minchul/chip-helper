import os

from cmd_tool import get_execution_path, exit_enter
from img_tool import composite_thumbnail, get_image_size


def contains_name(text, files: list):
    return any(text in filename for filename in files)


def find_filename(text, files: list):
    for filename in files:
        if text in filename:
            return filename


if __name__ == '__main__':
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
