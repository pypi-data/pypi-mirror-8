#!/usr/bin/env python
#
# Copyright (c) 2011-2013, Shopkick Inc.
# All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ---
# Author: John Egan <john@shopkick.com>

import functools
import inspect

import flawless.client


def wrap_function(func=None, error_threshold=None, reraise_exception=True):
    ''' Wraps a function with reporting to errors backend '''
    # This if/else allows wrap_function to behave like a normal decorator when
    # used like:
    #         @wrap_function
    #         def some_func():
    #
    # However, it also allows wrap_function to also be passed keyword arguments
    # like the following:
    #         @wrap_function(error_threshold=3, reraise_exception=False)
    #         def some_func():
    if func:
        return flawless.client._wrap_function_with_error_decorator(
            func=func, error_threshold=error_threshold, reraise_exception=reraise_exception)
    else:
        return functools.partial(flawless.client._wrap_function_with_error_decorator,
                                 error_threshold=error_threshold,
                                 reraise_exception=reraise_exception)


def wrap_class(cls, error_threshold=None):
    ''' Wraps a class with reporting to errors backend by decorating each function of the class.
            Decorators are injected under the classmethod decorator if they exist.
    '''
    for method_name, method in inspect.getmembers(cls, inspect.ismethod):
        wrapped_method = flawless.client._wrap_function_with_error_decorator(
            method if not method.im_self else method.im_func,
            save_current_stack_trace=False,
            error_threshold=error_threshold,
        )
        if method.im_self:
            wrapped_method = classmethod(wrapped_method)
        setattr(cls, method_name, wrapped_method)
    return cls
