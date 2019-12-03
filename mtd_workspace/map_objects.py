from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap, QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

import player


class f_door(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("f_door_0.png"))
        self.setScale(0.2)
        self.opened = False

    def open(self, fire):
        if self.collidesWithItem(fire) is True:
            self.setPixmap(QPixmap("door_opened.png"))
            self.opened = True
        else:
            self.setPixmap(QPixmap("f_door_0.png"))
            self.opened = False


class w_door(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("w_door.png"))
        self.setScale(0.2)
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


class PoolFire(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("zone_fire.png"))

    def kill_water(self, water):
        if self.collidesWithItem(water) is True:
            water.setVisible(False)


class PoolWater(QGraphicsPixmapItem):
    def __init__(self, ax, ay):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("zone_water.png"))
        self.setPos(ax, ay)
        self.setScale(0.15)

    def kill_fire(self, fire):
        if self.collidesWithItem(fire) is True:
            fire.setVisible(False)



class Button(QGraphicsRectItem):
    def __init__(self, slide, ax, ay):
        QGraphicsRectItem.__init__(self)
        self.setRect(ax, ay, 30, 10)
        self.setBrush(slide.brush())

    def push(self, object, slide):
        if self.collidesWithItem(object) is True:
            slide.slide(object)


class Slide_V(QGraphicsRectItem):

    def __init__(self, ax, ay, w, h):
        QGraphicsRectItem.__init__(self)
        self.top = ay
        self.bottom = ay+h
        self.left = ax
        self.height = h
        self.width = w
        self.setRect(ax, ay, w, h)
        self.setBrush(QColor.fromRgb(180, 50, 230))

    def collide(self, player):
        if self.collidesWithItem(player) is True:
            if player.x() < self.x():
                player.setX(player.x()-1)
            elif player.x() > self.x():
                player.setX(player.x()+1)

    def slide(self, a_button, object):
        if a_button.collidesWithItem(object) is True:
            if self.top - 60 < self.y():
                self.setY(self.y()-0.4)
        else:
            if self.y() > self.top:
                self.setY(self.y()+0.4)


