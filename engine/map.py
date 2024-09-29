class Map:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.squares = []
        self.objects = []
        self.doors = []

    # def __init__(self, width: int, height: int, 
    #              squares: list[list[int]],
    #              objects: list[list[int]],
    #              doors: list[list[int]]):
    #     self.width = width
    #     self.height = height
    #     self.squares = squares
    #     self.objects = objects
    #     self.doors = doors