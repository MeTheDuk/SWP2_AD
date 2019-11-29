
import sys
import time
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame, QMainWindow)

'''
게임을 실행하는 주 파일이자 모든것을 불러오는 화면.

'''

import scene

WINDOW_WIDTH            = 800
WINDOW_HEIGHT           = 600


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = scene.Title()
        self.stage_0 = scene.Scene0()

        self.setWindowTitle("MainWindow")
        self.setStyleSheet("background:black;")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.view = QGraphicsView(QGraphicsScene(None), self)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.initWindow()
        self.show()

        self.timer = QBasicTimer()
        self.timer.start(16, self)

    def initWindow(self):
        self.view.setGeometry(0, 0, 800, 600)
        self.view.setScene(self.title)

    def timerEvent(self, event):
        self.changeScene()

    def changeScene(self):
        if self.title.cleared is True:
            self.view.setScene(self.stage_0)
            self.title.__del__()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindow()
    sys.exit(app.exec_())

