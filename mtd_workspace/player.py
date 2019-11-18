
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

keys_pressed = set()

PLAYER_SPEED = 10
JUMP_HEIGHT = 120
GRAVITY = 10

class Player1(QGraphicsPixmapItem):

    def __init__(self, parent = None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("f_left_1.png"))
        self.setScale(0.25)
        self.jumped = False
        self.standing = False
        self.lastjump_y = 0

    def move(self, keys_pressed):
        dx = 0
        dy = 0
        end_R = False
        end_L = False
        # if len(keys_pressed)==0:
        #     self.setPixmap(QPixmap("f_stand.png"))

        if self.x() <= -3:
            end_L = True
        else:
            end_L = False

        if self.x() >= 760:
            end_R = True
        else:
            end_R = False

        if Qt.Key_Left in keys_pressed and end_L is False:
            dx -= PLAYER_SPEED

        if Qt.Key_Right in keys_pressed and end_R is False:
            dx += PLAYER_SPEED

        self.setPos(self.x()+dx, self.y())

    def gravity_and_jump(self):
        if self.jumped is True and self.standing is False:
            self.setPos(self.x(), self.y() - GRAVITY)
        elif self.jumped is False and self.standing is False:
            self.setPos(self.x(), self.y() + GRAVITY)

        if self.lastjump_y - self.y() >= JUMP_HEIGHT:
            self.jumped = False

    def grounddetect(self):
        if self.y() >= 520:
            self.jumped = False
            self.standing = True
        # if self.collidesWithItem():

    def jump(self, keys_pressed):
        if (Qt.Key_Up in keys_pressed) and (self.jumped is False):
            self.jumped = True
            self.standing = False
            self.setPos(self.x(), self.y()-5)
            self.lastjump_y = self.y()

