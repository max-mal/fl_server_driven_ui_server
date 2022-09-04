from django.http import JsonResponse, HttpRequest
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
            # print(item)

    return JsonResponse({
        "templates": {
            "yt_video": {
                'type': 'inkwell',
                '@click': [
                    {
                        '_': 'sdr_request',
                        'uri': {
                            '_v': 'interpolate',
                            'value': 'sdr://youtube.internal/video?id=$item.id&quality=$$quality&subtitles=$$subtitles',
                        }
                    },
                    {
                        '_': 'open_dialog',
                        'child': {
                            'type': 'alert_dialog',
                            'title': {
                                'type': 'text',
                                'text': 'Launching video',
                            },
                            'child': {
                                'type': 'text',
                                'text': 'Please wait, getting url and launching video in player',
                            }
                        }
                    },
                ],
                'child': {
                    'type': 'row',
                    'children': [
                        {
                            'type': 'image',
                            'source': 'network',
                            'value': {
                                '_v': '$item.thumbnail'
                            },
                            'width': 320.0,
                            'height': 180.0,
                        },
                        {
                            'type': 'sized_box',
                            'width': 10.0,
                        },
                        {
                            'type': 'expanded',
                            'child': {
                                'type': 'column',
                                'children': [
                                    {
                                        'type': 'sized_box',
                                        'height': 5.0,
                                    },
                                    {
                                        'type': 'text',
                                        'text': {
                                            '_v': '$item.title'
                                        }
                                    },
                                    {
                                        'type': 'sized_box',
                                        'height': 10.0,
                                    },
                                    {
                                        'type': 'text',
                                        'text': {
                                            '_v': '$item.shortDescription'
                                        }
                                    },
                                ],
                            }
                        }
                    ],
                },
            }
        },
        "areas": {
            "main": {
                '$' : {
                    'videos' : videos_data,
                    'onSearch': {
                        '_': 'sdr_request',
                        'uri': {
                            '_v': 'interpolate',
                            'value': 'sdr://youtube.internal/?search=$$search&quality=$$quality&subtitles=$$subtitles',
                        },
                    }
                },
                '$$': {
                    'search': search,
                    'quality': quality,
                    'subtitles': subtitles,
                },
                'type': 'column',
                'children': [
                    {
                        'type': 'container',
                        'border': {
                            'all': {
                                'color': '#ffffff',
                            },
                        },
                        'padding': 10,
                        'margin': 5,
                        'child': {
                            'type': 'row',
                            'crossAxisAlignment': 'center',
                            'children': [
                                {
                                    'type': 'expanded',
                                    'child': {
                                        'type': 'text_field',
                                        'hint': 'Search',
                                        '@changed': {
                                            '_': 'set_variable',
                                            'name': 'search',
                                            'value': {
                                                '_v': '$value',
                                            }
                                        },
                                        '@submit': {
                                            '_v': '$onSearch',
                                        },
                                        'max_lines': 1,
                                        'value': {
                                            '_v': '$$search',
                                        }
                                    },
                                },
                                {
                                    'type': 'text',
                                    'text': 'Quality:',
                                },
                                {
                                    'type': '$dropdown_button',
                                    'value': {
                                        '_v': '$$quality',
                                    },
                                    'options': {
                                        'best': 'Best',
                                        'best[height<=720]': '720p',
                                        'best[height<=480]': '480p',
                                        'best[height<=240]': '240p',
                                    },
                                    '@changed': {
                                        '_': 'set_variable',
                                        'name': 'quality',
                                        'value': {
                                            '_v': '$value',
                                        }
                                    }
                                },
                                {
                                    'type': 'sized_box',
                                    'width': 10.0,
                                },
                                {
                                    'type': 'text',
                                    'text': 'Subtitles:',
                                },
                                {
                                    'type': '$dropdown_button',
                                    'value': {
                                        '_v': '$$subtitles',
                                    },
                                    'options': {
                                        'ru,en': 'On',
                                        'en': 'English',
                                        'ru': 'Russian',
                                        '': 'Off',
                                    },
                                    '@changed': {
                                        '_': 'set_variable',
                                        'name': 'subtitles',
                                        'value': {
                                            '_v': '$value',
                                        }
                                    }
                                },
                                {
                                    'type': 'sized_box',
                                    'width': 10.0,
                                },
                                {
                                    'type': 'inkwell',
                                    '@click': {
                                       '_v': '$onSearch',
                                    },
                                    'child': {
                                        'type': 'icon',
                                        'icon': 'search',
                                    },
                                }
                            ],
                        }
                    },
                    {
                        'type': 'expanded',
                        'child': {
                            'type': 'list_builder',
                            'items': {
                                '_v': '$videos',
                            },
                            'child': {
                                'type': 'padding',
                                'padding': 10,
                                'child': {
                                    'type': 'yt_video',
                                },
                            },
                        }
                    }
                ],
            }
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