
import sys
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
    def __init__(self, parent=None, scene2show=None):
        super().__init__()

        self.stage_test = scene.Scene0()

        self.setWindowTitle("MainWindow")
        self.setStyleSheet("background:black;")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.initWindow()

    def initWindow(self):
        view = QGraphicsView(self.stage_test, self)
        view.setGeometry(0, 0, 800, 600)

        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show()
    #
    # def keyPressEvent(self, event):
    #     player.keys_pressed.add(event.key())
    #
    # def keyReleaseEvent(self, event):
    #     player.keys_pressed.remove(event.key())
    #
    # def timerEvent(self, event):
    #     self.game_update()
    #     self.update()
    #
    # def game_update(self):
    #     self.player1.move(player.keys_pressed)
    #     # self.player2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindow()
    sys.exit(app.exec_())

