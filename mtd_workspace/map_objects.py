from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap, QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

import player


class f_door(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("f_door.jpg"))
        self.opened = False

    def open(self, fire):
        if self.collidesWithItem(fire) is True:
            self.setPixmap(QPixmap("door_opened.png"))
            self.opened = True
        else:
            self.setPixmap(QPixmap("f_door.png"))
            self.opened = False


class w_door(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("w_door.jpg"))
        self.opened = False

    def open(self, water):
        if self.collidesWithItem(water) is True:
            self.setPixmap(QPixmap("door_opened.png"))
            self.opened = True
        else:
            self.setPixmap(QPixmap("w_door.png"))
            self.opened = False





class SolidRect(QGraphicsRectItem):

    def __init__(self, ax, ay, w, h):
        QGraphicsRectItem.__init__(self)
        self.top = ay
        self.bottom = ay+h
        self.left = ax
        self.height = h
        self.width = w
        self.setRect(ax, ay, w, h)
        self.setBrush(QColor.fromRgb(99, 66, 33))

    # def playerDetect(self, a_player):
    #     if self.collidesWithItem(a_player):
    #         # if a_player.y()+a_player.height > self.y():
    #         #     a_player.standing = True
    #         if a_player.y() < self.y()+self.height:
    #             a_player.jumped = False
    #             a_player.
    #             a_player.setY(a_player.y+5)


