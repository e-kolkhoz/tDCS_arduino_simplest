#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PySide import QtCore, QtGui
from PIL import Image
import time

class TestWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        self.button = QtGui.QPushButton("Do test")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.button.clicked.connect(self.do_test)

    def do_test(self):
        img = Image.open('tDCS_bb.png')
        self.display_image(img)
        QtCore.QCoreApplication.processEvents()  # let Qt do his work


    def display_image(self, img):
        self.scene.clear()
        w, h = img.size
        self.imgQ = QtGui.QImage(img.tobytes('raw', 'RGBA'),  w, h, QtGui.QImage.Format_ARGB32)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.scene.update()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = TestWidget()
    widget.resize(640, 480)
    widget.show()

    sys.exit(app.exec_())