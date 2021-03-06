#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# harlib
# Copyright (c) 2014-2017, Andrew Robbins, All rights reserved.
#
# This library ("it") is free software; it is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; you can redistribute it and/or
# modify it under the terms of LGPLv3 <https://www.gnu.org/licenses/lgpl.html>.
from __future__ import absolute_import
from .objects import (
    HarObject, HarFile, HarLog, HarEntry,
    HarResponse, HarRequest)
import collections
import json
import six


def dump(o, writer):
    assert isinstance(o, HarObject)
    o.dump(writer)


def dumps(o):
    assert isinstance(o, HarObject)
    return o.dumps()


def dumpd(o):
    assert isinstance(o, HarObject)
    return o.to_json()


def loadd(d):
    assert isinstance(d, collections.Mapping)
    if 'log' in d:
        return HarFile(d)
    elif 'entries' in d:
        return HarLog(d)
    elif 'time' in d:
        return HarEntry(d)
    elif 'status' in d or 'statusText' in d or 'content' in d:
        return HarResponse(d)
    elif 'method' in d or 'url' in d or 'queryString' in d:
        return HarRequest(d)
    else:
        raise ValueError("unrecognized HAR content", d)


def loads(s):
    assert isinstance(s, six.string_types)
    d = json.loads(s)
    return loadd(d)


def load(reader):
    d = json.load(reader)
    return loadd(d)
