from typing import Iterable

from ..styles.out import print



def choice_input(prompt:str, acceptables:Iterable, error_msg:str="Invalid input"):
    while True:
        choice = input(prompt)
        if choice in acceptables:
            return choice
        print(error_msg, color="red")
