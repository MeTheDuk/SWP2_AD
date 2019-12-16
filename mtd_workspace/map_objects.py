
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem


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
    def __init__(self, ax, ay):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("zone_fire.png"))
        self.setPos(ax, ay)
        self.setScale(0.15)

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


class PoolPoison(QGraphicsPixmapItem):
    def __init__(self, ax, ay):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap("zone_dead.png"))
        self.setPos(ax, ay)
        self.setScale(0.15)

    def kill_all(self, fire, water):
        if self.collidesWithItem(fire) is True:
            fire.setVisible(False)
        if self.collidesWithItem(water) is True:
            fire.setVisible(False)


class Button(QGraphicsRectItem):
    def __init__(self, slide, ax, ay):
        QGraphicsRectItem.__init__(self)
        self.setRect(ax, ay, 30, 10)
        self.setBrush(QColor.fromRgb(180, 50, 230))
        self.pushed = False
        self.slide = slide

    def push_detect(self, p1, p2):
        if self.collidesWithItem(p1) or self.collidesWithItem(p2) is True:
            self.pushed = True
            self.setVisible(False)
        else:
            self.pushed = False
            self.setVisible(True)


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
        self.on = False

    def collide(self, aplayer):
        if self.collidesWithItem(aplayer) is True:
            if aplayer.x() + aplayer.width >= self.sceneBoundingRect().x():
                aplayer.setX(aplayer.x()-2)
                aplayer.excel_horizontal = 0
            elif aplayer.x() <= self.sceneBoundingRect().x()+self.width:
                aplayer.setX(aplayer.x()+2)
                aplayer.excel_horizontal = 0

    def slide(self, a_button, b_button):
        if a_button.pushed or b_button.pushed is True:
            if self.sceneBoundingRect().top() - self.top < 80.8:
                self.setY(self.y()+0.8)

        else:
            if self.sceneBoundingRect().y() > self.top:
                self.setY(self.y()-0.8)




