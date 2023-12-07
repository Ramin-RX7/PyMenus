"""
This module contains the `Option` class which itself is a class to create end points in menus.
"""

from typing import Any,Callable

from pydantic import BaseModel



class Option(BaseModel):
    """
    Option object takes a `title` to be shown in the menus and when selected in a menu,
    it will call the given `function` with given `kwargs`
    """
    title:str
    function:Callable
    kwargs: dict[str,Any] = {}
