# coding: utf-8

"""
    Python Pydantic Responses API

    A simple API based on python pydantic responses.

    The version of the OpenAPI document: 1.0.0
    Contact: support@example.com
    Created by: http://example.com/support
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal


class RequiredTestFetch400Response(TypedDict):
    pass

class OptionalTestFetch400Response(TypedDict, total=False):
    error: str

class TestFetch400Response(RequiredTestFetch400Response, OptionalTestFetch400Response):
    pass
