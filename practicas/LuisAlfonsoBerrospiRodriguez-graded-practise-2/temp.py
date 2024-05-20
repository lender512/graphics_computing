class function(function):
    def __init__(self, func):
        super().__init__(func.__code__, func.__globals__, func.__name__, func.__defaults__, func.__closure__)
        self._func = func

    def __getitem__(self, key):
        # Implement custom behavior for subscripting
        if key == 'info':
            return f"Function name: {self._func.__name__}, Argument count: {self._func.__code__.co_argcount}"
        else:
            raise KeyError(f"Unsupported key: {key}")