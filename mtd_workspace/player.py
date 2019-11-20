
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

# P1_keys_pressed = set()


MAX_SPEED = 6
JUMP_HEIGHT = 120
gravity_excel = 0.2
jump_excel = 0.4

excel = 0.4
inertia = 0.1

excel_stop = 0.1


class Player1(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("f_stand.png"))
        self.setScale(0.25)

        self.P1_keys_pressed = set()

        self.standing = False
        self.jumped = False
        self.excel_horizontal = 0
        self.excel_vertical = 0
        self.jump_frame = 90  # 90프레임동안 상승
        self.animate_num = 1

    def key_in(self):
        if self.x() >= -3:
            end_L = False
        else:
            end_L = True

        if self.x() <= 760:
            end_R = False
        else:
            end_R = True

        if end_L is True:
            self.setX(-2)
            self.excel_horizontal = 0
        if end_R is True:
            self.setX(759)
            self.excel_horizontal = 0

        if Qt.Key_Left in self.P1_keys_pressed and end_L is False:
            self.excel_horizontal -= excel

        if Qt.Key_Right in self.P1_keys_pressed and end_R is False:
            self.excel_horizontal += excel


    def gravity(self):
        if self.standing is False:
            self.excel_vertical += gravity_excel

    def ground_detect(self):
        if self.y() >= 520:
            self.excel_vertical = 0
            self.standing = True
        # if self.collidesWithItem():

    def jump_key_in(self):
        if (Qt.Key_Up in self.P1_keys_pressed) and (self.standing is True):
            self.standing = False
            self.jumped = True

    def jumping(self):
        if self.jumped is True:
            self.excel_vertical -= jump_excel
            self.jump_frame -= 1
        if self.jump_frame == 0:
            self.jump_frame = 90
            self.jumped = False

    def move_per_frame(self):
        if self.excel_horizontal >= MAX_SPEED:
            self.excel_horizontal = MAX_SPEED
        elif self.excel_horizontal <= -MAX_SPEED:
            self.excel_horizontal = -MAX_SPEED

        if self.standing is True:
            self.excel_vertical = 0

        self.setPos(self.x() + self.excel_horizontal, self.y() + self.excel_vertical)

    def inertia(self):
        if (Qt.Key_Left, Qt.Key_Right) not in self.P1_keys_pressed:
            if self.excel_horizontal < -2 * inertia:
                self.excel_horizontal += inertia
            elif self.excel_horizontal > 2 * inertia:
                self.excel_horizontal -= inertia

        if -0.3 <= self.excel_horizontal <= 0.3:
            self.excel_horizontal = 0
            self.setPixmap(QPixmap("f_stand.png"))

    def char_animate(self):

        if self.excel_horizontal < 0:
            self.setPixmap(QPixmap("f_left_{}.png".format(self.animate_num)))
            if self.animate_num > 5:
                self.animate_num = 1
            self.animate_num += 1

        if self.excel_horizontal > 0:
            self.setPixmap(QPixmap("f_right_{}.png".format(self.animate_num)))
            if self.animate_num > 5:
                self.animate_num = 1
            self.animate_num += 1

        if self.excel_horizontal == 0:
            self.animate_num = 1
            QPixmap("f_stand.png")

        if self.animate_num > 60:
            self.animate_num = 1