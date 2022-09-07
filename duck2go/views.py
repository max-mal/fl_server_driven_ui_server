from django.http import HttpRequest, JsonResponse
from duckduckgo_search import ddg, ddg_images

def index(request: HttpRequest):
    search = request.GET.get('search', '')

    results = []

    if len(search) > 0:
        results = ddg(search, region="ru")

    return JsonResponse({
        "areas": {
            "main": {
                "$": {
                    'results': results,
                },
                'type': 'padding',
                'padding': '15',
                'child': {
                    'type': 'column',
                    'crossAxisAlignment': 'center',
                    'children': [
                        {
                            'type': 'ui_hcontainer',
                            'child': {
                                'type': 'sized_box',
                                'width': 300.0,
                                'child': {
                                    'type': 'text_field',
                                    'hint': 'Search internet',
                                    'value': search,
                                    'autofocus': True,
                                    'max_lines': 1,
                                    '@submit': {
                                        '_': 'sdr_request',
                                        'uri': 'sdr://duck2go.internal',
                                        'search': {
                                            '_v': '$value',
                                        }
                                    }
                                }
                            }
                        },
                        {
                            'type': 'expanded',
                            'child': {
                                'type': 'list_builder',
                                'items': {
                                    '_v': '$results',
                                },
                                'child': {
                                    'type': 'padding',
                                    'padding': 10,
                                    'child': {
                                        'type': 'inkwell',
                                        '@click': {
                                            '_': 'sdr_request',
                                            'uri': 'sdr://main/webpage',
                                            'location': {
                                                '_v': '$item.href',
                                            }
                                        },
                                        'child': {
                                            'type': 'ui_area',
                                            'child': {
                                                'type': 'column',
                                                'children': [
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
                                                            '_v': '$item.body'
                                                        }
                                                    },
                                                ],
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    ],
                }
            }
        }
    }, safe=False)


def images(request: HttpRequest):
    search = request.GET.get('search', '')

    results = []

    if len(search) > 0:
        results = ddg_images(search, region="ru")

    return JsonResponse({
        "areas": {
            "main": {
                "$": {
                    'results': results,
                },
                'type': 'padding',
                'padding': '15',
                'child': {
                    'type': 'column',
                    'crossAxisAlignment': 'center',
                    'children': [
                        {
                            'type': 'ui_hcontainer',
                            'child': {
                                'type': 'sized_box',
                                'width': 300.0,
                                'child': {
                                    'type': 'text_field',
                                    'hint': 'Search images',
                                    'value': search,
                                    'autofocus': True,
                                    'max_lines': 1,
                                    '@submit': {
                                        '_': 'sdr_request',
                                        'uri': 'sdr://duck2go.internal/images',
                                        'search': {
                                            '_v': '$value',
                                        }
                                    }
                                }
                            }
                        },
                        {
                            'type': 'expanded',
                            'child': {
                                'type': 'list_builder',
                                'items': {
                                    '_v': '$results',
                                },
                                'child': {
                                    'type': 'padding',
                                    'padding': 10,
                                    'child': {
                                        'type': 'inkwell',
                                        '@click': {
                                            '_': 'sdr_request',
                                            'uri': 'sdr://main/webpage',
                                            'location': {
                                                '_v': '$item.url',
                                            }
                                        },
                                        'child': {
                                            'type': 'ui_area',
                                            'child': {
                                                'type': 'row',
                                                'children': [
                                                    {
                                                        'type': 'image',
                                                        'source': 'network',
                                                        'width': 200.0,
                                                        'value': {
                                                            '_v': '$item.thumbnail',
                                                        }
                                                    },
                                                    {
                                                        'type': 'sized_box',
                                                        'width': 10.0,
                                                    },
                                                    {
                                                        'type': 'column',
                                                        'children': [
                                                            {
                                                                'type': 'text',
                                                                'text': {
                                                                    '_v': '$item.title'
                                                                }
                                                            },
                                                        ],
                                                    }
                                                ],
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    ],
                }
            }
        }
    }, safe=False)