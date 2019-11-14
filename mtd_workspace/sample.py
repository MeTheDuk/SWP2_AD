#
# Simple start to a game in PyQt5
#   move with arrow keys, spacebar to fire bullets
# Used graphics from https://opengameart.org/content/space-shooter-redux
# (reduced by 50%)
# Got some hints from https://www.youtube.com/watch?v=8ntEQpg7gck series
# and http://zetcode.com/gui/pyqt5/tetris/
#
import sys
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QFrame)

SCREEN_WIDTH            = 800
SCREEN_HEIGHT           = 600
PLAYER_SPEED            = 15   # pix/frame
PLAYER_BULLET_X_OFFSETS = [0,90]
PLAYER_BULLET_Y         = 15
BULLET_SPEED            = 64  # pix/frame
BULLET_FRAMES           = 64
FRAME_TIME_MS           = 16  # ms/frame


class Player1(QGraphicsPixmapItem):
    def __init__(self, parent = None):
        QGraphicsPixmapItem.__init__(self,parent)
        self.setPixmap(QPixmap("playerShip1_blue.png"))

    def move(self, keys_pressed):
        dx = 0
        dy = 0
        if Qt.Key_Left in keys_pressed:
            dx -= PLAYER_SPEED
        if Qt.Key_Right in keys_pressed:
            dx += PLAYER_SPEED
        if Qt.Key_Up in keys_pressed:
            dy -= PLAYER_SPEED
        if Qt.Key_Down in keys_pressed:
            dy += PLAYER_SPEED
        self.setPos(self.x()+dx, self.y()+dy)


class Player2(QGraphicsPixmapItem):
    def __init__(self, parent = None, ):
        QGraphicsPixmapItem.__init__(self,parent)
        self.setPixmap(QPixmap("playerShip2_blue.png"))

    def move(self, keys_pressed):
        dx = 0
        dy = 0
        if Qt.Key_A in keys_pressed:
            dx -= PLAYER_SPEED
        if Qt.Key_D in keys_pressed:
            dx += PLAYER_SPEED
        if Qt.Key_W in keys_pressed:
            dy -= PLAYER_SPEED
        if Qt.Key_S in keys_pressed:
            dy += PLAYER_SPEED
        self.setPos(self.x()+dx, self.y()+dy)


class Scene1(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)

        # 누르고 있는 키들 모음집.
        self.keys_pressed = set()

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        bg = QGraphicsRectItem()
        # (좌상단 기준 좌표 x, y, 직사각형 너비, 직사각형 높이)
        bg.setRect(-1, -1, SCREEN_WIDTH+2, SCREEN_HEIGHT+2)
        bg.setBrush(QBrush(Qt.darkMagenta))  # 배경 색
        # QGraphicScene 안에 아이템을 추가. 지금과같은 경우 직사각형 아이템을 배경을 만들어서
        # 1포인트씩 더 바깥쪽까지 덮게 했음.
        self.addItem(bg)

        # Player 기체 생성. 화면에 불러온 것은 아님.
        self.player1 = Player1()
        # Player 위치 지정. 화면 가운데 배치하기 위한 수식들.
        self.player1.setPos((SCREEN_WIDTH-self.player1.pixmap().width())/2,
                           (SCREEN_HEIGHT-self.player1.pixmap().height())/2)

        # 화면에 Player 기체를 생성함.
        self.addItem(self.player1)

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
        self.player1.move(self.keys_pressed)


class Scene2(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)

        # 누르고 있는 키들 모음집.
        self.keys_pressed = set()

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        bg = QGraphicsRectItem()
        # (좌상단 기준 좌표 x, y, 직사각형 너비, 직사각형 높이)
        bg.setRect(-1, -1, SCREEN_WIDTH+2, SCREEN_HEIGHT+2)
        bg.setBrush(QBrush(Qt.darkMagenta))  # 배경 색
        # QGraphicScene 안에 아이템을 추가. 지금과같은 경우 직사각형 아이템을 배경을 만들어서
        # 1포인트씩 더 바깥쪽까지 덮게 했음.
        self.addItem(bg)

        # Player 기체 생성. 화면에 불러온 것은 아님.
        self.player1 = Player1()
        self.player2 = Player2()
        # Player 위치 지정. 화면 가운데 배치하기 위한 수식들.
        self.player1.setPos((SCREEN_WIDTH-self.player1.pixmap().width())/2,
                           (SCREEN_HEIGHT-self.player1.pixmap().height())/2)
        self.player2.setPos((SCREEN_WIDTH - self.player2.pixmap().width()) / 2,
                            (SCREEN_HEIGHT - self.player2.pixmap().height()) / 2)

        # 화면에 Player 기체를 생성함.
        self.addItem(self.player1)
        self.addItem(self.player2)

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
        self.player1.move(self.keys_pressed)
        self.player2.move(self.keys_pressed)


if __name__ == '__main__':
    # a = int(input("1인용, 2인용?"))
    # if a == 1:
    #     app = QApplication(sys.argv)
    #     scene = Scene1()
    #     sys.exit(app.exec_())
    # elif a == 2:
    #     app = QApplication(sys.argv)
    #     scene = Scene2()
    #     sys.exit(app.exec_())
    app = QApplication(sys.argv)
    scene = Scene2()
    sys.exit(app.exec_())

