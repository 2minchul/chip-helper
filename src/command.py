import argparse
import os
import re
import sys
from typing import Optional

import sentry_sdk
import youtube_dl

from cmd_tool import (
    get_execution_path,
    exit_enter,
    get_input_path_or_exit,
    get_chrome_driver_path_or_exit,
    get_resource_path,
    cd
)
from imagetools import Size
from qrcode import NaverQrCode, make_qr_image, make_redirect_html
from thumbnail import composite_thumbnail, capture_video
from youtube_uploader import YoutubeUploader

sentry_sdk.init("https://1ff694f9169a4fa383a867fe10ed9329@o342398.ingest.sentry.io/5243685")


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
    exit_enter()


def make_thumbnail():
    input_path = os.path.join(get_execution_path(), 'input')

    for cur_dir, _, files in os.walk(input_path):
        dir_name = os.path.basename(cur_dir)

        def _is_mp4(filename):
            _, ext = os.path.splitext(filename)
            return ext == '.mp4'

        mp4_files = tuple(filter(_is_mp4, files))

        if 1 < len(mp4_files):
            print(f'pass: "{dir_name}" 안에 한개 이상의 mp4 파일이 존재합니다')

        if not dir_name.isnumeric():
            print(f'skip: "{dir_name}" 는 숫자로 구성된 폴더이름이 아닙니다')
            continue

        idx_text = f'{int(dir_name):04}'
        mp4_filename = mp4_files[0]
        jpg_filename = f'{idx_text}.jpg'
        jpg_filepath = os.path.join(cur_dir, jpg_filename)

        print(f'capture:\t{mp4_filename} to {jpg_filename}')
        capture_video(os.path.join(cur_dir, mp4_filename), jpg_filepath)
        target_filename = f'p{idx_text}.jpg'
        print(f'composite:\t{jpg_filename} to {target_filename} ...')
        composite_thumbnail(jpg_filepath, os.path.join(cur_dir, target_filename))

    print('완료되었습니다!')
    exit_enter()


def upload_videos():
    path = get_execution_path()
    chrome_driver_path = get_chrome_driver_path_or_exit()
    input_path = get_input_path_or_exit()

    cookie_path = os.path.join(get_execution_path(), 'cookies.txt')
    if not os.path.isfile(cookie_path):
        print('최상위 폴더에 cookies.txt 를 작성해야 합니다')
        exit_enter(1)

    uploader = None
    video_dirs = {}

    for cur_dir, _, files in os.walk(input_path):
        dir_name = os.path.basename(cur_dir)
        video_path = video_name = thumbnail_path = None

        if 1 < len(tuple(filter(lambda s: s.endswith('.mp4'), files))):
            print(f'"{cur_dir}" 에 여러개의 .mp4 파일이 존재합니다!')
            continue

        for filename in files:
            if filename == 'youtube_url.txt':
                video_path = thumbnail_path = None
                print(f'already uploaded: {dir_name}')
                break

            current_video_name, ext = os.path.splitext(filename)
            if ext == '.mp4':
                if not dir_name.isnumeric():
                    print(f'skip: "{dir_name}" 는 숫자로 구성된 폴더이름이 아닙니다')
                    break

                video_name = f'{int(dir_name):04}'
                video_path = os.path.join(cur_dir, f'{video_name}.mp4')
                if current_video_name != video_name:
                    print(f'rename "{filename}" to "{video_name}.mp4"')
                    os.rename(os.path.join(cur_dir, filename), video_path)
                video_dirs[video_name] = cur_dir

            elif ext == '.jpg' and re.match(r'p\d+[.]jpg', filename):
                thumbnail_path = os.path.join(cur_dir, filename)

        if not (video_path and thumbnail_path):
            continue

        if not uploader:
            uploader = YoutubeUploader()
            my_channel_id = uploader.init(chrome_driver_path, cookie_path)
            with open(os.path.join(path, '.mychannelid'), 'w') as f:
                f.write(my_channel_id)

        print(f'uploading {video_name}')
        uploader.upload_video(video_path, thumbnail_path)

    print('모든 동영상이 업로드 되었습니다.')
    exit_enter()


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
    overwrite = yn == 'y'

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

    is_created = False
    for video in yt.extract_info(my_channel_playlist, download=False, process=False).get('entries'):
        title = video['title']
        if video_dirs.get(title):
            is_created = True
            print(f'make youtube_url.txt: {title}')
            with open(os.path.join(video_dirs[title], 'youtube_url.txt'), 'w') as f:
                f.write(f"https://www.youtube.com/watch?v={video['id']}")
    if not is_created:
        print('업로드 된 동영상이 없거나, 아직 업로드가 완전히 완료되지 않았습니다.')
        print('잠시 후 다시 시도해주세요.')
    exit_enter()


def qrcode():
    input_path = get_input_path_or_exit()
    chrome_driver_path = get_chrome_driver_path_or_exit()
    resource_path = get_resource_path()

    if not os.path.isfile(os.path.join(resource_path, 'DXGulimB-KSCpc-EUC-H.ttf')):
        print('폰트 파일을 찾을 수 없습니다.')
        print('DXGulimB-KSCpc-EUC-H.ttf 파일을 "font/" 안에 넣어주세요!')
        exit_enter(1)

    naver_qr: Optional[NaverQrCode] = None

    for cur_dir, _, files in os.walk(input_path):
        dir_name = os.path.basename(cur_dir)
        if not dir_name.isnumeric():
            continue
        if 'youtube_url.txt' not in files:
            continue
        if 'qrcode.html' in files:
            print(f'already created: {dir_name}')
            continue

        idx = int(dir_name)
        idx_text = f'{idx:04}'
        with open(os.path.join(cur_dir, 'youtube_url.txt'), 'r') as f:
            youtube_url = f.read()

        if not naver_qr:
            naver_qr = NaverQrCode()
            naver_qr.init(chrome_driver_path)
            print('waiting login ...')
            naver_qr.login()
            print('login success')

        qr_data = naver_qr.create_qr(idx_text, youtube_url).get('QRCodeData', {})
        qr_url = qr_data.get('qrCodeUrl')
        qr_id = qr_data.get('qrcdNo')

        if not qr_url:
            print(f'{idx_text}: QR CODE 생성에 실패했습니다')
            continue

        with cd(resource_path):
            print(f'creating "{idx_text}.png"')
            image = make_qr_image(Size(591, 738), qr_url, idx)  # 5cm x 6.25cm (300dpi)
            with open(os.path.join(cur_dir, f'{idx_text}.png'), 'wb') as f:
                image.save(f, format='PNG', dpi=(300, 300))
            make_redirect_html(
                os.path.join(cur_dir, 'qrcode.html'),
                f'https://qr.naver.com/code/updateForm.nhn?qrcdNo={qr_id}'
            )

    if naver_qr:
        naver_qr.visit_admin_page()

    print('모든 작업이 끝났습니다.')
    input('press enter to exit...')
    if naver_qr:
        naver_qr.close()
    sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chip Helper')
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    subparsers.add_parser('makedirs', help='Create dirs like "nnnn" format in a specific path')
    subparsers.add_parser('thumbnail', help='Create thumbnails')
    subparsers.add_parser('upload', help='Upload videos to youtube')
    subparsers.add_parser('youtube-url', help='Make youtube_url.txt in input dirs')
    subparsers.add_parser('qrcode', help='Generate Naver QR and composite qr image')

    args = parser.parse_args()
    func = {
        'makedirs': make_dirs,
        'thumbnail': make_thumbnail,
        'upload': upload_videos,
        'youtube-url': update_youtube_urls,
        'qrcode': qrcode,
    }.get(args.command)
    func()
    print('모든 작업이 완료되었습니다.')
    exit_enter()
