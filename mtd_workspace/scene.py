
import sys
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

import player
from map_objects import SolidRect

SCREEN_WIDTH            = 800
SCREEN_HEIGHT           = 600
FRAME_TIME_MS           = 16  # 0.016s=16ms에 1번 = 960ms(0.96초)에 60번!


class Title(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        self.mainscene = True
        self.keys_pressed = set()
        self.cleared = False

        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("title.png"))
        bg.setScale(0.57)
        self.addItem(bg)
        start = QGraphicsPixmapItem(QPixmap("start.png"))
        start.setScale(0.5)

        self.addItem(start)
        start.setPos(127, 400)

    def __del__(self):
        print("del")

    def timerEvent(self, event):
        if len(self.keys_pressed) > 0:
            self.cleared = True
        print(self.cleared)

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        self.keys_pressed.remove(event.key())

        # # 그래픽 뷰 설정
        # self.view = QGraphicsView(self)
        # self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #
        # self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        # self.setSceneRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


class Scene0(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)
        self.cleared = False

        # 배경 사진 설정
        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_brick.png"))
        bg.setScale(0.25)
        self.addItem(bg)

        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(600, 200)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(200, 200)
        self.addItem(self.player2)

        # 맵 조성
        self.terrain1 = SolidRect(0, 550, 800, 40)  # 제일 밑 땅.

        # 맵 구성 요소를 scene에 추가
        self.addItem(self.terrain1)

        # 그래픽 뷰 설정
        # self.view = QGraphicsView(self)
        # self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #
        # self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        # self.setSceneRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)
        self.player2.ground_detect(self.terrain1)

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        self.player1.keys_pressed.remove(event.key())
        self.player2.keys_pressed.remove(event.key())

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()

        # print(self.player1.jumped)  # 키 인식 체크용
        # print(self.player1.excel_vertical)
        # print(self.player1.standing)
        # print(self.player1.foot_y)
        # print(self.player1.y())
        # print(self.player1.collidingItems())

    def timerEvent(self, event):
        self.game_update()
        self.update()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = Scene0()
    sys.exit(app.exec_())

