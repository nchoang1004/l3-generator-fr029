class Registry:
    def __init__(self):
        self.handlers = {}

    def get(self, key):
        def decorator(func):
            self.handlers[key] = func
            return func

        return decorator


registry = Registry()
