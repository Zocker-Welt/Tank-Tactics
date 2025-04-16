from pygame import Rect
from pygame import display

screen = display.set_mode([1920, 1080])

screen_center_x = 960
screen_center_y = 540

def get_position(x_offset=0, y_offset=0):
    return {
        "x": screen_center_x + x_offset,
        "y": screen_center_y - y_offset,
    }

class Level:
    def setup(self, level):
        self.level = level
        self.texture = f"level_{level}"
        self.hitboxes = []
        self.generate_hitboxes()
    
    def generate_hitboxes(self):
        match self.level:
            case 1:
                self.hitboxes.extend([
                    Rect(
                        (get_position(-267, 305)["x"],get_position(-267, 305)["y"]),
                        (76,616)
                    ),
                    Rect(
                        (998, 235),
                        (308, 76)
                    ),
                    Rect(
                        (998, 772),
                        (308, 76)
                    ),
                ])