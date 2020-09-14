"""
The template of the main script of the machine learning process
"""
import random
import numpy as np

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.last_x = 0
        self.last_y = 0
        self.count = 1

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        command = "NONE"
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            if random.randint(0, 1): command = "SERVE_TO_LEFT"
            else: command = "SERVE_TO_RIGHT"
        else:
            lx = self.last_x
            ly = self.last_y
            nx = scene_info["ball"][0] #現在的 x,y
            ny = scene_info["ball"][1]
            plat_x = scene_info["platform"][0]
            def adjust(px):
                while px < 0 or px > 195: #大於邊界值計算反射
                    if px < 0: px *= -1
                    else: px = 390 - px
                return px
            
            if (ly - ny) != 0:
                if (ny - ly) > 0:
                    px = adjust((lx*(400 - ny) - nx*(400 - ly))/(ly - ny)) + random.randint(-4, 4) #避免路線一直重複
                else:
                    fny = ly*2 - ny
                    px = adjust((lx*(400 - fny) - nx*(400 - ly))/(ly - fny)) + random.randint(-4, 4) #避免路線一直重複
                    
                if abs(px - (plat_x + 20)) > 10 and px > plat_x + 20: command = "MOVE_RIGHT"
                elif abs(px - (plat_x + 20)) > 10 and px < plat_x + 20: command = "MOVE_LEFT"
            
            self.last_x = nx
            self.last_y = ny

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
