#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Any instruments for customizing Models
"""


def get_name(column):
    if 'verbose_name' in column.info:
        return column.info['verbose_name']
    if column.name:
        return column.name
    return ''


def widget(fun):
    def wrapped(*args, **kwargs):
        sacrud_name = ''
        params = {}
        if 'column' in kwargs:
            if hasattr(kwargs['column'], 'property'):
                sacrud_name = kwargs['column'].property.key
            params.update({'column': kwargs['column']})
        if 'sacrud_name' in kwargs:
            sacrud_name = kwargs['sacrud_name']
        params.update({'sacrud_name': sacrud_name, 'name': sacrud_name})
        response = fun(*args, **kwargs)
        params.update(response)
        return params
    return wrapped


@widget
def widget_link(*args, **kwargs):
    return {'info': {'sacrud_position': 'inline',
                     'sacrud_list_template': 'sacrud/custom/WidgetLinkList.jinja2',
                     },
            'name': get_name(kwargs['column']),
            }


@widget
def widget_m2m(*args, **kwargs):
    return {'info': {'sacrud_template': 'sacrud/custom/WidgetM2MDetail.jinja2',
                     },
            }
