from ast import Not
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, QueryDict
from server import settings
from urllib.parse import urlparse, parse_qs
import requests
from .templates import apps_area_template, menu_template
from .use_cases import AppListUseCase
import subprocess
import asyncio

def menus(request):
    menu_items = settings.REGISTERED_MENUS
    items = []
    for menu_item in menu_items:
        items.append(menu_template(menu_item))

    return JsonResponse({
        'areas': {
            'menu': {
                'type': 'scroll',
                'direction': 'horizontal',
                'child': {
                    'type': 'padding',
                    'padding': 10,
                    'child': {
                        'type': 'row',
                        'children': items,
                    }
                },
            }
        }
    }, safe=False)

def on_request(request: HttpRequest):
    uri = request.GET.get('uri')
    parsed_uri = urlparse(uri)
    app_id = parsed_uri.hostname
    registered_app = None

    for app in settings.REGISTERED_APPS:
        if app['id'] == app_id:
            registered_app = app

    if registered_app is None:
        raise Exception(f"Failed to find app with id {app_id}")
    request_url = f"{registered_app['server_url']}{parsed_uri.path}?{parsed_uri.query}&{request.GET.urlencode()}"
    print(f"Requesting resource: {request_url}")
    response = requests.get(request_url)
    return JsonResponse(response.json(), safe=False)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

apps_use_case = AppListUseCase()
apps_use_case.apps = [] # apps_use_case.apps_list()

async def scan_images():
    print('Scanning images')
    apps_use_case.scan_images()
    print('Updating apps list')
    apps_use_case.apps = apps_use_case.apps_list()
    print('Apps list updated')

asyncio.run(scan_images())

def apps(request: HttpRequest):
    apps_list = apps_use_case.apps
    category_filter = request.GET.get('category', None)
    apps_filter = request.GET.get('filter', None)
    categories = []
    for item in apps_list:
        for category in item['categories']:
            if not category in categories:
                categories.append(category)

    sorted_categories = sorted(categories)

    if apps_filter is None:
        _apps_list = apps_list
    else:
        _apps_filter = apps_filter.lower()
        _apps_list = list(filter(lambda item: _apps_filter in str(item['name']).lower(), apps_list))

    if category_filter is None:
        apps_chunks = list(chunks(_apps_list, 4))
    else:
        filtered = list(filter(lambda item: category_filter in item['categories'], _apps_list))
        apps_chunks = list(chunks(filtered, 4))

    if apps_filter is not None:
        return JsonResponse({
            'actions': [
                {
                    "area": 'main',
                    "_": "set_variable",
                    'name': 'apps',
                    'value': apps_chunks,
                },
            ]
        }, safe=False)

    return JsonResponse(apps_area_template(apps_chunks, sorted_categories, apps_filter), safe=False)


def open(request: HttpRequest):
    path = request.GET.get('path', None)
    if path is None:
        return JsonResponse({})

    subprocess.Popen(['gio', 'launch', path])

    return JsonResponse({})


def network(request: HttpRequest):
    return JsonResponse({
        "areas": {
            "main": {
                '$': {
                    'apps': settings.REGISTERED_NETWORK_APPS,
                },
                'type': 'padding',
                'padding': 15,
                'child': {
                    'type': 'ui_area',
                    'child': {
                        'type': 'list_builder',
                        'items': {
                            '_v': '$apps',
                        },
                        'child': {
                            'type': 'padding',
                            'padding': 10,
                            'child': {
                                'type': 'inkwell',
                                '@click': {
                                    '_': 'sdr_request',
                                    'uri': {
                                        '_v': '$item.url',
                                    }
                                },
                                'child': {
                                    'type': 'ui_container',

                                    'child': {
                                        'type': 'text',
                                        'text': {
                                            '_v': '$item.name',
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }, safe=False)

def _webpage_response(child):
    return JsonResponse({
        "areas": {
            "main": {
                'type': 'padding',
                'padding': 15,
                'child': {
                    'type': 'ui_area',
                    'child': {
                       'type': 'scroll',
                       'child': child,
                    }
                }
            }
        }
    }, safe=False)

def webpage(request: HttpRequest):
    url = request.GET.get('location', None)
    if url is None:
        return _webpage_response({
            'type': 'text',
            'text': "Empty URL"
        })

    if url.startswith('https://www.youtube.com/watch') or url.startswith('https://youtube.com/watch'):
        url_parsed = urlparse(url)
        video_id = parse_qs(url_parsed.query)['v'][0]
        from youtube.views import video_preview
        request.GET = QueryDict('external=1&id=' + video_id)
        return video_preview(request)

    if url.startswith('https://youtu.be'):
        url_parsed = urlparse(url)
        video_id = url_parsed.path
        from youtube.views import video_preview
        request.GET = QueryDict('external=1&id=' + video_id)
        return video_preview(request)

    response = requests.get(url, stream=True)
    if response.status_code >= 400:
        response.close()
        return _webpage_response({
            'type': 'text',
            'text': f"Error: {response.status_code}. {response.reason}"
        })

    content_type = response.headers['content-type']
    if content_type.startswith('image/'):
        response.close()
        return _webpage_response({
            'type': 'image',
            'source': 'network',
            'value':  url,
        })

    if content_type.startswith('video/'):
        response.close()
        subprocess.Popen(['mpv', url])
        return _webpage_response({
            'type': 'text',
            'text': "Opening in mpv"
        })


    if not content_type.startswith('text/'):
        return _webpage_response({
            'type': 'text',
            'text': f"Unsupported entity: {content_type}"
        })


    return _webpage_response({
        'type': 'html',
        'html': response.text,
        'url': url,
        '@url': {
            '_': 'sdr_request',
            'uri': 'sdr://main/webpage',
            'location': {
                '_v': '$url',
            }
        }
    })

