
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

PLAYER_SPEED = 10

keys_pressed = set()


class Player1(QGraphicsPixmapItem):

    def __init__(self, parent = None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("f_left_1.png"))
        self.setScale(0.25)

    def move(self, keys_pressed):
        dx = 0
        dy = 0
        # if len(keys_pressed)==0:
        #     self.setPixmap(QPixmap("f_stand.png"))

        if Qt.Key_Left in keys_pressed:
            dx -= PLAYER_SPEED

        if Qt.Key_Right in keys_pressed:
            dx += PLAYER_SPEED

        if Qt.Key_Up in keys_pressed:
            dy -= PLAYER_SPEED

        if Qt.Key_Down in keys_pressed:
            dy += PLAYER_SPEED
        self.setPos(self.x()+dx, self.y()+dy)



