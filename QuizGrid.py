# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import dirname, join, isfile, basename
from sys import argv, exit
from random import shuffle
import string
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from PySide2.QtGui import QImage, QPixmap, QFont, QIcon
from PySide2.QtCore import Qt, QSize, Signal


# Path to folder containing all images
IMG_PATH = "C:/Users/Pierre/Documents/QuizGrid/images_2021"
# Path to the check mark image
CHECK_PATH = "C:/Users/Pierre/Documents/QuizGrid/check.png"
# Path to the window icon
ICON_PATH = "C:/Users/Pierre/Documents/QuizGrid/coupe.jpg"
WIN_NAME = "Quizz 2021"  # Name of the windows

IMG_SIZE = 256  # Size in pixel for each image
N_COL = 8  # Number of images column for the layout


class MyQLabel(QLabel):
    """Label with clicked event and index property"""

    clicked = Signal()

    def __init__(self, index=None, parent=None):
        QLabel.__init__(self, parent)
        self.index = index
        self.name = None

    def mousePressEvent(self, ev):
        self.clicked.emit()


class QuizNA(QWidget):
    def __init__(self):
        """Initialize the widget according to the img folder"""

        # Init the widget
        QWidget.__init__(self)
        self.setWindowTitle(WIN_NAME)
        appIcon = QIcon(ICON_PATH)
        self.setWindowIcon(appIcon)

        # Get list of images
        self.img_list = listdir(IMG_PATH)
        shuffle(self.img_list)  #  Change the order every time

        # Create the layout
        self.gridLayout = QGridLayout()
        self.check_list = [False for img in self.img_list]

        # Create image grid
        for ii, img_name in enumerate(self.img_list):
            # Load and resize all images
            label = self.get_image(join(IMG_PATH, img_name))
            label.index = ii
            # Add to layout
            self.gridLayout.addWidget(label, ii // N_COL + 1, ii % N_COL + 1)
            # Add signal
            label.clicked.connect(self.change_check)

        # Add Column header
        for ii in range(N_COL):
            label = QLabel()
            label.setText(string.ascii_uppercase[ii])
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 32))
            label.setMaximumSize(QSize(IMG_SIZE, IMG_SIZE))
            self.gridLayout.addWidget(label, 0, ii + 1)

        # Add line header
        for ii in range(len(self.img_list) // N_COL):
            label = QLabel()
            label.setText(str(ii + 1))
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 32))
            label.setMaximumSize(QSize(IMG_SIZE, IMG_SIZE))
            self.gridLayout.addWidget(label, ii + 1, 0)

        # Set main layout
        self.setLayout(self.gridLayout)

    def get_image(self, img_path, size=IMG_SIZE):
        """Return a QLabel with the image at the proper size"""
        label = MyQLabel()
        img = QImage(img_path)
        pixmap = QPixmap(img)
        pixmap.scaled(size, size, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setMaximumSize(QSize(size, size))
        if img_path != CHECK_PATH:
            img_name = basename(img_path)
            label.setToolTip("Question n°" + img_name.split(".")[0])
        return label

    def change_check(self):
        """When clicking on a label change the icon"""
        index = self.sender().index
        # Get proper image to set
        if self.check_list[index]:  # Check to image
            label = self.get_image(join(IMG_PATH, self.img_list[index]))
            print("Cancel for " + self.img_list[index].split(".")[0])
        else:  # image to check
            label = self.get_image(CHECK_PATH)
            print("Done for " + self.img_list[index].split(".")[0])
            label.setToolTip("Question n° " + self.img_list[index].split(".")[0])
        label.clicked.connect(self.change_check)
        label.index = index

        # Update GUI
        self.sender().setParent(None)
        self.check_list[index] = not self.check_list[index]
        self.gridLayout.addWidget(label, index // N_COL + 1, index % N_COL + 1)


if __name__ == "__main__":
    # Create application
    a = QApplication(argv)

    w = QuizNA()
    print("Image name are set as tooltips")
    w.setStyleSheet("* { background-color : white;}")
    w.show()

    exit(a.exec_())
