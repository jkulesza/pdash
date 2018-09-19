
from .model import Model
from functools import wraps
from twisted.internet.defer import inlineCallbacks

class page:

    @staticmethod
    def data(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            data = func(*args, **kwargs)
            for key in data:
                setattr(self, key, Model(data[key]))
        return wrapper

    @staticmethod
    def ui(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            layout = func(*args, **kwargs)
            try:
                self.setLayout(layout)
            except Exception as e:
                print(e)
            return layout
        return wrapper

    @staticmethod
    def style(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            stylesheet = func(*args, **kwargs)
            self.setStyleSheet(stylesheet)
            return stylesheet
        return wrapper

    @staticmethod
    def create(func):
        @wraps(func)
        @inlineCallbacks
        def wrapper(*args, **kwargs):
            yield func(*args, **kwargs)
        return wrapper

    @staticmethod
    def method(func):
        @wraps(func)
        @inlineCallbacks
        def wrapper(*args, **kwargs):
            yield func(*args, **kwargs)
        return wrapper

class component:

    @staticmethod
    def data(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            data = func(*args, **kwargs)
            for key in data:
                setattr(self, key, Model(data[key]))
        return wrapper

    @staticmethod
    def ui(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            layout = func(*args, **kwargs)
            self.setLayout(layout)
            return layout
        return wrapper

    @staticmethod
    def style(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            stylesheet = func(*args, **kwargs)
            self.setStyleSheet(stylesheet)
            return stylesheet
        return wrapper

    @staticmethod
    def create(func):
        @wraps(func)
        @inlineCallbacks
        def wrapper(*args, **kwargs):
            yield func(*args, **kwargs)
        return wrapper

    @staticmethod
    def method(func):
        @wraps(func)
        @inlineCallbacks
        def wrapper(*args, **kwargs):
            yield func(*args, **kwargs)
        return wrapper
