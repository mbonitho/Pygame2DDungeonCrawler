
from pygame import Vector2


class ViewportSettings:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.offset = Vector2(0,0)
        self.zoomlevel = Vector2(1,1)
        