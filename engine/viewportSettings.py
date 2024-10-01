
from pygame import Vector2


class ViewportSettings:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.offset = Vector2(0,0)
        self.zoomlevel = 1
        