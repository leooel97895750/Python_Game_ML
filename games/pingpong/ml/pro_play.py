"""
The template of the script for the machine learning process in game pingpong
"""
import random

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.b_x = 0

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            if random.randint(0, 1): command = "SERVE_TO_LEFT"
            else: command = "SERVE_TO_RIGHT"
        else:
            nx = scene_info["ball"][0] #現在的 x,y
            ny = scene_info["ball"][1]
            sx = scene_info["ball_speed"][0] #球的方向
            sy = scene_info["ball_speed"][1]
            bx = scene_info["blocker"][0] #擋板 x

            def adjust(n, b): #大於邊界值計算反射
                while n < 0 or n > b: 
                    if n < 0: n *= -1
                    else: n = b*2 - n  
                return n

            s = 0
            if self.side == "1P":
                s = 0
                b_wall = 260
                p_y = 420
                p_name = "platform_1P"
            else: 
                s = 1
                b_wall = 240
                p_y = 80
                p_name = "platform_2P"

            command = "NONE"
#             mpx = adjust((b_wall*sx - sx*ny + sy*nx)/sy, 195) #px為經過中間點時球的x值
#             frame = abs((b_wall - ny)/sy) #frame為到中間點所需frame值
#             way = bx - self.b_x #板子方向
#             if way > 0: pbx = adjust((bx + frame*way), 170) #擋板x值加上移動值
#             else: pbx = adjust((bx + frame*way), 170)

            #if abs(ny - b_wall) < 5: print('????', bx)
                
            cnx = nx
            csy = sy
            #預測會撞到擋板時
#             if s == 0:
# #                 if b_wall <= ny and sy < 0:
# #                     print(pbx)
#                 if b_wall <= ny and sy < 0 and abs(mpx - (pbx+15)) <= 15: 
#                     #print('撞到!')
#                     #print('---', mpx, '---', frame, '---', pbx)
#                     cnx = adjust((2*mpx - nx), 195)
#                     csy = sy * -1
#             else:
#                 if b_wall >= ny and sy > 0 and abs(mpx - (pbx+15)) <= 15: 
#                     #print('撞到!')
#                     #print('---', mpx, '---', frame, '---', pbx)
#                     cnx = adjust((2*mpx - nx), 195)
#                     csy = sy * -1
            #如果撞到擋板的左側
            #如果撞到擋板的右側
            #都不會
            px = adjust((p_y*sx - sx*ny + csy*cnx)/csy, 195) + random.randint(-1, 1) #避免路線一直重複
            if px > scene_info[p_name][0] + 20: command = "MOVE_RIGHT"
            else: command = "MOVE_LEFT"

#             if s == 0:
#                 print(command)
            self.b_x = bx
 
        return command
    
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False