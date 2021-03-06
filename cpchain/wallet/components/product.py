from PyQt5.QtCore import Qt, QPoint, QObject, pyqtSlot, pyqtSignal, pyqtProperty, QUrl
from PyQt5.QtWidgets import (QScrollArea, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QGridLayout, QPushButton,
                             QMenu, QAction, QCheckBox, QVBoxLayout, QWidget, QDialog, QFrame, QTableWidgetItem,
                             QAbstractItemView, QMessageBox, QTextEdit, QHeaderView, QTableWidget, QRadioButton,
                             QFileDialog, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QCursor, QFont, QFontDatabase, QPainter, QColor, QPen, QPixmap
from PyQt5.QtQuickWidgets import QQuickWidget

from cpchain.crypto import ECCipher, RSACipher, Encoder

from cpchain.wallet.pages import load_stylesheet, HorizontalLine, wallet, main_wnd, get_pixm, qml_path

from twisted.internet.defer import inlineCallbacks
from twisted.internet.threads import deferToThread
from cpchain.wallet import fs
from cpchain.utils import open_file, sizeof_fmt

import importlib
import os
import os.path as osp
import string
import logging

from cpchain import config, root_dir
from cpchain.wallet.pages import app, Binder
from cpchain.wallet.components.picture import Picture
from cpchain.wallet.simpleqt.component import Component
from cpchain.wallet.simpleqt.decorator import component

from datetime import datetime as dt

from . import ProductObject, ImageObject


class ProductQML(Component):

    qml = qml_path('components/Product.qml')

    def __init__(self, parent, image=None, img_width=None, img_height=None, market_hash=None, show_status=False):
        self.obj = ImageObject(None, image, img_width,
                               img_height, market_hash=market_hash, show_status=show_status)
        super().__init__(parent)

    @component.create
    def create(self):
        pass

    @component.ui
    def ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        widget = QQuickWidget(self)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.rootContext().setContextProperty('self', self.obj)
        widget.setSource(QUrl(self.qml))
        layout.addWidget(widget)
        return layout


class Product(QWidget):

    def __init__(self, image=None, _id=None, name=None, icon=None, category='category',
                 cpc=0, sales=0, remain=0, description="", market_hash=None, h=135,
                 owner_address=None, ptype=None, show_status=False, created=None):
        self.image = image
        self.id = _id
        self.name = name
        self.category = category
        self.cpc = cpc
        self.sales = sales
        self.remain = remain
        self.icon = icon
        self.description = description
        self.h = h
        self.market_hash = market_hash
        self.show_status = show_status
        self.ptype = ptype
        self.created = created
        self.owner_address = owner_address

        super().__init__()
        self.initUI()

    def initUI(self):
        width = 220
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        height = 250
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)

        vbox_wrapper = QVBoxLayout()
        vbox_wrapper.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        vbox_wrapper.setContentsMargins(0, 0, 0, 0)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(10, 10, 10, 10)
        def listener():
            app.router.redirectTo('product_detail',
                                  image=self.image,
                                  product_id=self.id,
                                  name=self.name,
                                  icon=self.icon,
                                  cpc=self.cpc,
                                  ptype=self.ptype,
                                  created=self.created,
                                  category=self.category,
                                  description=self.description,
                                  market_hash=self.market_hash,
                                  owner_address=self.owner_address)

        image_url = wallet.market_client.url + \
            'product/v1/allproducts/images/?path=' + self.image

        image = ProductQML(None, image_url, width, int(
            self.h), market_hash=self.market_hash, show_status=self.show_status)
        image.obj.signals.click.connect(listener)
        vbox_wrapper.addWidget(image)
        vbox_wrapper.addLayout(vbox)
        vbox_wrapper.addStretch(1)

        # Name
        name = QLabel(self.name)
        name.setObjectName('name')
        name.setWordWrap(True)
        vbox.addWidget(name)

        # Category
        catbox = QHBoxLayout()
        if self.icon:
            icon = QLabel()
            icon.setMaximumWidth(20)
            icon.setMaximumHeight(20)
            icon.setObjectName('icon')
            icon.setPixmap(QPixmap(self.icon))
            catbox.addWidget(icon)
        category = QLabel(self.category)
        category.setObjectName('category')
        category.setAlignment(Qt.AlignCenter)
        category.setMaximumWidth(72)
        catbox.addWidget(category)
        catbox.addStretch(1)
        vbox.addLayout(catbox)

        # CPC and Sales
        hbox = QHBoxLayout()
        hbox.setObjectName('hbox1')

        cpc = QLabel(str(self.cpc))
        cpc.setObjectName('cpc')
        cpc_unit = QLabel('CPC')
        cpc_unit.setObjectName('cpc_unit')

        hbox.addWidget(cpc)
        hbox.addWidget(cpc_unit)

        hbox.addStretch(1)

        vbox.addLayout(hbox)

        # Timestamp and Remain Days
        tbox = QHBoxLayout()
        timestamp = QLabel(str(self.created))
        timestamp.setObjectName('timestamp')
        tbox.addWidget(timestamp)

        # add verticle-line
        vline = QLabel("|")
        vline.setObjectName('vline')
        tbox.addWidget(vline)

        sales = QLabel(str(self.sales) + ' sales')
        sales.setObjectName('sales')
        tbox.addWidget(sales)

        tbox.addStretch(1)
        vbox.addLayout(tbox)

        vbox.addStretch(1)

        tmp = QWidget()
        tmp.setLayout(vbox_wrapper)
        tmp.setContentsMargins(0, 0, 0, 0)
        tmp.setObjectName('main_product')
        layout = QVBoxLayout()
        layout.addWidget(tmp)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        load_stylesheet(self, "components/product.qss")
