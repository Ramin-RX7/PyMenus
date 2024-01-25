import sys
from typing import Literal

from ultra_cli.argument_parser import ArgumentParser



class MyParser(ArgumentParser):
    name : str
    age : int = 18
    email : str|None
    disabled : bool
    subscriptions : list[int] = [1,2,3]   # also `set` and `tuple`
    provider : Literal["MTN","MCI"]
    # msg : Positional[str]

    class Config:
        name = "myapp"




print(sys.argv[1:])
print()
parser = MyParser()
args = parser.parse_arguments()
print()
print(args)
