
import sys
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

SCREEN_WIDTH            = 960
SCREEN_HEIGHT           = 720
FRAME_TIME_MS           = 16  # 16ms에 1번 = 960ms(0.96초)에 60번!


class Scene0(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)

        # 누르고 있는 키들 모음집.
        self.keys_pressed = set()

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("preview.png"))

        # QGraphicScene 안에 아이템을 추가. 지금과같은 경우 직사각형 아이템을 배경을 만들어서
        # 1포인트씩 더 바깥쪽까지 덮게 했음.
        self.addItem(bg)

        self.view = QGraphicsView(self)
        self.view.setWindowTitle("YEEEEEE")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.show()
        self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setSceneRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        self.game_update()
        self.update()

    def game_update(self):
        None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = Scene0()
    sys.exit(app.exec_())

