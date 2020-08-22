"""
The template of the main script of the machine learning process
"""
import random

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.last_x = 0
        self.last_y = 0

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"
        else:
            nx = scene_info["ball"][0] #現在的 x,y
            ny = scene_info["ball"][1]
            
            if ny > self.last_y: #下降時計算路線
                px = (self.last_x*(400 - ny) - nx*(400 - self.last_y))/(self.last_y - ny) #預測的平台 x值
                while px < 0 or px > 195: #大於邊界值計算反射
                    if px < 0: px *= -1
                    else: px = 390 - px
                px += random.randint(-5, 5) #避免路線一直重複
                if px > scene_info["platform"][0] + 20: command = "MOVE_RIGHT"
                else: command = "MOVE_LEFT"
                    
            else: #上升時平台置中
                if scene_info["platform"][0] > 80: command = "MOVE_LEFT"
                else: command = "MOVE_RIGHT"  

            self.last_x = nx
            self.last_y = ny

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
