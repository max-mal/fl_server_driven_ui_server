from django.http import JsonResponse, HttpRequest

from youtube.templates import video_item_template, video_preview_template, videos_area
from .services import YoutubeService
from server import settings
import os
import shlex
import subprocess

service = YoutubeService()

def index(request: HttpRequest):
    search = request.GET.get('search', '')
    quality = request.GET.get('quality', 'best[height<=480]')
    subtitles = request.GET.get('subtitles', 'ru,en')
    videos = service.search(text=search),
    videos_data = []

    for item in videos[0]['items']:
        try:
            if isinstance(item['id'], str):
                id = item['id']
            else:
                if item['id']['kind'] == 'youtube#channel':
                    continue
                id = item['id']['videoId']
            videos_data.append({
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'shortDescription': item['snippet']['description'][:150] + "...",
                'id': id,
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
            })
        except Exception as e:
            print(e)

    return JsonResponse({
        "templates": {
            "yt_video": video_item_template(),
        },
        "areas": {
            'youtube.video': {
                'type': 'sized_box',
            },
            "main": videos_area(videos_data, search, quality, subtitles),
        },
    }, safe=False)

def video(request: HttpRequest):
    id = request.GET.get('id')
    quality = request.GET.get('quality', 'best')
    subtitles = request.GET.get('subtitles', '')

    proc = subprocess.Popen([f"{settings.BASE_DIR}/.venv/bin/youtube-dl", "-g", "-f", quality, id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()

    stdout = proc.stdout.read().decode()
    stderr = proc.stderr.read().decode()

    if proc.returncode != 0:
        return JsonResponse({
        'actions': [
            {
                '_': 'close_dialogs',
            },
            {
                '_': 'open_dialog',
                'child': {
                    'type': 'alert_dialog',
                    'title': {
                        'type': 'text',
                        'text': 'Error',
                    },
                    'child': {
                        'type': 'text',
                        'text': f'Failed to get video link: {stderr}',
                    }
                }
            },
        ],
    })

    video_url = stdout

    mpv_options = ["mpv", "--fs", "--force-window=immediate", "--demuxer-readahead-secs=120", "--cache-secs=120", "--demuxer-max-bytes=200M"]

    if len(subtitles)> 0:
        proc = subprocess.Popen([f"{settings.BASE_DIR}/.venv/bin/youtube-dl", "--write-sub", "--write-auto-sub", "--sub-lang", subtitles, "-o", f"/tmp/{id}", "--skip-download", id])
        proc.wait()

        for part in subtitles.split(','):
            mpv_options.append(f"--sub-file=/tmp/{id}.{part}.vtt")

    mpv_options.append(video_url)
    subprocess.Popen(mpv_options)

    return JsonResponse({
        'actions': [
            {
                '_': 'close_dialogs',
            }
        ],
    })

def video_preview(request: HttpRequest):
    id = request.GET.get('id')
    external = request.GET.get('external', None)
    video = service.get(id)

    area_id = "youtube.video"
    if external is not None:
        area_id = "main"

    return JsonResponse({
       'areas': {
           area_id: video_preview_template(video),
       }
    }, safe=False)
