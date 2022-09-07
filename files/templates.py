
def file_item():
    return {
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
    }

def files_area(files_data, path):
    return {
        '$' : {
            'files' : files_data,
            'path': path,
        },
        'type': 'row',
        'children': [
            {
                'type': 'expanded',
                'child': {
                    'type': 'padding',
                    'padding': 15,
                    'child': {
                        'type': 'ui_hcontainer',
                        'child': {
                            'type': 'column',
                            'children': [
                                {
                                    'type': 'row',
                                    'mainAxisAlignment': 'end',
                                    'children': [
                                        {
                                            'type': 'inkwell',
                                            '@click': {
                                                '_': 'sdr_request',
                                                'uri': {
                                                    '_v': 'interpolate',
                                                    'value': 'sdr://files.internal/open?path=$path',
                                                }
                                            },
                                            'child': {
                                                'type': 'text',
                                                'text': 'fm',
                                            }
                                        },
                                        {
                                            'type': 'sized_box',
                                            'width': 5.0,
                                        },
                                        {
                                            'type': 'inkwell',
                                            '@click': {
                                                '_': 'sdr_request',
                                                'uri': {
                                                    '_v': 'interpolate',
                                                    'value': 'sdr://files.internal/feh?path=$path',
                                                }
                                            },
                                            'child': {
                                                'type': 'text',
                                                'text': 'feh',
                                            }
                                        }
                                    ],
                                },
                                {
                                    'type': 'expanded',
                                    'child': {
                                        'type': 'list_builder',
                                        'items': {
                                            '_v': '$files',
                                        },
                                        'child': file_item(),
                                    }
                                }
                            ],
                        }
                    }
                },

            },
            {
                'type': 'expanded',
                'flex': 2,
                'child': {
                    'type': 'padding',
                    'padding': 15,
                    'child': {
                        'type': 'ui_area',
                        'child': {
                            'type': 'column',
                            'children': [
                                {
                                    'type': 'expanded',
                                    'child': {
                                        'type': 'scroll',
                                        'key': 'scroll_file',
                                        'child': {
                                            'type': 'sdr_area',
                                            'area_id': 'files.internal__file',
                                        }
                                    }
                                }
                            ],
                        }
                    }
                }
            }
        ],
    }