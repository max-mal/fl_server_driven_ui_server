from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from server import settings
from urllib.parse import urlparse
import requests

def menus(request):
    menu_items = settings.REGISTERED_MENUS
    items = []
    for menu_item in menu_items:
        items.append({
            'type': 'inkwell',
            '@click': {
                '_': 'sdr_request',
                'uri': menu_item['id'],
            },
            'child': {
                'type': 'padding',
                'padding': 5,
                'child': {
                    'type': 'container',
                    'padding': 20,                
                    'border': {
                        'all': {
                            'color': '#ffffff',
                            'width': 1,
                        }
                    },
                    'child': {
                        'type': 'text',
                        'text': menu_item['name'],
                        'fontSize': 20,
                    },
                }
            }
        })
    return JsonResponse({
        'areas': {
            'menu': {
                'type': 'scroll',
                'direction': 'horizontal',
                'child': {
                    'type': 'row',
                    'children': items,
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
    request_url = f"{app['server_url']}{parsed_uri.path}?{parsed_uri.query}"
    print(f"Requesting resource: {request_url}")
    response = requests.get(request_url)
    return JsonResponse(response.json(), safe=False)