"""
The template of the main script of the machine learning process
"""
import random
import pickle
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
#         self.feature = np.array([1, 2, 3, 4, 5, 6, 7])

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        command = "NONE"
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or scene_info["status"] == "GAME_PASS"):
#             print(self.count)
#             if self.count%10 == 0: #每10次破關資料儲存
#                 print('save feature')
#                 file = open('arkanoid_E3_20200824_'+str(self.count)+'.pkl', 'wb')
#                 pickle.dump(self.feature, file)
#                 file.close()
#                 self.feature = np.array([1, 2, 3, 4, 5, 6, 7]) #初始化feature陣列
#             self.count += 1
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            if random.randint(0, 1): command = "SERVE_TO_LEFT"
            else: command = "SERVE_TO_RIGHT"
        else:
            nx = scene_info["ball"][0] #現在的 x,y
            ny = scene_info["ball"][1]
            plat_x = scene_info["platform"][0]
            lx = self.last_x
            ly = self.last_y
            if (ly - ny) != 0:
                def adjust(n): #大於邊界值計算反射
                    while n < 0 or n > 195: 
                        if n < 0: n *= -1
                        else: n = 390 - n
                    return n
                px = adjust((lx*(400 - ny) - nx*(400 - ly))/(ly - ny)) + random.randint(-8, 8) #避免路線一直重複
                if abs(px - (plat_x + 20)) < 8: command = "NONE"
                elif px > plat_x + 20: command = "MOVE_RIGHT"
                else: command = "MOVE_LEFT"

                #特徵儲存
#                 c = 0 #command: 0=none 1=left 2=right
#                 if command == "MOVE_LEFT": c = 1
#                 elif command == "MOVE_RIGHT": c = 2
#                 #[上一楨球的x, 上一楨球的y, x, y, 平台x值, 平台移動模式, 平台正確x值]
#                 feature_row = np.array([lx, ly, nx, ny, plat_x, c, px]) 
#                 self.feature = np.vstack((self.feature, feature_row))
            
            self.last_x = nx
            self.last_y = ny

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
