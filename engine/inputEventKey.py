
class InputEventKey():

    def __init__(self) -> None:
        self.pressed = False
        self.actionsPressed = {
            "forward": False,
            "backward": False,
            "strafe_left": False,
            "strafe_right": False,
            "turn_left": False,
            "turn_right": False,
        }

    def is_action_pressed(self, eventName: str):
        return self.actionsPressed[eventName]

    def set_action_pressed(self, eventName: str):
        self.actionsPressed[eventName] = True
        self.pressed = True