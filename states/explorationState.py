
import pygame
from engine.engine import Engine
from engine.inputEventKey import InputEventKey
from datetime import datetime

class ExplorationState:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.engine = Engine(self.screen)
        self.engine._ready()
        self.lastInputTime = datetime.now()

    def input(self):

        canInput = (datetime.now() - self.lastInputTime).microseconds > 500000
        if not canInput:
            return

        # Get keys pressed
        keys = pygame.key.get_pressed()

        event = InputEventKey()

        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            event.set_action_pressed("turn_left")
            self.lastInputTime = datetime.now()
        if keys[pygame.K_RIGHT] or keys[pygame.K_e]:
            event.set_action_pressed("turn_right")
            self.lastInputTime = datetime.now()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            event.set_action_pressed("forward")
            self.lastInputTime = datetime.now()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            event.set_action_pressed("backward")
            self.lastInputTime = datetime.now()
        if keys[pygame.K_a]:
            event.set_action_pressed("strafe_left")
            self.lastInputTime = datetime.now()
        if keys[pygame.K_d]:
            event.set_action_pressed("strafe_right")
            self.lastInputTime = datetime.now()

        self.engine._input(event)

    def update(self, delta):
        self.engine._process(delta)

    def draw(self):
        self.engine._draw()