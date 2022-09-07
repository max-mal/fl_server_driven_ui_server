import subprocess
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import os
from pathlib import Path
import magic
import shlex
from .templates import files_area

def _single_file_response(path, widget):
    if widget is None:
        widget = {
            'type': 'container'
        }

    return JsonResponse({
        "areas": {
            "files.internal__file": {
                'type': 'column',
                'children': [
                    {
                        'type': 'row',
                        'mainAxisAlignment': 'space_around',
                        'children': [
                            {
                                'type': 'expanded',
                                'child': {
                                    'type': 'text',
                                    'text': path,
                                }
                            },
                            {
                                'type': 'inkwell',
                                '@click': {
                                    '_': 'sdr_request',
                                    'uri': {
                                        '_v': 'interpolate',
                                        'value': 'sdr://files.internal/open?path=' + path,
                                    }
                                },
                                'child': {
                                    'type': 'text',
                                    'text': 'open',
                                }
                            }
                        ],
                    },
                    {
                        'type': 'divider',
                        'color': '#ffffff',
                    },
                    widget,
                ],
            }
        }
    }, safe=False)

def _single_file(path, object_path):

    mimetype = magic.from_file(object_path, mime=True)
    print(mimetype)
    if str(mimetype).startswith("image/") :
        return _single_file_response(path, {
            'type': 'image',
            'source': 'file',
            'value': object_path,
        })

    if str(mimetype).startswith("text/") :
        file = open(object_path, 'r')
        return _single_file_response(path, {
            'type': 'text',
            'text': {
                '_v': 'raw',
                'value': file.read(),
            },
        })

    if str(mimetype).startswith("video/") :
        os.system(f'mpv {shlex.quote(object_path)}')
        return _single_file_response(path, {
            'type': 'text',
            'text': 'Opening in mpv...',
        })

    if str(mimetype).startswith("audio/") :
        return _single_file_response(path, {
            'type': 'audio_player',
            'path': f'file://{object_path}'
        })

    os.system(f'xdg-open {shlex.quote(object_path)}')
    return _single_file_response(path, {
        'type': 'text',
        'text': 'Opening with xdg...',
    })

def index(request: HttpRequest):
    directory = Path.home()
    path = request.GET.get('path', '')
    path = os.path.normpath(path)
    object_path = str(directory) + "/" + path

    if os.path.isfile(object_path):
        return _single_file(path, object_path)

    if not os.path.isdir(object_path):
        return JsonResponse({
            "areas": {
                "files.internal__file": {
                    'type': 'text',
                    'text': 'Unsupported entity'
                }
            }
        }, safe=False)


    contents = os.listdir(object_path)
    contents.insert(0, '..')
    files_data = []

    for file in contents:
        if file.startswith('.') and file != '..':
            continue

        type = "other"
        if os.path.isdir(f"{directory}/{file}"):
            type = "dir"

        if os.path.isfile(f"{directory}/{file}"):
            type = "file"

        files_data.append({
            'name': file,
            'type': type,
            'path': f"{path}/{file}",
        })

    return JsonResponse({
        "areas": {
            "main": files_area(files_data, path),
        },
    }, safe=False)

def open_feh(request: HttpRequest):
    directory = Path.home()
    path = request.GET.get('path', '')
    path = os.path.normpath(path)

    object_path = str(directory) + "/" + path

    subprocess.Popen(['feh', object_path])

    return JsonResponse({})

def open_path(request: HttpRequest):
    directory = Path.home()
    path = request.GET.get('path', '')
    path = os.path.normpath(path)

    object_path = str(directory) + "/" + path

    subprocess.Popen(['xdg-open', object_path])

    return JsonResponse({})
