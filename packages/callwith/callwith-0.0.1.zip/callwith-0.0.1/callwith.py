# -*- coding: utf-8 -*-
from __future__ import print_function


class CallWith:
    __slot__ = ('args', 'kwargs')

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        return func(*self.args, **self.kwargs)

    def __str__(self):
        items = []
        items.extend(map(repr, self.args))
        items.extend(map(lambda kv: '{}={!r}'.format(*kv), self.kwargs.items()))
        return ', '.join(items)
