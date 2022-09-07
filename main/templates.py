def menu_template(menu_item: dict):
    return {
            'type': 'inkwell',
            '@click': {
                '_': 'sdr_request',
                'uri': menu_item['id'],
            },
            'child': {
                'type': 'padding',
                'padding': 5,
                'child': {
                    'type': 'ui_container',
                    'child': {
                        'type': 'text',
                        'text': str(menu_item['name']).upper(),
                        'fontSize': 20,
                    },
                }
            }
        }

def app_template(item: dict):
    return {
        'type': 'boolean',
        'value': item['item'],
        'true': {
            'type': 'padding',
            'padding': 20,
            'child': {
                'type': 'inkwell',
                '@click': {
                    '_': 'sdr_request',
                    'uri': 'sdr://main/open',
                    'path': item['path'],
                },
                'child': {
                'type': 'sized_box',
                'width': 80.0,
                'child': {
                        'type': 'column',
                        'crossAxisAlignment': 'center',
                        'children': [
                            {
                                'type': 'image',
                                'source': 'file',
                                'value': item['icon'],
                                'width': 60.0,
                                'height': 60.0,
                            },
                            {
                                'type': 'sized_box',
                                'height': 5.0,
                            },
                            {
                                'type': 'text',
                                'text': item['name'],
                                'textAlign': 'center',
                            }
                        ],
                }
                },
            }
        }
    }

def _apps_search_bar(filter):
    return {
        'type': 'ui_hcontainer',
        'child': {
            'type': 'container',
            'width': 380.0,
            'child': {
                'type': 'text_field',
                'hint': 'search apps',
                'value': filter,
                'autofocus': True,
                'max_lines': 1,
                '@changed': {
                    '_': 'sdr_request',
                    'uri': {
                        '_v': 'interpolate',
                        'value': 'sdr://main/apps?filter=$value',
                    }
                }
            }
        }
    }

def _apps_list(apps_chunks, sorted_categories):
    return {
        'type': 'expanded',
        'child': {
            'type': '$list_builder',
            'items': {
                '_v': '$$apps',
            },

            'child': {
                'type': 'row',
                'mainAxisAlignment': 'center',
                'children': [
                    app_template({
                        'path': {
                            '_v': '$item.0.path',
                        },
                        'item': {
                            '_v': '$item.0',
                        },
                        'name': {
                            '_v': '$item.0.name',
                        },
                        'icon': {
                            '_v': '$item.0.icon_path',
                        },
                    }),
                    app_template({
                        'path': {
                            '_v': '$item.1.path',
                        },
                        'item': {
                            '_v': '$item.1',
                        },
                        'name': {
                            '_v': '$item.1.name',
                        },
                        'icon': {
                            '_v': '$item.1.icon_path',
                        },
                    }),
                    app_template({
                        'path': {
                            '_v': '$item.2.path',
                        },
                        'item': {
                            '_v': '$item.2',
                        },
                        'name': {
                            '_v': '$item.2.name',
                        },
                        'icon': {
                            '_v': '$item.2.icon_path',
                        },
                    }),
                    app_template({
                        'path': {
                            '_v': '$item.3.path',
                        },
                        'item': {
                            '_v': '$item.3',
                        },
                        'name': {
                            '_v': '$item.3.name',
                        },
                        'icon': {
                            '_v': '$item.3.icon_path',
                        },
                    }),
                ],
            }
        }
    }

def _apps_categories():
    return {
        'type': 'padding',
        'padding': 15,
        'child': {
            'type': 'ui_hcontainer',
            'child': {
                'type': 'sized_box',
                'width': 120.0,
                'child': {
                    'type': 'list_builder',
                    'items': {
                        '_v': '$categories',
                    },
                    'child': {
                        'type': 'inkwell',
                        '@click': {
                            '_': 'sdr_request',
                            'uri': {
                                '_v': 'interpolate',
                                'value': 'sdr://main/apps?category=$item',
                            }
                        },
                        'child': {
                            'type': 'padding',
                            'padding': 10,
                            'child': {
                                'type': 'text',
                                'text': {
                                    '_v': '$item'
                                }
                            }
                        }
                    }
                },
            },
        }
    }

def apps_area_template(apps_chunks, sorted_categories, filter):
    if filter is None:
        filter = ''

    return {
        'areas': {
            'main': {
                '$$': {
                    "apps": apps_chunks,
                },
                '$': {
                    "categories": sorted_categories,
                },
                'type': 'row',
                'children': [
                    _apps_categories(),
                    {
                        'type': 'expanded',
                        'child': {
                            'type': 'padding',
                            'padding': 15,
                            'child': {
                                'type' : 'ui_area',
                                'child': {
                                    'type': 'center',
                                    'child': {
                                        'type': 'column',
                                        'crossAxisAlignment': 'center',
                                        'children': [
                                            _apps_search_bar(filter),
                                            _apps_list(apps_chunks, sorted_categories),
                                        ],
                                    }
                                }
                            },
                        }
                    },
                ],
            }
        }
    }