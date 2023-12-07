"""
Ultra-CLI forms validation module.

Contains `Validator` and `ValidationError`
"""

from typing import Callable,Any



Validator = Callable[[str,str,Any],str]

class ValidationError(Exception):
    """This exception is used in Validators to inform that user answer is not acceptable"""
    pass
