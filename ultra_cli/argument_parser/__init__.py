"""
Main part of the ultra_cli!

This package provides a command line argument handler.

Using `ArgumentParser` class you can parse the given options and flags of command line.
"""

from .parser import ArgumentParser, Option, DefaultConfig, Positional
