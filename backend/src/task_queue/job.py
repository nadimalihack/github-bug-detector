
class Job:
    def __init__(self, func):
        self.func = func
    def __call__(self):
        return self.func()
