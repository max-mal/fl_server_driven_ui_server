from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import os
from pathlib import Path
import magic
import shlex

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
                        'type': 'text',
                        'text': path,
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
            "main": {   
                '$' : {
                    'files' : files_data,
                },
                'type': 'row',                       
                'children': [
                    {
                        'type': 'expanded',
                        'child': {
                            'type': 'list_builder',
                            'items': {
                                '_v': '$files',
                            },                            
                            'child': {
                                'type': 'inkwell',
                                '@click': {
                                    '_': 'sdr_request',
                                    'uri': {
                                        '_v': 'interpolate',
                                        'value': 'sdr://files.internal?path=$item.path',
                                    }
                                },
                                'child': {
                                    'type': 'container',
                                    'padding': 10,
                                    'margin': 10,
                                    'border': {
                                        'bottom': {
                                            'color': '#ffffff',
                                            'width': 1,
                                        }
                                    },
                                    'child': {
                                        'type': 'text',
                                        'text': {
                                            '_v': '$item.name',
                                        },
                                        'fontSize': 16,                    
                                    }
                                }
                            },
                        },
                        
                    },
                    {
                        'type': 'container',
                        'width': 1.0,
                        "height": 350.0,
                        'border': {
                            'all': {
                                'color': '#ffffff',
                                'width': 1,
                            }
                        },
                    },
                    {
                        'type': 'expanded',
                        'flex': 2,
                        'child': {
                            'type': 'padding',
                            'padding': 20,
                            'child': {
                                'type': 'scroll',
                                'key': 'scroll_file',
                                'child': {
                                    'type': 'sdr_area',
                                    'area_id': 'files.internal__file',
                                }
                            }
                        }
                    }
                ],                
            }
        },        
    }, safe=False)

