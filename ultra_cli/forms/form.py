from .question import Question



class Form:
    def __init__(self, questions:list[Question]):
        self.questions = questions

    def display(self):
        results = {}
        for question in self.questions:
            results[question.name] = question(results)
        return results
