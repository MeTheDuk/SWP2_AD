

import time
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

import player
from map_objects import (SolidRect, f_door, w_door,
                         PoolFire, PoolWater, PoolPoison,
                         Slide_V, Button)

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

    def timerEvent(self, event):
        if len(self.keys_pressed) > 0:
            self.cleared = True
        # print(self.cleared)

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.keys_pressed.remove(event.key())
        except KeyError:
            pass


class Scene0(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)
        self.cleared = False
        self.gameover = False
        self.gameover_bg = QGraphicsPixmapItem(QPixmap("gameover.png"))
        self.gameover_bg.setScale(0.57)

        # 배경 사진 설정
        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_brick.png"))
        bg.setScale(0.25)
        self.addItem(bg)

        # 맵 조성
        self.terrain1 = SolidRect(0, 560, 800, 40)  # 제일 밑 땅.
        self.addItem(self.terrain1)

        # 맵 object 추가
        self.f_door = f_door()
        self.f_door.setPos(0, 496)
        self.addItem(self.f_door)

        self.w_door = w_door()
        self.w_door.setPos(750, 496)
        self.addItem(self.w_door)

        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(600, 0)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(200, 0)
        self.addItem(self.player2)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)
        self.player2.ground_detect(self.terrain1)

    def object_update(self):  # 맵에 있는 오브젝트들의 변화를 감지.
        self.f_door.open(self.player1)
        self.w_door.open(self.player2)
        self.stage_clear_detect()

    def stage_clear_detect(self):
        if self.f_door.opened and self.w_door.opened:
            self.cleared = True
        else:
            self.cleared = False

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()
        self.object_update()
        # print(self.cleared)

# 디버그용 출력들
        # print(self.cleared)
        # print(self.player1.jumped)  # 키 인식 체크용
        # print(self.player1.excel_vertical)
        # print(self.player1.standing)
        # print(self.player1.foot_y)
        # print(self.player1.y())
        # print(self.player1.collidingItems())

    def timerEvent(self, event):
        self.game_update()
        self.update()


class Scene1(QGraphicsScene):
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

        # 맵 조성
        self.terrain1 = SolidRect(0, 580, 800, 40)  # 제일 밑 땅.
        self.addItem(self.terrain1)

        self.terrain2 = SolidRect(60, 480, 120, 40)
        self.addItem(self.terrain2)

        self.terrain3 = SolidRect(620, 480, 120, 40)
        self.addItem(self.terrain3)

        self.terrain4 = SolidRect(120, 400, 560, 40)
        self.addItem(self.terrain4)

        # 맵 object 추가
        self.f_door = f_door()
        self.f_door.setPos(629, 400-64)
        self.addItem(self.f_door)

        self.w_door = w_door()
        self.w_door.setPos(121, 400-64)
        self.addItem(self.w_door)

        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(0, 500)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(750, 500)
        self.addItem(self.player2)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)
        self.player1.ground_detect(self.terrain2)
        self.player1.ground_detect(self.terrain3)
        self.player1.ground_detect(self.terrain4)

        self.player2.ground_detect(self.terrain1)
        self.player2.ground_detect(self.terrain2)
        self.player2.ground_detect(self.terrain3)
        self.player2.ground_detect(self.terrain4)

    def object_update(self):  # 맵에 있는 오브젝트들의 변화를 감지.
        self.f_door.open(self.player1)
        self.w_door.open(self.player2)
        self.stage_clear_detect()

    def stage_clear_detect(self):
        if self.f_door.opened and self.w_door.opened:
            self.cleared = True

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()
        self.object_update()

    def timerEvent(self, event):
        self.game_update()
        self.update()


class Scene2(QGraphicsScene):
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

        # 맵 조성
        self.terrain1 = SolidRect(0, 560, 800, 40)  # 제일 밑 땅.
        self.addItem(self.terrain1)
        self.pool1 = PoolWater(200, 559)
        self.addItem(self.pool1)
        self.pool2 = PoolFire(450, 559)
        self.addItem(self.pool2)
        self.terrain2 = SolidRect(200, 350, 300, 20)
        self.addItem(self.terrain2)
        self.terrain3 = SolidRect(275, 270, 150, 20)
        self.addItem(self.terrain3)
        self.terrain4 = SolidRect(0, 300, 150, 20)
        self.addItem(self.terrain4)
        self.pool3 = PoolPoison(275, 349)
        self.pool4 = PoolPoison(300, 349)
        self.addItem(self.pool3)
        self.addItem(self.pool4)
        self.terrain5 = SolidRect(600, 440, 100, 20)
        self.addItem(self.terrain5)

        # 맵 object 추가
        self.f_door = f_door()
        self.f_door.setPos(0, 300-64)
        self.addItem(self.f_door)

        self.w_door = w_door()
        self.w_door.setPos(60, 300-64)
        self.addItem(self.w_door)

        self.spawn()

    def spawn(self):
        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(100, 500)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(100-50, 500)
        self.addItem(self.player2)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)
        self.player1.ground_detect(self.terrain2)
        self.player1.ground_detect(self.terrain3)
        self.player1.ground_detect(self.terrain4)
        self.player1.ground_detect(self.terrain5)

        self.player2.ground_detect(self.terrain1)
        self.player2.ground_detect(self.terrain2)
        self.player2.ground_detect(self.terrain3)
        self.player2.ground_detect(self.terrain4)
        self.player2.ground_detect(self.terrain5)

    def object_update(self):  # 맵에 있는 w오브젝트들의 변화를 감지.
        self.f_door.open(self.player1)
        self.w_door.open(self.player2)
        self.pool1.kill_fire(self.player1)
        self.pool2.kill_water(self.player2)
        self.pool3.kill_all(self.player1, self.player2)
        self.pool4.kill_all(self.player1, self.player2)

        self.death()
        self.stage_clear_detect()

    def death(self):
        if self.player1.isVisible() & self.player2.isVisible() is False:
            self.player1.setVisible(False)
            self.player2.setVisible(False)
            time.sleep(1)
            self.spawn()

    def stage_clear_detect(self):
        if self.f_door.opened and self.w_door.opened:
            self.cleared = True

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()
        self.object_update()

    def timerEvent(self, event):
        self.game_update()
        self.update()


class Scene3(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)
        self.cleared = False
        self.gameover = False
        self.gameover_bg = QGraphicsPixmapItem(QPixmap("gameover.png"))
        self.gameover_bg.setScale(0.57)

        # 배경 사진 설정
        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_brick.png"))
        bg.setScale(0.25)
        self.addItem(bg)

        # 맵 조성
        self.terrain1 = SolidRect(0, 560, 800, 40)  # 제일 밑 땅.
        self.addItem(self.terrain1)
        self.terrain2 = SolidRect(0, 440, 500, 40)
        self.addItem(self.terrain2)

        # 맵 object 추가
        self.f_door = f_door()
        self.f_door.setPos(0, 440-64)
        self.addItem(self.f_door)

        self.w_door = w_door()
        self.w_door.setPos(60, 440-64)
        self.addItem(self.w_door)

        self.slide_v1 = Slide_V(440, 480, 60, 80)
        self.addItem(self.slide_v1)

        self.button_v1 = Button(Slide_V, 200, 550)
        self.addItem(self.button_v1)
        self.button_v2 = Button(Slide_V, 200, 430)
        self.addItem(self.button_v2)

        # 파이어보이 생성 및 좌표 지정
        self.player1 = player.Player1()
        self.player1.setPos(60, 500)
        self.addItem(self.player1)

        # 워터걸 생성 및 좌표 지정
        self.player2 = player.Player2()
        self.player2.setPos(120, 500)
        self.addItem(self.player2)

    def terrain_detect(self):  # 플레이어와 모든 지형의 접촉을 감지해줘야 함.
        self.player1.ground_detect(self.terrain1)
        self.player1.ground_detect(self.terrain2)

        self.player2.ground_detect(self.terrain1)
        self.player2.ground_detect(self.terrain2)

    def object_update(self):  # 맵에 있는 오브젝트들의 변화를 감지.
        self.f_door.open(self.player1)
        self.w_door.open(self.player2)

        self.slide_v1.collide(self.player1)
        self.slide_v1.collide(self.player2)

        self.button_v1.push_detect(self.player1, self.player2)
        self.button_v2.push_detect(self.player1, self.player2)

        self.slide_v1.slide(self.button_v1, self.button_v2)

        # print(self.slide_v1.y())
        # print(self.button_v1.pushed and self.button_v2.pushed)

        self.stage_clear_detect()

    def stage_clear_detect(self):
        if self.f_door.opened and self.w_door.opened:
            self.cleared = True
        else:
            self.cleared = False

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.terrain_detect()
        self.player1.player1_update()
        self.player2.player2_update()
        self.object_update()

    def timerEvent(self, event):
        self.game_update()
        self.update()


class End(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)

        # 60hz에 가까운 주기로 새로고침함(16ms에 1번 = 960ms(0.96초)에 16번)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        self.mainscene = True
        self.keys_pressed = set()
        self.cleared = False

        bg = QGraphicsPixmapItem()
        bg.setPixmap(QPixmap("bg_end.png"))
        bg.setScale(0.57)
        self.addItem(bg)

        self.player1 = player.Player1()
        self.player1.setPos(50, 0)
        self.addItem(self.player1)

        self.player2 = player.Player2()
        self.player2.setPos(700, 0)
        self.addItem(self.player2)

    def keyPressEvent(self, event):  # 키 입력 이벤트 핸들러
        self.player1.keys_pressed.add(event.key())
        self.player2.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):  # 키 입력 해제 이벤트 핸들러
        try:
            self.player1.keys_pressed.remove(event.key())
            self.player2.keys_pressed.remove(event.key())
        except KeyError:
            pass

    def game_update(self):
        self.player1.player1_update()
        self.player2.player2_update()

    def timerEvent(self, event):
        self.game_update()
        if self.player1.y() >= 600:
            self.player1.setY(0)
        if self.player2.y() >= 600:
            self.player2.setY(0)
        if self.player1.excel_vertical >= 6:
            self.player1.excel_vertical = 6
            self.player2.excel_vertical = 6
        self.update()

