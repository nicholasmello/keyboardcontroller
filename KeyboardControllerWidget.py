#!/usr/bin/env python3
import math
import os
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QSlider, QAbstractSlider,
                               QSystemTrayIcon, QMenu)
from __feature__ import true_property

PATH = "/sys/devices/platform/tuxedo_keyboard"

class KeyboardControllerWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.red = 255
        self.green = 255
        self.blue = 255
        self.bright = 255

        self.redslider = QSlider(Qt.Horizontal)
        self.greenslider = QSlider(Qt.Horizontal)
        self.blueslider = QSlider(Qt.Horizontal)
        self.brightslider = QSlider(Qt.Horizontal)

        self.redlabel = QLabel("Red")
        self.greenlabel = QLabel("Green")
        self.bluelabel = QLabel("Blue")
        self.brightlabel = QLabel("Brightness")

        file = open("{}/brightness".format(PATH), "r")
        self.brightslider.value = self.descaleValue(int(file.read().strip()))
        file.close()

        file = open("{}/color_left".format(PATH), "r")
        filetxt = file.read().strip()
        file.close()
        self.redslider.value = self.descaleValue(int("0x{}".format(filetxt[0:2]), 16))
        self.greenslider.value = self.descaleValue(int("0x{}".format(filetxt[2:4]), 16))
        self.blueslider.value = self.descaleValue(int("0x{}".format(filetxt[4:6]), 16))

        self.redslider.valueChanged.connect(self.adjustRed)
        self.greenslider.valueChanged.connect(self.adjustGreen)
        self.blueslider.valueChanged.connect(self.adjustBlue)
        self.brightslider.valueChanged.connect(self.adjustBright)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.redslider)
        self.layout.addWidget(self.redlabel)
        self.layout.addWidget(self.greenslider)
        self.layout.addWidget(self.greenlabel)
        self.layout.addWidget(self.blueslider)
        self.layout.addWidget(self.bluelabel)
        self.layout.addWidget(self.brightslider)
        self.layout.addWidget(self.brightlabel)
    
    def scaleValue(self, val):
        return math.floor(val*255/99)

    def descaleValue(self, val):
        return math.floor(val*99/255)
    
    def updateColor(self):
        os.system("echo \"0x{:02x}{:02x}{:02x}\" > {}/color_left".format(self.red, self.green, self.blue, PATH))

    def adjustRed(self, i):
        self.red = self.scaleValue(i)
        self.updateColor()

    def adjustGreen(self, i):
        self.green = self.scaleValue(i)
        self.updateColor()

    def adjustBlue(self, i):
        self.blue = self.scaleValue(i)
        self.updateColor()

    def adjustBright(self, i):
        self.bright = self.scaleValue(i)
        os.system("echo \"0x{:02x}\" > {}/brightness".format(self.bright, PATH))

def test():
    print("test")

if __name__ == "__main__":
    app = QApplication([])
    app.quitOnLastWindowClosed = False
    widget = KeyboardControllerWidget()

    icon = QIcon("./input-keyboard-symbolic.svg")

    tray = QSystemTrayIcon()
    tray.icon = icon
    tray.isVisible = True
    tray.activated.connect(widget.show)

    menu = QMenu()
    action = QAction("Adjust Keyboard")
    action.triggered.connect(widget.show)
    menu.addAction(action)

    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    tray.setContextMenu(menu)
    tray.show()

    app.exec()
