import json


class BestScore:
    def __init__(self, best_score=0, history=None, start=None, goal=None):
        if goal is None:
            goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.best_score = best_score
        self.history = history
        self.start = start
        self.goal = goal

    # Source:
    # Visha. Make a Python Class JSON Serializable. PYnative
    # https://pynative.com/make-python-class-json-serializable/
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
