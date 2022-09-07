def video_item_template():
    return {
        'type': 'inkwell',
        '@click': [
            {
                '_': 'sdr_request',
                'uri': {
                    '_v': 'interpolate',
                    'value': 'sdr://youtube.internal/video_preview?id=$item.id',
                }
            },
        ],
        'child': {
            'type': 'row',
            'children': [
                {
                    'type': 'ui_hcontainer',
                    'child': {
                        'type': 'image',
                        'source': 'network',
                        'value': {
                            '_v': '$item.thumbnail'
                        },
                        'width': 200.0,
                        # 'height': 180.0,
                    }
                },
                {
                    'type': 'sized_box',
                    'width': 10.0,
                },
                {
                    'type': 'expanded',
                    'child': {
                        'type': 'ui_area',
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
                }
            ],
        },
    }

def _video_search_bar():
    return {
        'type': 'ui_hcontainer',
        'margin': 5,
        'child': {
            'type': 'sized_box',
            'width': 600.0,
            'child': {
                'type': 'row',
                'crossAxisAlignment': 'center',
                'children': [
                    {
                        'type': 'expanded',
                        'child': {
                            'type': 'text_field',
                            'hint': 'Search',
                            'autofocus': True,
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
        }
    }

def _quality_dropdown():
    return {
        'type': 'row',
        'mainAxisAlignment': 'center',
        'crossAxisAlignment': 'center',
        'children': [
            {
                'type': 'text',
                'text': 'Quality:',
            },
            {
                'type': 'sized_box',
                'width': 10.0,
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
        ],
    }

def _subtitles_dropdown():
    return {
        'type': 'row',
        'mainAxisAlignment': 'center',
        'crossAxisAlignment': 'center',
        'children': [
            {
                'type': 'text',
                'text': 'Subtitles:',
            },
            {
                'type': 'sized_box',
                'width': 10.0,
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
        ],
    }

def video_preview_template(video):
    return {
        '$': {
            'video': video,
        },
        '$$': {
            'quality': 'best[height<=480]',
            'subtitles': 'ru,en',
        },
        'type': 'scroll',
        'child': {
            'type': 'ui_area',
            'child': {
                'type': 'container',
                'width': 400.0,
                'child': {
                    'type': 'column',
                    'children': [
                        {
                            'type': 'text',
                            'text': {
                                '_v': '$video.snippet.title'
                            },
                        },
                        {
                            'type': 'divider',
                        },
                        {
                            'type': 'sized_box',
                            'height': 5.0,
                        },
                        {
                            'type': 'row',
                            'mainAxisAlignment': 'center',
                            'crossAxisAlignment': 'center',
                            'children': [
                                {
                                    'type': 'inkwell',
                                    '@click': [
                                        {
                                            '_': 'sdr_request',
                                            'uri': {
                                                '_v': 'interpolate',
                                                'value': 'sdr://youtube.internal/video?id=$video.id&quality=$$quality&subtitles=$$subtitles',
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
                                                },
                                                'actions': [],
                                            }
                                        },
                                    ],
                                    'child': {
                                        'type': 'ui_container',
                                        'child': {
                                            'type': 'text',
                                            'text': 'Open in MPV',
                                        }
                                    }
                                },
                                {
                                    'type': 'sized_box',
                                    'width': 20.0,
                                },
                                {
                                    'type': 'column',
                                    'children': [
                                        _quality_dropdown(),
                                        _subtitles_dropdown(),
                                    ],
                                }
                            ],
                        },
                        {
                            'type': 'text',
                            'text': {
                                '_v': '$video.snippet.description'
                            },
                        },
                    ],
                }
            }
        }
    }

def videos_area(videos_data, search, quality, subtitles):
    return {
        '$' : {
            'videos' : videos_data,
            'onSearch': {
                '_': 'sdr_request',
                'uri': {
                    '_v': 'interpolate',
                    'value': 'sdr://youtube.internal/?search=$$search',
                },
            }
        },
        '$$': {
            'search': search,
        },
        'type': 'column',
        'children': [
            {
                'type': 'center',
                'child': _video_search_bar(),
            },
            {
                'type': 'expanded',
                'child': {
                    'type': 'padding',
                    'padding': 15,
                    'child': {
                        'type': 'ui_area',
                        'child': {
                            'type': 'row',
                            'children': [
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
                                },
                                {
                                    'type': 'sdr_area',
                                    'area_id': 'youtube.video',
                                }
                            ],
                        }
                    }
                }
            }
        ],
    }