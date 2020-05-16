import argparse
import os
import re

import youtube_dl

from cmd_tool import get_execution_path, exit_enter, get_input_path_or_exit
from imagetools import get_image_size, composite_thumbnail
from youtube_uploader import YoutubeUploader


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
            target_filename = f'p{n:04}.jpg'
            print('composite:', jpg_filename, 'to', target_filename, '...')
            composite_thumbnail(os.path.join(cur_dir, jpg_filename), os.path.join(cur_dir, target_filename))

    print('완료되었습니다!')
    exit_enter()


def upload_videos():
    path = get_execution_path()
    chrome_driver_path = os.path.join(path, 'chromedriver.exe')
    input_path = get_input_path_or_exit()
    cookie_path = os.path.join(get_execution_path(), 'cookies.txt')

    if not os.path.isfile(chrome_driver_path):
        print('최상위 폴더에 chromedriver 를 다운받아야 합니다')
        exit_enter(1)

    if not os.path.isfile(cookie_path):
        print('최상위 폴더에 cookies.txt 를 작성해야 합니다')
        exit_enter(1)

    uploader = my_channel_id = None
    video_dirs = {}

    for cur_dir, _, files in os.walk(input_path):
        dir_name = os.path.basename(cur_dir)
        video_path = thumbnail_path = None

        for filename in files:
            if filename == 'youtube_url.txt':
                video_path = thumbnail_path = None
                print(f'already uploaded: {dir_name}')
                break

            name, ext = os.path.splitext(filename)
            if ext == '.mp4':
                video_path = os.path.join(cur_dir, filename)
                video_dirs[name] = cur_dir

            elif ext == '.jpg' and re.match(r'p\d+[.]jpg', filename):
                thumbnail_path = os.path.join(cur_dir, filename)

        if not (video_path and thumbnail_path):
            continue

        if not dir_name.isnumeric():
            print(f'skip: "{dir_name}" 는 숫자로 구성된 폴더이름이 아닙니다')
            continue

        if not uploader:
            uploader = YoutubeUploader()
            my_channel_id = uploader.init(chrome_driver_path, cookie_path)
            with open(os.path.join(path, '.mychannelid'), 'w') as f:
                f.write(my_channel_id)

        uploader.upload_video(video_path, thumbnail_path)

    print('모든 동영상이 업로드 되었습니다.')


def update_youtube_urls(my_channel_id=None):
    path = get_execution_path()
    input_path = get_input_path_or_exit()
    cookie_path = os.path.join(get_execution_path(), 'cookies.txt')

    if not my_channel_id:
        mychannelid_path = os.path.join(path, '.mychannelid')
        if os.path.isfile(mychannelid_path):
            with open(mychannelid_path, 'r') as f:
                my_channel_id = f.read()
        else:
            print('youtube upload 를 먼저 실행해주세요')
            exit_enter(1)

    yn = input('기존에 존재하는 youtube_url.txt 도 덮어쓰시겠습니까? [y/n]: ')
    if yn == 'y':
        overwrite = True
    else:
        overwrite = False

    video_dirs = {}
    for cur_dir, _, files in os.walk(input_path):
        if not overwrite and os.path.isfile(os.path.join(cur_dir, 'youtube_url.txt')):
            continue
        dir_name = os.path.basename(cur_dir)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.mp4' and dir_name.isnumeric():
                video_dirs[name] = cur_dir

    yt = youtube_dl.YoutubeDL(dict(cookiefile=cookie_path))

    my_channel_playlist = yt.extract_info(
        f'https://www.youtube.com/channel/{my_channel_id}', download=False, process=False
    ).get('url')

    for video in yt.extract_info(my_channel_playlist, download=False, process=False).get('entries'):
        title = video['title']
        if video_dirs.get(title):
            print(f'make youtube_url.txt: {title}')
            with open(os.path.join(video_dirs[title], 'youtube_url.txt'), 'w') as f:
                f.write(f"https://www.youtube.com/watch?v={video['id']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chip Helper')
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    subparsers.add_parser('makedirs', help='Create dirs like "nnnn" format in a specific path')
    subparsers.add_parser('thumbnail', help='Create thumbnails')
    subparsers.add_parser('upload', help='Upload videos to youtube')
    subparsers.add_parser('youtube-url', help='Make youtube_url.txt in input dirs')

    args = parser.parse_args()
    func = {
        'makedirs': make_dirs,
        'thumbnail': make_thumbnail,
        'upload': upload_videos,
        'youtube-url': update_youtube_urls,
    }.get(args.command)
    func()
