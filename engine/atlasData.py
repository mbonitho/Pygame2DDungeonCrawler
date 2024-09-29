from datetime import datetime

class AtlasData:

    def __init__(self, 
                 version: int, 
                 generated: datetime, 
                 resolution: tuple,
                 depth: int, 
                 width: int):
        self.version = version
        self.generated = generated
        self.resolution = resolution
        self.depth = depth
        self.width = width
        self.layers = {}