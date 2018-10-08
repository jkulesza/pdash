from PyQt5.QtWidgets import QLabel, QFrame
from functools import wraps
import sys
sys.path.append('.')

class Binder:
    
    @staticmethod
    def click(obj, listener):
        setattr(obj, 'mousePressEvent', listener)

def operate(func):
    @wraps(func)
    def wrapper(*args, **kw):
        self = args[0]
        func(*args, **kw)
        return self
    return wrapper

class Line(QFrame):
    def __init__(self, parent=None, wid=2, color="#ccc"):
        super().__init__(parent)
        self.parent = parent
        self.wid = wid
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(self.wid)
        self.setStyleSheet("QFrame{{ border-top: {}px solid {};}}".format(wid, color))

class Builder:

    def __init__(self, widget=QLabel, *args, **kw):
        self.widget = widget("", *args, **kw)

    @operate
    def model(self, model):
        self.widget.model = model
        model.setView(self.widget)

    @operate
    def text(self, text):
        self.widget.setText(str(text))
    
    @operate
    def align(self, align):
        self.widget.setAlignment(align)

    @operate
    def wrap(self, wrap):
        self.widget.setWordWrap(wrap)

    @operate
    def width(self, width):
        self.widget.setMinimumWidth(width)

    @operate
    def height(self, height):
        self.widget.setMinimumHeight(height)

    @operate
    def name(self, name):
        self.widget.setObjectName(name)

    @operate
    def click(self, callback):
        if isinstance(self.widget, QLabel):
            Binder.click(self.widget, callback)
            return
        self.widget.clicked.connect(callback)

    @operate
    def pixmap(self, pixmap):
        self.widget.setPixmap(pixmap)

    def build(self):
        return self.widget

from .button import Button
from .input import Input
from .checkbox import CheckBox

__all__ = [Builder, Button, Input, CheckBox]
