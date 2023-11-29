from typing import Callable,Any



Validator = Callable[[str,str,Any],str]

class ValidationError(Exception):
    pass
