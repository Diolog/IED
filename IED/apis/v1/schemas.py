# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import url_for

from IED.models.resources import Resource


# def user_schema(user):
#     return {
#         'id': user.id,
#         'self': url_for('.user', _external=True),
#         'kind': 'User',
#         'username': user.username,
#         'all_items_url': url_for('.items', _external=True),
#         'active_items_url': url_for('.active_items', _external=True),
#         'completed_items_url': url_for('.completed_items', _external=True),
#         'all_item_count': len(user.items),
#         'active_item_count': Item.query.with_parent(user).filter_by(done=False).count(),
#         'completed_item_count': Item.query.with_parent(user).filter_by(done=True).count(),
#     }


def item_schema(item):
    return {
        'id': item.id,
        'name': item.name,
        'size': round(item.size/1024/1024, 1)
    }


def items_schema(items, current, prev, next, pagination, class_id):
    return {
        'self': current,
        'items': [item_schema(item) for item in items],
        'prev': prev,
        'first': url_for('.items', page=1, class_id=class_id, _external=True),
        'last': url_for('.items', page=pagination.pages, class_id=class_id, _external=True),
        'next': next,
        'count': pagination.total
    }