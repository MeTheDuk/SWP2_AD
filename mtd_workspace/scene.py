
import sys
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)
import player

SCREEN_WIDTH            = 800
SCREEN_HEIGHT           = 600
FRAME_TIME_MS           = 16  # 0.016s=16ms에 1번 = 960ms(0.96초)에 60번!


class Scene0(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        # 배경 사진 설정
        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_brick.png"))
        bg.setScale(0.25)
        self.addItem(bg)

        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(200, 200)  # 땅에 선것처럼 하려면 520임
        self.addItem(self.player1)

        self.view = QGraphicsView(self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.view.show() # scene 하나만 단일로 테스트 할때 활성화
        self.view.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setSceneRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # 맵 생성
        self.test = Solid()
        self.addItem(self.test)
        self.test.setPos(400, 400)

    def keyPressEvent(self, event):
        self.player1.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.player1.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        self.game_update()
        self.update()

    def game_update(self):
        self.player1.ground_detect()
        self.player1.char_animate()
        self.player1.key_in()
        self.player1.jump()
        self.player1.gravity()
        self.player1.move_per_frame()
        self.player1.inertia()
        # print(self.player1.jumped)  # 키 인식 체크용
        # print(self.player1.jump_excel)


class Solid(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("wall1.jpg"))
        self.setScale(0.02)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = Scene0()
    sys.exit(app.exec_())

