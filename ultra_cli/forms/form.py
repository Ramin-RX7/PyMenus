"""
ultra-cli form module which contains `Form` class.
"""

from typing import Any

from .question import Question



class Form:
    """
    Form class is used to ask multiple questions and return the result of each of them in a dictionary.
    """
    def __init__(self, questions:list[Question]):
        """Form class constructor

        Args:
            questions (list[Question]): list of questions to be asked from user
        """
        self.questions = questions

    def display(self) -> dict[str,Any]:
        """This method is used to ask question one by one from user.

        Returns:
            dictionary: returns a dictionary of question names and (validated) user responses.
        """
        results = {}
        for question in self.questions:
            results[question.name] = question(results)
        return results
