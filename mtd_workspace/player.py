
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

from map_objects import SolidRect

MAX_SPEED = 4
gravity_excel = 0.2
JUMP_EXCEL_DEFAULT = -0.8
JUMP_HEIGHT = 17.6
excel = 0.6
inertia = 0.2

excel_stop = 0.1
same_chip_frame = 4


class Player1(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("f_stand.png"))
        self.setScale(0.25)

        self.keys_pressed = set()

        self.width = self.sceneBoundingRect().width()  # 50
        self.height = self.sceneBoundingRect().height()  # 57
        self.standing = False  # 땅에 서있는가 서있지 않는가
        self.jumped = False  # 점프를 했는가 안했는가

        self.foot_y = 0

        self.excel_horizontal = 0  # 수평 방향 가속도.
        self.excel_vertical = 0  # 수직 방향 가속도.
        self.jump_excel = JUMP_EXCEL_DEFAULT  # 점프력 설정. 전역 변수 JUMP_EXCEL_DEFAULT를 받아옴.
        self.animate_num = 0  # 캐릭터가 움직이는 것 처럼 보이게 하기위한 캐릭터 칩의 번호.
        self.last_chip_num = 5  # 한 캐릭터가 가진 캐릭터 칩의 마지막 번호(0~5번까지임)
        self.y_before_jump = 0  # 점프 전 y좌표 저장

    def key_in(self):  # 키 인식, 맵 양 옆 끝이면 더이상 못가게 함.
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

        if Qt.Key_Left in self.keys_pressed and end_L is False:
            self.excel_horizontal -= excel

        if Qt.Key_Right in self.keys_pressed and end_R is False:
            self.excel_horizontal += excel

        if Qt.Key_Up in self.keys_pressed:
            if self.standing is True:
                self.standing = False
                self.jumped = True
                self.setY(self.y()-10)
                self.y_before_jump = self.y()

    def gravity(self):  # 땅에 있는거 아니면 중력 가속도 받음
        if self.jumped is False:
            self.excel_vertical += gravity_excel

    def ground_detect(self, a_SolidRect):  # 땅인지 아닌지 감지. 땅이면 standing을 True로
        self.foot_y = self.y() + self.height  # 얘네는 화면 젤 왼쪽 위가 0,0이라 발 높이를 따로 해줘야 편함.

        if self.collidesWithItem(a_SolidRect) is True:
            if self.foot_y >= a_SolidRect.sceneBoundingRect().top():
                self.standing = True
                self.excel_vertical = 0

            # if self.foot_y >= a_SolidRect.top + (a_SolidRect.height/16):
            #     self.standing = True
            #     self.excel_vertical = 0

            if (self.jumped is True) and (self.y() <= a_SolidRect.bottom):
                self.jumped = False
                self.standing = False
                self.setY(a_SolidRect.bottom+3)

        elif self.collidesWithItem(a_SolidRect) is False:
            if len(set(self.collidingItems())) < 2:
                self.standing = False

    def jump(self):  # 점프 처리.
        if self.jumped is True:
            self.excel_vertical += self.jump_excel
        if self.y_before_jump-self.y() >= JUMP_HEIGHT:
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
        if (Qt.Key_Left, Qt.Key_Right) not in self.keys_pressed:
            if self.excel_horizontal < -1.5 * inertia:
                self.excel_horizontal += inertia
            elif self.excel_horizontal > 1.5 * inertia:
                self.excel_horizontal -= inertia

        if -0.3 <= self.excel_horizontal <= 0.3:
            self.excel_horizontal = 0
            self.setPixmap(QPixmap("f_stand.png"))

    def char_animate(self):
        if self.excel_horizontal < 0:
            self.setPixmap(QPixmap("f_left_{}.png".format(self.animate_num//same_chip_frame)))
            if self.animate_num == same_chip_frame*self.last_chip_num:
                self.animate_num = -1
            self.animate_num += 1

        if self.excel_horizontal > 0:
            self.setPixmap(QPixmap("f_right_{}.png".format(self.animate_num//same_chip_frame)))
            if self.animate_num == same_chip_frame*self.last_chip_num:
                self.animate_num = -1
            self.animate_num += 1

        if self.excel_horizontal == 0:
            self.animate_num = 1
            QPixmap("f_stand.png")

    def player1_update(self):
        self.char_animate()
        self.key_in()
        self.jump()
        self.gravity()
        self.move_per_frame()
        self.inertia()


class Player2(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.setPixmap(QPixmap("w_stand.png"))
        self.setScale(0.25)

        self.keys_pressed = set()

        self.width = self.sceneBoundingRect().width()  # 50
        self.height = self.sceneBoundingRect().height()  # 57
        self.standing = False  # 땅에 서있는가 서있지 않는가
        self.jumped = False  # 점프를 했는가 안했는가

        self.foot_y = 0

        self.excel_horizontal = 0  # 수평 방향 가속도.
        self.excel_vertical = 0  # 수직 방향 가속도.
        self.jump_excel = JUMP_EXCEL_DEFAULT  # 점프력 설정. 전역 변수 JUMP_EXCEL_DEFAULT를 받아옴.
        self.animate_num = 0  # 캐릭터가 움직이는 것 처럼 보이게 하기위한 캐릭터 칩의 번호.
        self.last_chip_num = 5  # 한 캐릭터가 가진 캐릭터 칩의 마지막 번호(0~5번까지임)
        self.y_before_jump = 0  # 점프 전 y좌표 저장

    def key_in(self):  # 키 인식, 맵 양 옆 끝이면 더이상 못가게 함.
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

        if Qt.Key_A in self.keys_pressed and end_L is False:
            self.excel_horizontal -= excel

        if Qt.Key_D in self.keys_pressed and end_R is False:
            self.excel_horizontal += excel

        if Qt.Key_W in self.keys_pressed:
            if self.standing is True:
                self.standing = False
                self.jumped = True
                self.setY(self.y()-10)
                self.y_before_jump = self.y()

    def gravity(self):  # 땅에 있는거 아니면 중력 가속도 받음
        if self.jumped is False:
            self.excel_vertical += gravity_excel

    def ground_detect(self, a_SolidRect):  # 땅인지 아닌지 감지. 땅이면 standing을 True로
        self.foot_y = self.y() + self.height  # 얘네는 화면 젤 왼쪽 위가 0,0이라 발 높이를 따로 해줘야 편함.

        if self.collidesWithItem(a_SolidRect) is True:
            if self.foot_y >= a_SolidRect.sceneBoundingRect().top():
                self.standing = True
                self.excel_vertical = 0

            # if self.foot_y >= a_SolidRect.top + (a_SolidRect.height/16):
            #     self.standing = True
            #     self.excel_vertical = 0

            if (self.jumped is True) and (self.sceneBoundingRect().y() <= a_SolidRect.bottom):
                self.jumped = False
                self.standing = False
                self.setY(a_SolidRect.bottom+3)

        elif self.collidesWithItem(a_SolidRect) is False:
            if len(set(self.collidingItems())) < 2:
                self.standing = False

    def jump(self):  # 점프 처리.
        if self.jumped is True:
            self.excel_vertical += self.jump_excel
        if self.y_before_jump-self.y() >= JUMP_HEIGHT:
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
        if (Qt.Key_Left, Qt.Key_Right) not in self.keys_pressed:
            if self.excel_horizontal < -1.5 * inertia:
                self.excel_horizontal += inertia
            elif self.excel_horizontal > 1.5 * inertia:
                self.excel_horizontal -= inertia

        if -0.3 <= self.excel_horizontal <= 0.3:
            self.excel_horizontal = 0
            self.setPixmap(QPixmap("w_stand.png"))

    def char_animate(self):
        if self.excel_horizontal < 0:
            self.setPixmap(QPixmap("w_left_{}.png".format(self.animate_num//same_chip_frame)))
            if self.animate_num == same_chip_frame*self.last_chip_num:
                self.animate_num = -1
            self.animate_num += 1

        if self.excel_horizontal > 0:
            self.setPixmap(QPixmap("w_right_{}.png".format(self.animate_num//same_chip_frame)))
            if self.animate_num == same_chip_frame*self.last_chip_num:
                self.animate_num = -1
            self.animate_num += 1

        if self.excel_horizontal == 0:
            self.animate_num = 1
            QPixmap("w_stand.png")

    def player2_update(self):
        self.char_animate()
        self.key_in()
        self.jump()
        self.gravity()
        self.move_per_frame()
        self.inertia()

